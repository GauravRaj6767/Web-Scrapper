from flask import Flask, render_template, request
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


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
    products = []
    for product in results:
        try:
            title = product.find(
                "a", class_="a-link-normal s-line-clamp-2 s-link-style a-text-normal").h2.span.text.strip()
        except Exception:
            title = "N/A"
        try:
            price = product.find("span", class_="a-offscreen").text.strip()
        except Exception:
            price = "N/A"
        try:
            rating = product.find("span", class_="a-icon-alt").text.strip()
        except Exception:
            rating = "N/A"
        try:
            img_elem = product.find("img", class_="s-image")
            img_link = img_elem["src"] if img_elem and "src" in img_elem.attrs else ""
        except Exception:
            img_link = ""
        try:
            link_elem = product.find("a", class_="a-link-normal")
            if link_elem and "href" in link_elem.attrs:
                prod_link = "https://www.amazon.in" + link_elem["href"]
            else:
                prod_link = "#"
        except Exception:
            prod_link = "#"

        products.append({
            "title": title,
            "price": price,
            "rating": rating,
            "img_link": img_link,
            "prod_link": prod_link
        })
    return products


def scrape_flipkart(query):
    prod_name = query.replace(' ', '%20')
    url = f'https://www.flipkart.com/search?q={prod_name}&otracker=search'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    results = soup.find_all('div', attrs={'class': '_75nlfW'})
    products = []
    for obj in results:
        try:
            img_link = obj.find('div', attrs={'class': '_4WELSP'}).img['src']
        except Exception:
            img_link = "N/A"
        try:
            title = obj.find('div', attrs={'class': 'KzDlHZ'}).text.strip()
        except Exception:
            title = "N/A"
        try:
            price = obj.find(
                'div', attrs={'class': 'Nx9bqj _4b5DiR'}).text.strip()
        except Exception:
            price = "N/A"
        try:
            link = obj.find('a', attrs={'class': 'CGtC98'})['href']
            prod_link = f"https://www.flipkart.com{link}"
        except Exception:
            prod_link = "N/A"
        try:
            rating = obj.find(
                'div', attrs={'class': 'XQDdHH'}).text.strip() + " out of 5 stars"
        except Exception:
            rating = "N/A"

        products.append({
            "title": title,
            "price": price,
            "rating": rating,
            "img_link": img_link,
            "prod_link": prod_link
        })
    return products


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        amazon_products = scrape_amazon(query)
        flipkart_products = scrape_flipkart(query)
        return render_template("results.html", query=query,
                               amazon_products=amazon_products,
                               flipkart_products=flipkart_products)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
