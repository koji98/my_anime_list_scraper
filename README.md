# my_anime_list_scraper
A package to easily scrape www.myanimelist.com. The purpose of this package is to scrape large amounts of data from MyAnimeList, not to request individual information about a specific item within MyAnimeList. This package can be used to request individual information, but would recommend you to look towards another tool for that as this was not created with that in mind. 

*my_anime_list_scraper* is being developed mainly for [anibrain.ai](anibrain.ai). This package will be updated as needed for the site mentioned above. If you require additional information currently not available through this package, please reach out or feel free to contribute.

## Installation
`pip install my_anime_list_scraper`

## Usage
### Importing the scraper
`from my_anime_list_scraper.scraper import MalScraper`

### Instantiating the scraper
| Constructor Parameters | Type | Description |
| --- | --- | --- |
| output_type | string | How the scraper will save the data. Either "tsv" or "mysql" <br/><br/> Default Value: "tsv" |
| output_location | string | The location to save the data. <br/><br/> Required if `output_type="tsv"` |
| db_host | string | The database host. <br/><br/> Required if `output_type="mysql"` |
| db_user | string | The username to access the database. <br/><br/> Required if `output_type="mysql"` |
| db_password | string | The password to access the database. <br/><br/> Required if `output_type="mysql"` |
| db_database | string | The database name to write scrape data to. <br/><br/> Required if `output_type="mysql"` |

#### Scraper saves data as TSV
`mal_scraper = MalScraper(output_type='tsv', output_location='/Home/example/folder/)`

#### Scraper saves data in MySQL Database
`mal_scraper = MalScraper(output_type='mysql', output_location='/Home/example/folder/, db_host=example_host_name, db_user=example_user, db_password=example_password, db_database=example_database)`

## Methods

**scrape_details()**

| Parameters | Type | Description |
| --- | --- | --- |
| content_type | string | The type of the page being scraped. <br/> Only "anime" available right now <br/><br/> Default Value: "anime" |
| start_page | int | The page to start scraping *(e.g. type="anime" and start_page=5 => https://myanimelist.net/anime/5 )* <br/><br/> Default Value: 0 |
| failure_threshold | int | The number of consecutive fails allowed before stopping the scraper. A fail is when a 404 page is returned, signifying no content is at that page. <br/><br/> Default Value: 100 |
| print_intermediate | bool | Determine if to print intermediate output during scrape to keep user informed on progress <br/><br/> Default Value: False |

Scraped Details (anime example):

`{
   "AltNameEnglish":"Cowboy Bebop",
   "AltNameSynonyms":None,
   "AltNameJapanese":"カウボーイビバップ",
   "MediaType":"TV",
   "EpisodeCount":26,
   "CurrentStatus":"Finished Airing",
   "Aired":"Apr 3, 1998 to Apr 24, 1999",
   "Premiered":"Spring 1998",
   "Broadcast":"Saturdays at 01",
   "Producers":"Bandai Visual",
   "Licensors":"Funimation,Bandai Entertainment",
   "Studios":"Sunrise",
   "Source":"Original",
   "Genres":"Action,Adventure,Comedy,Drama,Sci-Fi,Space",
   "Duration":"24 min. per ep.",
   "Rating":"R - 17+ (violence & profanity)",
   "Score":8.79,
   "ScoredByCount":566904,
   "Ranked":25,
   "Popularity":37,
   "MembersCount":1159776,
   "FavoritesCount":58298,
   "Title":"Cowboy Bebop",
   "Synopsis":"In the year 2071, humanity has colonized several of the planets and moons of the solar system leaving the now uninhabitable surface of planet Earth behind. The Inter Solar System Police attempts to keep peace in the galaxy, aided in part by outlaw bounty hunters, referred to as \"Cowboys.\" The ragtag team aboard the spaceship Bebop are two such individuals. Mellow and carefree Spike Spiegel is balanced by his boisterous, pragmatic partner Jet Black as the pair makes a living chasing bounties and collecting rewards. Thrown off course by the addition of new members that they meet in their travels—Ein, a genetically engineered, highly intelligent Welsh Corgi; femme fatale Faye Valentine, an enigmatic trickster with memory loss; and the strange computer whiz kid Edward Wong—the crew embarks on thrilling adventures that unravel each member\\'s dark and mysterious past little by little. Well-balanced with high density action and light-hearted comedy, Cowboy Bebop is a space Western classic and an homage to the smooth and improvised music it is named after. [Written by MAL Rewrite]",
   "MyAnimeListId":1,
   "PromoVideo":"https://www.youtube.com/embed/qig4KOK2R2g?enablejsapi=1&wmode=opaque&autoplay=1",
   "PromoVideoBackgroundImage":"https://i.ytimg.com/vi/qig4KOK2R2g/mqdefault.jpg",
   "ImageSrc":"https://cdn.myanimelist.net/images/anime/4/19644.jpg"
}`