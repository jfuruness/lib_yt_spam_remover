import os
import pickle

from .downloader import Downloader

class Labeller:

    path = os.path.join(Downloader.data_dir, "comments.p")
 
    def __init__(self, comments):
        self.labelled_comments = self.load()
        self.unlabelled_comments = []
        for comment in comments:
            if comment.yt_id not in self.labelled_comments:
                self.unlabelled_comments.append(comment)

    def run(self):
        for i, comment in enumerate(self.unlabelled_comments):
            print(f"{i}/{len(self.unlabelled_comments)}")
            done = self._validate(comment)
            if done:
                self.dump()
                return
            for reply in comment.replies:
                done = self._validate(reply)
                if done:
                    self.dump()
                    return

    def _validate(self, comment):
        print(comment.__str__(replies=False))
        ans = "r"
        while "r" in ans:
            ans = input("Spam? y for yes. r for go back. d for done.").lower()
            if "d" in ans:
                return True
            elif "r" in ans:
                self._validation_regret()
                return self._validate(comment)
            elif "y" in ans:
                comment.spam = True
        self.labelled_comments[comment.yt_id] = comment
        return False

    def _validation_regret(self):
        # Get the last item added to the dictionary
        comment = [v for k, v in self.labelled_comments.items()][-1]
        print("You seemed to have regretted your past action")
        print(comment)
        ans = input("Spam? y for yes")
        if "y" in ans:
            comment.spam = True
        else:
            comment.spam = False

    def dump(self):
        with open(self.path, "wb") as f:
            pickle.dump(self.labelled_comments, f)

    def load(self):
        try:
            with open(Labeller.path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return dict()
