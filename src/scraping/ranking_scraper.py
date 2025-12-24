from time import sleep
from bs4 import BeautifulSoup
from src.utils.scraping import scrape_page, save_csv
from src.models.ranking import Ranking
    

def scrape_ranking_from_url(url: str) -> list[Ranking]:
    page = scrape_page(url)
    return scrape_ranking(page)


def scrape_ranking(page: BeautifulSoup) -> list[Ranking]:
    listings: list[Ranking] = []

    table = page.find('table', class_='top-ranking-table')
    shows = table.find_all('tr', class_='ranking-list')

    for row in shows:
        rank = int(row.td.span.text)
        title = row.find('td', class_='title').div.find('div', class_='di-ib').h3.a.text
        score = float(row.find('td', class_='score').find('span', class_='text').text)
        url = row.find('td', class_='title').div.find('div', class_='di-ib').h3.a['href']
        thumbnail = row.find('td', class_='title').a.img.attrs.get('data-src', '')

        ranking = Ranking(rank, title, score, url, thumbnail)
        listings.append(ranking)

    return listings


def scrape_ranking_pages(pages: int = 1) -> list[Ranking]:
    lst: list[Ranking] = []
    
    for page in range(0, pages):
        url = f"https://myanimelist.net/topanime.php?limit={page * 50}"
        lst.extend(scrape_ranking_from_url(url))
        # sleep(1)

    return lst


def save_rankings_as_csv(rankings: list[Ranking], filename: str) -> None:
    save_csv(rankings, ['rank', 'title', 'score', 'url', 'thumbnail'], filename)
    
    
def main():
    import sys
    pages = 1
    if len(sys.argv) > 1:
        pages = int(sys.argv[1])
    
    ranks = scrape_ranking_pages(pages)
    save_rankings_as_csv(ranks, 'rankings.csv')


if __name__ == "__main__":
    main()
