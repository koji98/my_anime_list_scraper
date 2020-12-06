import math
from collections import OrderedDict 

def clean_anime_details(information_dict):
    """
    Cleans raw extracted data

    Parameters
    ----------
    information_dict: dict
        The dictionary holding extracted data
    """

    # Creating final dictionary from dictionary passed since hard to account for values (changes sometimes based on page).
    clean_information_dict = OrderedDict()

    # Removing whitespace
    clean_information_dict["AltNameEnglish"] = information_dict["English"].strip() if "English" in information_dict else None
    clean_information_dict["AltNameSynonyms"] = information_dict["Synonyms"].strip() if "Synonyms" in information_dict else None
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
