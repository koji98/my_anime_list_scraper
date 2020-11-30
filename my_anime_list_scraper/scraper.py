import requests
from bs4 import BeautifulSoup
import math


class MalScraper:
    """
    This class defines a scraper for www.myanimelist.com.
    """

    def __init__(self, output_type="tsv", output_location=None, db_host=None,
                 db_user=None, db_password=None, db_database=None):
        """
        Parameters
        ----------
        output_type : str
        The format to save the data. Either "tsv" or "mysql".
        output_location : str
        The location to save the data if output_type="tsv".
        db_host : str
        The database host. Required if output_type="mysql".
        db_user : str
        The database user. Required if output_type="mysql".
        db_password : str
        The database password. Required if output_type="mysql".
        db_database : str
        The database name. Required if output_type="mysql".
        """
        self.output_type = output_type
        self.output_location = output_location
        self.base_url = "https://myanimelist.net/"

        if (db_host is not None) and (db_user is not None) and (db_password is not None) and (db_database is not None):
            self.sql_manager = DatabaseManager(
                db_host, db_user, db_password, db_database)

        class DatabaseManager:
            """
            This class defines a database manager for opening connections, 
            closing connections, and querying the tables within the database.
            """

            import mysql.connector

            def __init__(self, host, user, password, database):
                """
                Parameters
                ----------
                host : str
                The database host.
                user : str
                The database user.
                password : str
                The database password.
                database : str
                The database name.
                """
                self.host = host
                self.user = user
                self.password = password
                self.database = database
                self.db = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )

            def close(self):
                """
                Closes the open connection to the database
                Users of this class should **always** call close when they are
                done with this class so it can clean up the DB connection.
                """
                self.db.close()

            def connect(self):
                """
                Opens a connection to the database.
                """
                self.db = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )

            def insert(self, query, values):
                """
                Executes the provided query with the value(s) on the 
                database.

                Parameters
                ----------
                query : str
                A sql insert query.
                values : tuple
                Values to be inserted to the table
                """
                cursor = self.db.cursor()

                if type(values) is list:
                    cursor.executemany(query, values)
                else:
                    cursor.execute(query, values)

                self.db.commit()

    def scrape_title_details(self, content_type="anime", start_page=0, failure_threshold=100, print_intermediate=False):
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
                break
                save_data(db, info)

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
        dark_text_child_data = soup.find_all("span", class_="dark_text")
        details_dict = {}

        for child in dark_text_child_data:
            parent = child.parent

            if parent.has_attr("itemprop"):
                rating_value = parent.find(
                    "span", itemprop="ratingValue").text.strip()
                rating_count = parent.find(
                    "span", itemprop="ratingCount").text.strip()
                details_dict["Score"] = rating_value
                details_dict["ScoredByCount"] = rating_count
            else:
                superscript_element = parent.find("sup")
                statistics_element = parent.find("div", class_="statistics-info info2")

                # Removing uninteresting elements to make data easier to parse
                if superscript_element is not None:
                    superscript_element.decompose()

                if statistics_element is not None:
                    statistics_element.decompose()

                key_value = parent.text.strip().split(":")
                details_dict[key_value[0]] = key_value[1]

        title = soup.select("h1.title-name strong")[0].text.strip()
        description = soup.find("p", itemprop="description").text.strip()
        image = soup.find("img", itemprop="image")["data-src"].strip()
        video = soup.find("a", class_="iframe js-fancybox-video video-unit promotion")
        
        if video is not None:
            promo_video = video["href"]
            promo_video_background_image = video["style"]
            details_dict["PromoVideo"] = promo_video
            details_dict["PromoVideoBackgroundImage"] = promo_video_background_image

        details_dict["Title"] = title
        details_dict["ImageSrc"] = image
        details_dict["Synopsis"] = description
        details_dict["MyAnimeListId"] = mal_id

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
        # Creating final dictionary from dictionary passed since hard to account for values (changes sometimes based on page).
        clean_information_dict = {}

        # Removing whitespace
        clean_information_dict["AltNameEnglish"] = information_dict["English"].strip() if "English" in information_dict else None
        clean_information_dict["AltNameSynonyms"] = information_dict["Synonyms"].strip() if "Synonyms" in information_dict else None
        clean_information_dict["AltNameJapanese"] = information_dict["Japanese"].strip() if "Japanese" in information_dict else None
        clean_information_dict["MediaType"] = information_dict["Type"].strip() if "Type" in information_dict else None
        
        # try-except due to type conversion
        try:
            clean_information_dict["EpisodeCount"] = int(information_dict["Episodes"].strip()) if "Episodes" in information_dict else None
        except:
            clean_information_dict["EpisodeCount"] = None

        clean_information_dict["CurrentStatus"] = information_dict["Status"].strip() if "Status" in information_dict else None
        clean_information_dict["Aired"] = information_dict["Aired"].strip() if "Aired" in information_dict else None
        clean_information_dict["Premiered"] = information_dict["Premiered"].strip() if "Premiered" in information_dict else None
        clean_information_dict["Broadcast"] = information_dict["Broadcast"].strip() if "Broadcast" in information_dict else None
        clean_information_dict["Producers"] = ",".join(map(lambda x: x.strip(), information_dict["Producers"].split(","))) if "Producers" in information_dict else None
        clean_information_dict["Licensors"] = ",".join(map(lambda x: x.strip(), information_dict["Licensors"].split(","))) if "Licensors" in information_dict else None
        clean_information_dict["Studios"] = ",".join(map(lambda x: x.strip(), information_dict["Studios"].split(","))) if "Studios" in information_dict else None
        clean_information_dict["Source"] = information_dict["Source"].strip() if "Source" in information_dict else None
        clean_information_dict["Genres"] = ",".join(map(lambda x: x.strip()[0: math.floor(len(x.strip()) / 2)], information_dict["Genres"].split(","))) if "Genres" in information_dict else None
        clean_information_dict["Duration"] = information_dict["Duration"].strip() if "Duration" in information_dict else None
        clean_information_dict["Rating"] = information_dict["Rating"].strip() if "Rating" in information_dict else None

        try:
            clean_information_dict["Score"] = float(information_dict["Score"].strip()) if "Score" in information_dict else None
        except:
            clean_information_dict["Score"] = None

        try:
            clean_information_dict["ScoredByCount"] = int(information_dict["ScoredByCount"].strip()) if "ScoredByCount" in information_dict else None
        except:
            clean_information_dict["ScoredByCount"] = None

        try:
            clean_information_dict["Ranked"] = int(information_dict["Ranked"].strip()[1:]) if "Ranked" in information_dict else None
        except:
            clean_information_dict["Ranked"] = None

        try:
            clean_information_dict["Popularity"] = int(information_dict["Popularity"].strip()[1:]) if "Popularity" in information_dict else None
        except:
            clean_information_dict["Popularity"] = None

        try:
            clean_information_dict["MembersCount"] = int(information_dict["Members"].strip().replace(",", "")) if "Members" in information_dict else None
        except:
            clean_information_dict["MembersCount"] = None

        try:
            clean_information_dict["FavoritesCount"] = int(information_dict["Favorites"].strip().replace(",", "")) if "Favorites" in information_dict else None
        except:
            clean_information_dict["FavoritesCount"] = None

        clean_information_dict["Title"] = information_dict["Title"].strip() if "Title" in information_dict else None
        clean_information_dict["Synopsis"] = " ".join(information_dict["Synopsis"].strip().split()) if "Synopsis" in information_dict else None
        clean_information_dict["MyAnimeListId"] = information_dict["MyAnimeListId"]
        clean_information_dict["PromoVideo"] = information_dict["PromoVideo"].strip() if "PromoVideo" in information_dict else None
        clean_information_dict["PromoVideoBackgroundImage"] = information_dict["PromoVideoBackgroundImage"][information_dict["PromoVideoBackgroundImage"].find("(") + 2: information_dict["PromoVideoBackgroundImage"].rfind(")") - 1] if "PromoVideoBackgroundImage" in information_dict else None
        clean_information_dict["ImageSrc"] = information_dict["ImageSrc"].strip() if "ImageSrc" in information_dict else None

        return clean_information_dict

if __name__ == "__main__": 
    m = MalScraper()
    m.scrape_title_details(print_intermediate=True)