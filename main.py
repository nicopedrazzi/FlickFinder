import argparse
import sys

from config import load_config
from render import format_details, format_summary_list
from services import discover_flow, fetch_details, search_summaries

def run_search(args):
    try:
        config = load_config(language=args.language)
        summaries = search_summaries(config, title=args.title, media_type=args.media_type)
    except ValueError as exc:
        print(str(exc))
        return 1
    if not summaries:
        print("No results found.")
        return 0
    print(format_summary_list(summaries))
    if len(summaries) == 1:
        choice = 1
    else:
        try:
            choice = int(input("Pick a number: ").strip())
        except ValueError:
            print("Invalid selection.")
            return 1
    if choice < 1 or choice > len(summaries):
        print("Invalid selection.")
        return 1
    try:
        details = fetch_details(
            config,
            summaries=summaries,
            media_type=args.media_type,
            pick_index=choice - 1,
        )
    except ValueError as exc:
        print(str(exc))
        return 1
    print(format_details(details))
    return 0


def run_discover(args):
    try:
        config = load_config(language=args.language, region=args.region)
        results = discover_flow(
            config,
            media_type=args.media_type,
            genre_name=args.genre,
            provider_name=args.provider,
        )
    except ValueError as exc:
        print(str(exc))
        return 1
    if not results:
        print("No results found.")
        return 0
    print(format_summary_list(results))
    u_input = int(input("Pick a number: ").strip())
    try:
        args.title = results[u_input-1].title
        run_search(args)
        return 0
    except ValueError as e:
        return e



def build_parser():
    parser = argparse.ArgumentParser(prog="flickfinder")
    subparsers = parser.add_subparsers(dest="command")

    search_parser = subparsers.add_parser("search", help="Search movies or TV")
    search_parser.add_argument("title", help="Movie or TV title to search")
    search_parser.add_argument(
        "--type",
        dest="media_type",
        default="movie",
        choices=["movie", "tv"],
        help="movie or tv",
    )
    search_parser.add_argument("--language", help="Language, e.g. en-US")

    discover_parser = subparsers.add_parser("discover", help="Discover movies or TV")
    discover_parser.add_argument(
        "--type",
        dest="media_type",
        default="movie",
        choices=["movie", "tv"],
        help="movie or tv",
    )
    discover_parser.add_argument("--genre", help="Genre name")
    discover_parser.add_argument("--provider", help="Streaming provider")
    discover_parser.add_argument("--region", help="Country code, e.g. US")
    discover_parser.add_argument("--language", help="Language, e.g. en-US")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0
    if args.command == "search":
        return run_search(args)
    if args.command == "discover":
        return run_discover(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
