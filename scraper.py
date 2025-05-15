import aiohttp
from bs4 import BeautifulSoup

async def fetch_car_prices():
    base_url = "https://www.spot.uz/oz/search/?q=mashina+narxlari"
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="article-preview__title")

    for link in links:
        if "narx" in link.text.lower() or "avtomobil" in link.text.lower():
            article_url = "https://www.spot.uz" + link["href"]
            return await parse_article(article_url)

    return None

async def parse_article(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_="article-body")

    if not article:
        return None

    lines = article.get_text(separator="\n").split("\n")
    narxlar = []
    for line in lines:
        if any(car in line.lower() for car in ["nexia", "malibu", "cobalt", "damas", "tracker", "spark", "captiva", "chevrolet", "gm"]) and "so" in line.lower():
            narxlar.append(line.strip())

    return {"url": url, "prices": narxlar[:10]}
