# Data analysis project

## Pre requisite
Install uv (run in powershell)
```ps
powershell -c "irm https://astral.sh/uv/install.ps1 | more"
```

## Scraping MAL

### Scraping top animes

```sh
# one page (50 entry)
uv --native-tls run -m src.scraping.ranking_scraper

# three pages (150 entry)
uv --native-tls run -m src.scraping.ranking_scraper 3
```

### Scraping shows

```sh
# one entry
uv --native-tls run -m src.scraping.show_scraper

# twenty entries
uv --native-tls run -m src.scraping.show_scraper 20
```