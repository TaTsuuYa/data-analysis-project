from time import sleep
from bs4 import BeautifulSoup
from src.scraping.ranking_scraper import scrape_ranking_pages
from src.utils.scraping import scrape_page, save_csv
from src.utils.scraping import scrape_page, save_csv
from src.models.show import Show


def scrape_show_from_url(url: str) -> Show | None:
    page = scrape_page(url)
    if 'Human Verification' in page.text:
        print(f"CAPTCHA detected for {url}")
        return None
    return scrape_show(page)


def scrape_show(page: BeautifulSoup) -> Show:
    title = page.find('h1').text.strip()
    side = page.find('table').td
    img = side.div.div.a.img.attrs.get('data-src', '')
    info = side.find_all('div', class_='spaceit_pad')
    info = {field.text.split(':')[0].strip(): ' '.join(field.text.split(':')[1].split()).strip() for field in info}
    type = info.get('Type', '')
    episodes = info.get('Episodes', '')
    status = info.get('Status', '')
    aired = info.get('Aired', '')
    premiered = info.get('Premiered', '')
    broadcast = info.get('Broadcast', '')
    producers = info.get('Producers', '')
    licensors = info.get('Licensors', '')
    studios = info.get('Studios', '')
    source = info.get('Source', '')
    genres_list = info.get('Genres', '').split(', ')
    genres = ', '.join(g[:len(g)//2] for g in genres_list)
    demographic_raw = info.get('Demographic', '')
    demographic = demographic_raw[:len(demographic_raw)//2]
    duration = info.get('Duration', '')
    rating = info.get('Rating', '')
    score = info.get('Score', '0.0').split()[0]
    rank = info.get('Ranked', '#0').replace('#', '').split('2 2')[0]
    popularity = info.get('Popularity', '#0').replace('#', '')
    members = info.get('Members', '0').replace(',', '')
    favorites = info.get('Favorites', '0').replace(',', '')
    
    h2 = page.find('h2', id='summary_stats')
    stats = h2.find_next_siblings('div', class_='spaceit_pad')
    stats = {field.text.split(':')[0].strip(): ' '.join(field.text.split(':')[1].split()).strip() for field in stats}
    
    show = Show(
        title=title,
        url='',
        img=img,
        score=float(score),
        rank=int(rank) if rank.isdigit() else 0,
        popularity=int(popularity) if popularity.isdigit() else 0,
        watching=int(stats.get('Watching', '0').replace(',', '')),
        completed=int(stats.get('Completed', '0').replace(',', '')),
        on_hold=int(stats.get('On-Hold', '0').replace(',', '')),
        dropped=int(stats.get('Dropped', '0').replace(',', '')),
        plan_to_watch=int(stats.get('Plan to Watch', '0').replace(',', '')),
        members=int(members) if members.isdigit() else 0,
        favorites=int(favorites) if favorites.isdigit() else 0,
        type=type,
        episodes=int(episodes) if episodes.isdigit() else 0,
        status=status,
        aired=aired,
        premiered=premiered,
        broadcast=broadcast,
        producers=producers,
        licensors=licensors,
        studios=studios,
        Source=source,
        genres=genres,
        demographic=demographic,
        duration=duration,
        rating=rating
    )

    return show


def scrape_n_shows(number: int = 1) -> list[Show]:
    lst: list[Show] = []
    kanigs = scrape_ranking_pages((number // 50) + 1)
    
    for i in range(number):
        print(f"---------- Scraping show {i + 1}/{number}: {kanigs[i].title} ----------")

        url = kanigs[i].url + '/stats'
        show = scrape_show_from_url(url)
        if show is not None:
            show.url = kanigs[i].url
            lst.append(show)
            # sleep(0.5)
        else:
            i -= 1  # Retry the same index in case of CAPTCHA
            sleep(5)

    return lst


def save_shows_as_csv(shows: list[Show], filename: str) -> None:
    save_csv(shows, ['title',
        'url',
        'img',
        'score',
        'rank',
        'popularity',
        'watching',
        'completed',
        'on_hold',
        'dropped',
        'plan_to_watch',
        'members',
        'favorites',
        'type',
        'episodes',
        'status',
        'aired',
        'premiered',
        'broadcast',
        'producers',
        'licensors',
        'studios',
        'Source',
        'genres',
        'demographic',
        'duration',
        'rating'], filename)
    
    
def main():
    import sys
    number = 1
    if len(sys.argv) > 1:
        number = int(sys.argv[1])
    
    ranks = scrape_n_shows(number)
    save_shows_as_csv(ranks, 'shows.csv')


if __name__ == "__main__":
    main()
