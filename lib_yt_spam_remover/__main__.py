from argparse import ArgumentParser
import logging

from .downloader import Downloader

def main():

    parser = ArgumentParser(description="Runs yt_spam_remover")
    parser.add_argument("--debug", default=False, action='store_true')
    parser.add_argument("--download", default=False, action='store_true')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                         format='%(asctime)s-%(levelname)s: %(message)s')

    if args.download:
        Downloader().run()
    else:
        parser.print_help()
