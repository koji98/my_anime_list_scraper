# my_anime_list_scraper
A package to easily scrape www.myanimelist.com. The purpose of this package is to scrape large amounts of data from MyAnimeList, not to request individual information about a specific item within MyAnimeList. This package can be used to request individual information, but would recommend you to look towards another tool for that as this was not created with that in mind. 

*my_anime_list_scraper* is being developed mainly for [anibrain.ai](anibrain.ai). This package will be updated as needed for the site mentioned above. If you require additional information currently not available through this package, please reach out or feel free to contribute.

## Installation
`pip install my_anime_list_scraper`

## Usage
### Importing the scraper
`from scraper import MalScraper`

### Instantiating the scraper
Based on how you want to save the data, the parameters requried for the scraper constructor differs.

#### Scraper saves data as TSV
`mal_scraper = MalScraper(output_type='tsv', output_location='/Home/example/folder/)`

#### Scraper saves data in MySQL Database
`mal_scraper = MalScraper(output_type='mysql', output_location='/Home/example/folder/, db_host=example_host_name, db_user=example_user, db_password=example_password, db_database=example_database)`

## Methods
**scrape_details()**
| Parameter | Type | Description |
| --- | --- | --- |
| content_type | string | The type of the page being scraped. \n Only "anime" available right now |
| start_page | int | The page to start scraping *(e.g. type="anime" and start_page=5 => https://myanimelist.net/anime/5 )* |
| failure_threshold | int | The number of consecutive fails allowed before stopping the scraper. A fail is when a 404 page is returned, signifying no content is at that page. |
| print_intermediate | bool | Determine if to print intermediate output during scrape to keep user informed on progress |