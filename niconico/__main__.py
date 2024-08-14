"""Main module for niconico package."""

import argparse
import logging
from pathlib import Path

from niconico import NicoNico, __version__
from niconico.exceptions import LoginFailureError, WatchAPIError


def command_details(args: argparse.Namespace) -> None:
    """Show video details."""
    logging.debug("Starting command: details with args: %s", args)
    client = NicoNico()
    video = client.video.get_video(args.id)
    if video is None:
        logging.error("Video not found")
        return
    logging.debug("Video: %s", video)
    if args.output is None:
        logging.info(video.model_dump_json(indent=2, by_alias=True))
    else:
        with args.output.open("w") as f:
            f.write(video.model_dump_json(by_alias=True))
        logging.info("Saved to %s", args.output)


def command_quality(args: argparse.Namespace) -> None:
    """Show video quality."""
    logging.debug("Starting command: quality with args: %s", args)
    client = NicoNico()
    if args.session is not None:
        try:
            client.login_with_session(args.session)
            logging.debug("Logged in with session")
        except LoginFailureError:
            logging.exception("Login failed")
        logging.debug("is_premium: %s", client.premium)
    try:
        watch_data = client.video.watch.get_watch_data(args.id)
    except WatchAPIError:
        logging.exception("An error has occurred")
        return
    logging.debug("Watch data: %s", watch_data)
    outputs = client.video.watch.get_outputs(watch_data)
    logging.info("Label\tVideo, Audio")
    for output_key, output in outputs.items():
        logging.info("%s:\t%s", output_key, ", ".join(output))


def command_download(args: argparse.Namespace) -> None:
    """Download video."""
    logging.debug("Starting command: download with args: %s", args)
    client = NicoNico()
    if args.session is not None:
        try:
            client.login_with_session(args.session)
            logging.debug("Logged in with session")
        except LoginFailureError:
            logging.exception("Login failed")
        logging.debug("is_premium: %s", client.premium)
    try:
        watch_data = client.video.watch.get_watch_data(args.id)
    except WatchAPIError:
        logging.exception("An error has occurred")
        return
    logging.debug("Watch data: %s", watch_data)
    outputs = client.video.watch.get_outputs(watch_data)
    logging.debug("Outputs: %s", outputs)
    if args.quality is not None:
        if args.quality not in outputs:
            logging.error("This quality is not supported")
            return
        quality = args.quality
        logging.debug("Selected quality: %s", quality)
    else:
        quality = next(iter(outputs))
        logging.debug("Selected quality: %s(best)", quality)
    logging.debug("Downloading video...")
    downloaded_path = client.video.watch.download_video(watch_data, quality, args.output)
    logging.info("Downloaded to %s", downloaded_path)


def main() -> None:
    """Main function for niconico package."""
    parser = argparse.ArgumentParser(
        description="download video from niconico",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--debug", help="enable debug logging", action="store_true")

    subparsers = parser.add_subparsers(title="commands")

    parser_details = subparsers.add_parser("details", help="show video details")
    parser_details.add_argument("id", help="video id", type=str)
    parser_details.add_argument("-o", "--output", help="output file (default: stdout)", default=None, type=Path)
    parser_details.set_defaults(func=command_details)

    parser_quality = subparsers.add_parser("quality", help="show video quality")
    parser_quality.add_argument("id", help="video id", type=str)
    parser_quality.add_argument("-s", "--session", help="user_session cookie", default=None, type=str)
    parser_quality.set_defaults(func=command_quality)

    parser_download = subparsers.add_parser("download", help="download video")
    parser_download.add_argument("id", help="video id", type=str)
    parser_download.add_argument("-o", "--output", help="output file (default: stdout)", default=".", type=Path)
    parser_download.add_argument("-s", "--session", help="user_session cookie", default=None, type=str)
    parser_download.add_argument("-q", "--quality", help="video quality (default: best)", default=None, type=str)
    parser_download.set_defaults(func=command_download)

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format="%(message)s")

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
