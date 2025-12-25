from bs4 import BeautifulSoup
import requests


def scrape_page(url: str, params: str = "") -> BeautifulSoup:
    url += params
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, verify=False)
    return BeautifulSoup(response.content, 'lxml')


def save_csv(data: list, rows: list[str], filename: str) -> None:
    import csv
    from dataclasses import fields

    with open('data/' + filename, mode='w+', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(rows)

        for item in data:
            writer.writerow([getattr(item, field.name) for field in fields(item) if field.name in rows])
            
    print(f"Data saved to {filename}")
    
