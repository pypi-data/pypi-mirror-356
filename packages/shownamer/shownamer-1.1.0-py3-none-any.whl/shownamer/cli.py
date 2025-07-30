import os
import re
import requests
import argparse
from collections import defaultdict

# Default supported video extensions
DEFAULT_EXTENSIONS = [".mkv", ".mp4", ".avi", ".mov", ".flv"]
TOOL_VERSION = "1.0.0"

# Enhanced filename pattern
FILENAME_PATTERN = re.compile(
    r"^(?P<show>.+?)[\s._-]*[Ss]?(?P<season>\d{1,2})?[Ee](?P<episode>\d{2})",
    re.IGNORECASE,
)

# Characters not allowed in filenames
INVALID_CHARS = r'\/:*?"<>|'


def sanitize_filename(name):
    """Remove or replace characters that are not allowed in filenames."""
    return "".join(c if c not in INVALID_CHARS else "_" for c in name)


def get_episode_title(show_name, season, episode):
    """Query TVmaze API for the episode title."""
    response = requests.get(
        "https://api.tvmaze.com/singlesearch/shows", params={"q": show_name}
    )
    if response.status_code != 200:
        return None
    show_data = response.json()
    show_id = show_data["id"]

    episode_response = requests.get(
        f"https://api.tvmaze.com/shows/{show_id}/episodebynumber",
        params={"season": season, "number": episode},
    )
    if episode_response.status_code != 200:
        return None
    return episode_response.json()["name"]


def list_series_summary(directory, extensions):
    """List all detected show names with season/episode counts."""
    stats = defaultdict(lambda: defaultdict(int))
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext.lower() not in extensions:
            continue
        match = FILENAME_PATTERN.match(name)
        if not match:
            continue
        show = match.group("show").strip()
        season_str = match.group("season")
        season = int(season_str) if season_str else 1
        stats[show][season] += 1

    if not stats:
        print("No recognizable TV show files found.")
        return

    print("Detected Series Summary:")
    for show, seasons in stats.items():
        print(f"  {show}:")
        for season, count in sorted(seasons.items()):
            print(f"    Season {season:02}: {count} episode(s)")


def rename_files(directory, extensions, dry_run=False, verbose=False, format_str=None):
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext.lower() not in extensions:
            continue

        match = FILENAME_PATTERN.match(name)
        if not match:
            if verbose:
                print(f"[skip] {filename}: doesn't match expected pattern")
            continue

        show = match.group("show").strip()
        season_str = match.group("season")
        season = int(season_str) if season_str else 1
        episode = int(match.group("episode"))

        episode_title = get_episode_title(show, season, episode)
        if not episode_title:
            print(f"[fail] {filename}: could not fetch episode title")
            continue

        safe_title = sanitize_filename(episode_title)

        if not format_str:
            format_str = "{name} S{season:02}E{episode:02} - {title}"

        try:
            new_basename = format_str.format(
                name=show, season=season, episode=episode, title=safe_title
            )
        except KeyError as e:
            print(f"[fail] Invalid format string key: {e}")
            continue

        new_filename = f"{new_basename}{ext}"
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_filename)

        if os.path.exists(dst):
            print(f"[skip] {new_filename} already exists")
            continue

        if dry_run:
            print(f"[dry-run] {filename} → {new_filename}")
        else:
            os.rename(src, dst)
            print(f"[renamed] {filename} → {new_filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Rename TV episode files by fetching episode titles from TVmaze."
    )
    parser.add_argument(
        "--dir",
        default=os.getcwd(),
        help="Directory containing video files (default: current directory)",
    )
    parser.add_argument(
        "--ext",
        nargs="*",
        default=DEFAULT_EXTENSIONS,
        help="List of allowed video file extensions (default: common types)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview renaming without making changes"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Show skipped files and debug info"
    )
    parser.add_argument(
        "--version", action="store_true", help="Show tool version and exit"
    )
    parser.add_argument(
        "--name", action="store_true", help="List show names and episode counts"
    )
    parser.add_argument(
        "--format",
        type=str,
        help='Custom output format using {name}, {season}, {episode}, {title} (default: "{name} S{season:02}E{episode:02} - {title}")',
    )

    args = parser.parse_args()

    extensions = [e if e.startswith(".") else "." + e for e in args.ext]

    if args.version:
        print(f"shownamer version {TOOL_VERSION}")
        return

    if args.name:
        list_series_summary(args.dir, extensions)
        return

    rename_files(
        directory=args.dir,
        extensions=extensions,
        dry_run=args.dry_run,
        verbose=args.verbose,
        format_str=args.format,
    )


if __name__ == "__main__":
    main()
