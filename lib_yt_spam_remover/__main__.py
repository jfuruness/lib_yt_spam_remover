from argparse import ArgumentParser
import logging

from .comment_reader import CommentReader
from .downloader import Downloader
from .labeller import Labeller

def main():

    parser = ArgumentParser(description="Runs yt_spam_remover")
    parser.add_argument("--debug", default=False, action='store_true')
    parser.add_argument("--download", default=False, action='store_true')
    parser.add_argument("--read", default=False, action='store_true')
    parser.add_argument("--label", default=False, action='store_true')
    parser.add_argument("--investigate", default=False, action="store_true")

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                         format='%(asctime)s-%(levelname)s: %(message)s')

    if args.download:
        Downloader().run()
    if args.read:
        CommentReader().run()
    if args.label:
        comments = CommentReader().run()
        Labeller(comments).run()
    if args.investigate:
        comments = CommentReader().run()
        labeller = Labeller(comments)
        for comment in labeller.labelled_comments.values():
            if comment.spam:
                input(comment)
    if not any([args.download, args.read, args.label, args.investigate]):
        parser.print_help()
