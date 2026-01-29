class TitleSummary:
    def __init__(
        self,
        id,
        title,
        year=None,
        overview=None,
        media_type=None,
        poster_path=None,
    ):
        self.id = id
        self.title = title
        self.year = year
        self.overview = overview
        self.media_type = media_type
        self.poster_path = poster_path


class TitleDetails:
    def __init__(
        self,
        id,
        title,
        year=None,
        overview=None,
        media_type=None,
        poster_path=None,
        genres=None,
        runtime=None,
    ):
        self.id = id
        self.title = title
        self.year = year
        self.overview = overview
        self.media_type = media_type
        self.poster_path = poster_path
        self.genres = genres or []
        self.runtime = runtime
