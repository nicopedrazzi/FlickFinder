import requests
from models import TitleDetails, TitleSummary
from random import randint

class TMDBClient:
    def __init__(self, config):
        self.config = config
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {config.token}",
        }

    def search_title(self, query, media_type, language):
        endpoint = f"/search/{media_type}"
        data = self._request(
            endpoint,
            params={
                "query": query,
                "include_adult": "false",
                "language": language,
            },
        )
        results = data.get("results", [])
        return [self._to_summary(item, media_type) for item in results]

    def get_details(self, title_id, media_type, language):
        endpoint = f"/{media_type}/{title_id}"
        data = self._request(endpoint, params={"language": language})
        return self._to_details(data, media_type)

    def discover(
        self,
        media_type,
        genre_ids,
        provider_ids,
        region,
        language,
        page=None,
    ):
        params = {
            "language": language,
            "watch_region": region,
        }
        if page:
            params["page"] = page
        if genre_ids:
            params["with_genres"] = ",".join(str(gid) for gid in genre_ids)
        if provider_ids:
            params["with_watch_providers"] = ",".join(str(pid) for pid in provider_ids)
        data = self._request(f"/discover/{media_type}", params=params)
        results = data.get("results", [])
        return [self._to_summary(item, media_type) for item in results]

    def get_random_movies(self, language, media_type):
        endpoint = f"{media_type}/popular"
        params={
            "language":language,
            "page": randint(0,500)
        }
        data = self._request(endpoint,params=params)
        results = data.get("results",[])
        return [self._to_summary(item,media_type) for item in results]



    def list_genres(self, media_type, language):
        data = self._request(f"/genre/{media_type}/list", params={"language": language})
        genres = data.get("genres", [])
        return {genre["name"].lower(): genre["id"] for genre in genres}

    def list_watch_providers(self, media_type, region):
        data = self._request(f"/watch/providers/{media_type}", params={"watch_region": region})
        providers = data.get("results", [])
        return {provider["provider_name"].lower(): provider["provider_id"] for provider in providers}

    def _request(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params, timeout=20)
        response.raise_for_status()
        return response.json()

    def _to_summary(self, item, media_type):
        title_key = "title" if media_type == "movie" else "name"
        date_key = "release_date" if media_type == "movie" else "first_air_date"
        year = None
        if item.get(date_key):
            year = item[date_key].split("-")[0]
        return TitleSummary(
            id=item.get("id"),
            title=item.get(title_key) or "Untitled",
            year=year,
            overview=item.get("overview"),
            media_type=media_type,
            poster_path=item.get("poster_path"),
        )

    def _to_details(self, item, media_type):
        title_key = "title" if media_type == "movie" else "name"
        date_key = "release_date" if media_type == "movie" else "first_air_date"
        year = None
        if item.get(date_key):
            year = item[date_key].split("-")[0]
        genres = [g.get("name") for g in item.get("genres", []) if g.get("name")]
        runtime = item.get("runtime")
        return TitleDetails(
            id=item.get("id"),
            title=item.get(title_key) or "Untitled",
            year=year,
            overview=item.get("overview"),
            media_type=media_type,
            poster_path=item.get("poster_path"),
            genres=genres,
            runtime=runtime,
        )
