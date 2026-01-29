from textwrap import fill

def format_summary_list(items):
    lines = []
    for index, item in enumerate(items, start=1):
        year = f" ({item.year})" if item.year else ""
        lines.append(f"{index}. {item.title}{year}")
    return "\n".join(lines)


def format_details(details):
    if details is None:
        return "No details available."
    year = f" ({details.year})" if details.year else ""
    lines = [f"{details.title}{year}"]
    if details.genres:
        lines.append(f"Genres: {', '.join(details.genres)}")
    if details.runtime:
        lines.append(f"Runtime: {details.runtime} min")
    if details.overview:
        lines.append(fill(details.overview, width=80))
    if details.poster_path:
        lines.append(f"Poster: https://image.tmdb.org/t/p/w500{details.poster_path}")
    return "\n".join(lines)
