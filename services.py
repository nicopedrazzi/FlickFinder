from tmdb_client import TMDBClient


def search_summaries(
    config,
    title,
    media_type,
):
    client = TMDBClient(config)
    summaries = client.search_title(title, media_type=media_type, language=config.language)
    return summaries[:5]


def fetch_details(
    config,
    summaries,
    media_type,
    pick_index=0,
):
    if not summaries:
        return None
    client = TMDBClient(config)
    pick_index = max(0, min(pick_index, len(summaries) - 1))
    picked = summaries[pick_index]
    return client.get_details(picked.id, media_type=media_type, language=config.language)


def discover_flow(
    config,
    media_type,
    genre_name,
    provider_name,
):
    client = TMDBClient(config)
    genre_ids = None
    if genre_name:
        genre_map = client.list_genres(media_type, language=config.language)
        genre_id = genre_map.get(genre_name.lower())
        if genre_id is None:
            raise ValueError(f"Unknown genre: {genre_name}")
        genre_ids = [genre_id]

    provider_ids = None
    if provider_name:
        provider_map = client.list_watch_providers(media_type, region=config.region)
        provider_id = provider_map.get(provider_name.lower())
        if provider_id is None:
            raise ValueError(f"Unknown provider: {provider_name}")
        provider_ids = [provider_id]

    results = client.discover(
        media_type=media_type,
        genre_ids=genre_ids,
        provider_ids=provider_ids,
        region=config.region,
        language=config.language,
    )
    return results[:10]
