from argparse import ArgumentParser, Namespace

from .baseclass import BaseProvider
from .baseclass.downloader import BaseDownloadHandler
from .pakete.sammelpaket import Sammelpaket
from .utils.db import ProDB
from .utils.threader import MultiThreader

from .utils.logger import enable_console_log
enable_console_log()

args: Namespace | None = None


def download_sammelpaket(provider: BaseProvider, sammelpaket: Sammelpaket):
    print(f"Downloading {sammelpaket.titel}")
    download_handler = provider.get_downloader(sammelpaket)
    downloader = BaseDownloadHandler(download_handler)
    downloader.download()


def download_provider(provider: BaseProvider):
    with MultiThreader(max_threads=args.threads, ignore_exceptions=False) as threader:
        for sammelpaket in ProDB().sort_sammelpakete(provider.get_all()):
            if ProDB().already_downloaded(sammelpaket) and not args.update:
                continue

            threader.add_thread(download_sammelpaket, provider, sammelpaket)


def download_cli(provider: BaseProvider):
    arg_parser = ArgumentParser(description="Promediathek Downloader")
    arg_parser.add_argument('--list', default=False, action='store_true', help="List every Sammelpaket available.")
    arg_parser.add_argument('--update', default=False, action='store_true', help="Check every Video for new Video/Audio/Subtitles.")
    arg_parser.add_argument('--threads', default=1, type=int, help="Number of download threads to use, increases RAM usage.")
    arg_parser.add_argument('--download-id', default='', type=str, help="Download one specific Sammelpaket")

    global args
    args = arg_parser.parse_args()

    is_subscribed = provider.check_if_subscribed()
    if provider.listing_requires_subscription and not is_subscribed:
        print(f"You are not subscribed to {provider.name}.")
        exit(1)

    if args.list:
        for sammelpaket in ProDB().sort_sammelpakete(provider.get_all()):
            print(sammelpaket)
        exit(0)

    if not is_subscribed:
        print(f"You are not subscribed to {provider.name}.")
        exit(1)

    if not args.download_id:
        download_provider(provider)

    else:
        sammelpakete = provider.get_all()
        sammelpaket = {sammelpaket.id: sammelpaket for sammelpaket in sammelpakete}
        if args.download_id not in sammelpaket:
            print(f"Sammelpaket with id {args.download_id} not found.")
            exit(1)

        download_sammelpaket(provider, sammelpaket[args.download_id])
