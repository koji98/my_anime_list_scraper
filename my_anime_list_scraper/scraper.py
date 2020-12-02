import requests
from bs4 import BeautifulSoup
import cleaner
import extractor
import saver


class MalScraper:
    """
    This class defines a scraper for www.myanimelist.com.
    """

    def __init__(self, output_type="tsv", output_location=None):
        """
        Parameters
        ----------
        output_type : str
        The format to save the data. Either "tsv" or "sql".
        output_location : str
        The location to save the data if output_type="tsv".
        """
        self.output_type = output_type
        self.output_location = output_location
        self.base_url = "https://myanimelist.net/"

    def scrape_details(self, content_type="anime", start_page=0, failure_threshold=100, print_intermediate=False):
        """
        Scrapes MyAnimeList detail pages.

        Parameters
        ----------
        content_type : str
        The type of page being scraped. Either "anime" or "manga".
        start_page : int
        The location to start at (e.g. type="anime" and start_page=5 => https://myanimelist.net/anime/5 )
        failure_threshold : int
        The number of consecutive fails allowed before stopping the scraper. A fail is when a 404 page is returned,
        signifying no content is at that page.
        print_intermediate : bool
        Determines if intermediate output would be appreciated by the user (current page being scraped, number of 
        consectuve fails, etc.).
        """
        continue_scraping = True
        mal_id = start_page
        failure_count = 0

        if print_intermediate:
            print("=======================STARTING MYANIMELIST SCRAPER=======================\n\n")

        while continue_scraping:
            url = self.base_url + content_type + "/" + str(mal_id)

            if print_intermediate:
                print("Scraping: " + url)

            # Request page
            page = requests.get(url)

            # Parse content
            soup = BeautifulSoup(page.content, "html.parser")

            # Check if content_type with this id was found
            page_not_found = soup.find("div", class_="error404") is not None

            # If we get the 404 page, increase the failure_count
            if page_not_found:
                failure_count = failure_count + 1

                if print_intermediate:
                    print("Page not found in " + str(failure_count) + " continuous attempts.")

                # If we have reached our limit off continuous 404 pages, stop scraping
                # (this assumes there's nothing left to scrape)
                if failure_count == failure_threshold:
                    continue_scraping = False
            else:
                # Set failure count to 0 because we succeeded
                failure_count = 0
                info = self.__get_anime_details(soup, mal_id) if content_type == "anime" else None

                if self.output_type is "tsv":
                    saver.save_as_tsv(self.output_location, info, "mal_" + content_type + "_details.tsv")
                elif self.output_type is "sql":
                    saver.save_as_sql(self.output_location, info, "mal_" + content_type + "_details.sql", "MAL_" + content_type.capitalize() + "_Details")

                break

            mal_id = mal_id + 1

    def __get_anime_details(self, soup, mal_id):
        """
        Extracts an anime page's details and statistics.

        Parameters
        ----------
        soup : BeautifulSoup object
            The BeautifulSoup object containing the page's content
        mal_id : int
            Id of the anime being scraped
        """
        details_dict = extractor.extract_anime_details(soup, mal_id)
        cleaned_dict = self.__clean_anime_details(details_dict)

        return cleaned_dict

    def __clean_anime_details(self, information_dict):
        """
        Cleans raw extracted data

        Parameters
        ----------
        information_dict : dict
            The dictionary holding extracted data
        """
        return cleaner.clean_anime_details(information_dict)

if __name__ == "__main__": 
    m = MalScraper()
    m.scrape_details(print_intermediate=True)