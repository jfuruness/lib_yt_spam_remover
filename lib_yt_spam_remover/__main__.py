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
        true_pos = false_pos = false_neg = true_neg = 0
        for comment in labeller.labelled_comments.values():
            if comment.ten_nums_next_to_each_other:
            #if (comment.ten_nums_next_to_each_other
            #    or comment.num_non_ascii > 5):
            #if comment.ten_nums_next_to_each_other or "!G" in comment.og_text:
            #if comment.num_numbers >= 10 and comment.num_not_numbers_letters > 10:
                if comment.spam:
                    true_pos += 1
                else:
                    false_pos += 1
                    input(comment)
            else:
                if comment.spam:
                    false_neg += 1
                    #from unidecode import unidecode
                    #input(comment)
                    #input(unidecode(str(comment)))
                else:
                    true_neg += 1
                
        print("true_pos", true_pos, "false_pos", false_pos, "true_neg", true_neg, "false_neg", false_neg)
        input(len(labeller.labelled_comments.values()))
    if not any([args.download, args.read, args.label, args.investigate]):
        parser.print_help()
