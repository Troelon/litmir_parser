from bs4 import BeautifulSoup
import lxml
import requests
import json

def get_data():
    global book_hash
    book_hash = []
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.52"
    }
    url = "https://www.litmir.me/main_page?type=OnShowDown&rs=5%7C1%7C0&o=20&p=1"

    page_count = BeautifulSoup(requests.get("https://www.litmir.me/main_page?type=OnShowDown&rs=5%7C1%7C0&o=20&p=1").text,"lxml")
    page_count = page_count.find("td", attrs={"style":"padding-right: 10px"})
    pages = page_count.find_all("a")
    print(pages[-1].text)

    for i in range(1,4): #int(pages[-1].text) # количество страниц с которых нужно собрать
        url = f"https://www.litmir.me/main_page?type=OnShowDown&rs=5%7C1%7C0&o=20&p={i}"
        req = requests.get(url = url, headers=headers)
        soup = BeautifulSoup(req.text,"lxml")

        book_list = soup.find("div", attrs={"jq":"BookList"})
        book_list = book_list.find_all("table")
        for el in book_list:
            book_name = el.find("span", attrs = {"itemprop":"name"}).text
            book_author = el.find("span", attrs = {"itemprop":"author","class":"desc2"}).text
            book_genre = el.find("span", attrs = {"itemprop":"genre"}).text
            box = el.find("div", attrs = {"class":"desc_container"}).find_all("div")
            book_series = box[2].a
            if book_series != None:
                book_series = book_series.text
                book_series = book_series.replace(' ','',1)
            book_pages = box[-2].find_all("span")[-1].text
            book_status = box[-1].text
            book_content = el.find("div", attrs = {"class":"BBHtmlCodeInner"}).text
            
            book_author = book_author.strip()
            book_genre = book_genre.strip()
            book_pages = book_pages.strip()          #Блок удаления пробелов
            book_pages = book_pages.strip()
            book_content = book_content.strip()

            book_hash.append({
                'name':f'{book_name}',
                'author':f'{book_author}',
                'genre':f'{book_genre}',
                'pages':f'{book_pages}',
                'status':f'{book_status}',
                'short_content':f'{book_content}'
            })
     
    


def main():
    get_data()
    with open("data.json","w",encoding="utf8") as f:
        json.dump(book_hash,f, indent = 4, ensure_ascii = False)


if __name__ == "__main__":
    main()