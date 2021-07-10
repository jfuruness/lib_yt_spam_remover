from argparse import ArgumentParser

from .downloader import Downloader

def main():

    parser = ArgumentParser(description="Runs yt_spam_remover")
    parser.add_argument("--debug", default=False, action='store_true')
    parser.add_argument("--download", default=False, action='store_true')

    args = parser.parse_args()

    if args.download:
        Downloader().run()
    else:
        parser.print_help()
