def create_mal_anime_details_table():
    """
    Returns query string for creating the MAL_Anime_Details table.
    """

    return """
    CREATE TABLE MAL_Anime_Details (
        MAL_Id int NOT NULL PRIMARY KEY,
        Title varchar(255) DEFAULT NULL,
        AltNameEnglish varchar(255) DEFAULT NULL,
        AltNameSynonyms varchar(255) DEFAULT NULL,
        AltNameJapanese varchar(255) DEFAULT NULL,
        Synopsis mediumtext DEFAULT NULL,
        MediaType varchar(50) DEFAULT NULL,
        EpisodeCount int DEFAULT NULL,
        CurrentStatus varchar(255) DEFAULT NULL,
        Aired varchar(255) DEFAULT NULL,
        Premiered varchar(255) DEFAULT NULL,
        Broadcast varchar(255) DEFAULT NULL,
        Producers varchar(255) DEFAULT NULL,
        Licensors varchar(255) DEFAULT NULL,
        Studios varchar(255) DEFAULT NULL,
        Source varchar(50) DEFAULT NULL,
        Genres varchar(255) DEFAULT NULL,
        Duration varchar(255) DEFAULT NULL,
        Rating varchar(50) DEFAULT NULL,
        PromoVideoSrc varchar(255) DEFAULT NULL,
        PromoVideoBackgroundImageSrc varchar(255) DEFAULT NULL,
        ImageSrc varchar(255) DEFAULT NULL
    );
    """

def create_mal_anime_detail_stats_table():
    """
    Returns query string for creating the MAL_Anime_Detail_Stats table.
    """

    return """
    CREATE TABLE MAL_Anime_Detail_Stats (
        MAL_Id int NOT NULL PRIMARY KEY,
        Score float(24) DEFAULT NULL,
        ScoredByCount int DEFAULT NULL,
        Ranked int DEFAULT NULL,
        Popularity int DEFAULT NULL,
        MembersCount int DEFAULT NULL,
        FavoritesCount int DEFAULT NULL,
        FOREIGN KEY (MAL_Id) REFERENCES MAL_Anime_Details(MAL_Id)
    );
    """

def insert_mal_anime_detail(data):
    """
    Returns tuple (query, values) necessary for inseting 
    data into the MAL_Anime_Details table.
    """

    query = """
    INSERT INTO MAL_Anime_Details 
    (
        MAL_Id, 
        Title, 
        AltNameEnglish,
        AltNameSynonyms,
        AltNameJapanese,
        Synopsis,
        MediaType,
        EpisodeCount,
        CurrentStatus,
        Aired,
        Premiered,
        Broadcast,
        Producers,
        Licensors,
        Studios,
        Source,
        Genres,
        Duration,
        Rating,
        PromoVideoSrc,
        PromoVideoBackgroundImageSrc,
        ImageSrc
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["MyAnimeListId"],
        data["Title"],
        data["AltNameEnglish"],
        data["AltNameSynonyms"],
        data["AltNameJapanese"],
        data["Synopsis"],
        data["MediaType"],
        data["EpisodeCount"],
        data["CurrentStatus"],
        data["Aired"],
        data["Premiered"],
        data["Broadcast"],
        data["Producers"],
        data["Licensors"],
        data["Studios"],
        data["Source"],
        data["Genres"],
        data["Duration"],
        data["Rating"],
        data["PromoVideo"],
        data["PromoVideoBackgroundImage"],
        data["ImageSrc"]
    )

    return query, values

def insert_mal_anime_detail_stats(data):
    """
    Returns tuple (query, values) necessary for inseting 
    data into the MAL_Anime_Detail_Stats table.
    """

    query = """
    INSERT INTO MAL_Anime_Detail_Stats
    (
        MAL_Id,
        Score,
        ScoredByCount,
        Ranked,
        Popularity,
        MembersCount,
        FavoritesCount
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["MyAnimeListId"],
        data["Score"],
        data["ScoredByCount"],
        data["Ranked"],
        data["Popularity"],
        data["MembersCount"],
        data["FavoritesCount"]
    )

    return query, values