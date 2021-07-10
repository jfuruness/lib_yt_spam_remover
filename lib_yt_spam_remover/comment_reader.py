import json
import logging
import os

from tqdm import tqdm

from .comment import TopLevelComment, Reply
from .downloader import Downloader


class CommentReader:
    """Reads the comments and saves them"""

    def run(self):
        """Parses all comments that were downloaded"""

        top_level_comments = []
        fnames = os.listdir(Downloader.data_dir)
        for fname in tqdm(fnames, total=len(fnames), desc="Reading comments"):
            if fname == self.path:
                continue
            else:
                with open(os.path.join(Downloader.data_dir, fname), "r") as f:
                    response = json.load(f)
                    for comment in response["items"]:
                        top_level_comments.append(TopLevelComment(comment))
        # Was going to save these, but this is so fast that there is no need
        return top_level_comments
