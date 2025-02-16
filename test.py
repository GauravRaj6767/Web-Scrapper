from flask import Flask, render_template, request
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
import requests


def scrape_amazon(query):
    prod_name = query.replace(' ', '+')
    url = f'https://www.amazon.in/s?k={prod_name}'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # Set the user agent via Chrome options
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"
    )

    # Use the correct path to your chromedriver.exe file
    s = Service('chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=chrome_options)

    driver.get(url)
    driver.implicitly_wait(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    results = soup.find_all("div", {"data-component-type": "s-search-result"})
    # print(results[1])

    for obj in results:
        try:
            title = obj.find(
                "a", class_="a-link-normal s-line-clamp-2 s-link-style a-text-normal").h2.span.text.strip()
            # price = obj.find("span", class_="a-offscreen").text.strip()
            # rating = obj.find("span", class_="a-icon-alt").text.strip()
            print(title)
        except:
            print("NA")


def scrape_flipkart(query):
    prod_name = query.replace(' ', '%20')
    url = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'.format(
        prod_name)
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    products = soup.find_all('div', attrs={'class': '_75nlfW'})

    print(len(products))
    # print(products[5])
    rating = products[5].find(
        'div', attrs={'class': 'XQDdHH'}).text + "out of 5 stars"
    print(rating)
    # i_link = (products[5].find('div', attrs={'class': '_4WELSP'}).img)['src']
    # print(i_link)
    # # img_link = (products[5].find('div', attrs={'class': '_4WELSP'}))['src']
    # # print(img_link)

    # # print("https://www.flipkart.com{}".format(link))
    # for obj in products:
    #     img_link = (obj.find('div', attrs={'class': '_4WELSP'}).img)['src']
    #     # link = (obj.find('a', attrs={'class': 'CGtC98'}))['href']
    #     # prod_link = "https://www.flipkart.com{}".format(link)
    #     # title = (obj.find('div', attrs={'class': 'KzDlHZ'})).text.strip()
    #     # price = (obj.find('div', attrs={'class': 'Nx9bqj _4b5DiR'})).text.strip()
    #     print(img_link)


if __name__ == "__main__":
    scrape_flipkart("laptops")
