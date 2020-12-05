def extract_anime_details(soup, mal_id):
    """
    Extracts an anime page's details and statistics.

    Parameters
    ----------
    soup: BeautifulSoup object
        The BeautifulSoup object containing the page's content
    mal_id: int
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

    return details_dict