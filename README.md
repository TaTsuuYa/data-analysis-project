# Data analysis project

## Scraping MAL

### Scraping top animes

```sh
# one page (50 entry)
uv --native-tls run -m src.scraping.ranking_scraper

# three pages (150 entry)
uv --native-tls run -m src.scraping.ranking_scraper 3
```