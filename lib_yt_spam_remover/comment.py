import textwrap

class Comment:
    def __init__(self, raw: dict, parent=None):
        self.raw: dict = raw
        self.spam = None

    @property
    def yt_id(self):
        return self.raw["id"]

    @property
    def channel_id(self):
        return self.raw["snippet"]["authorChannelId"]["value"]

    @property
    def channel_name(self):
        return self.raw["snippet"]["authorDisplayName"]

    @property
    def image_url(self):
        return self.raw["snippet"]["authorProfileImageUrl"]

    @property
    def likes(self):
        return self.raw["snippet"]["likeCount"]

    @property
    def text(self):
        """Returns html text"""
        return self.raw["snippet"]["textDisplay"]

    @property
    def og_text(self):
        """Returns original text"""
        return self.raw["snippet"]["textOriginal"]

    def __str__(self, **kwargs):
        text_wrapped = textwrap.fill(self.og_text, 110)
        ogtext = ""
        for i, line in enumerate(text_wrapped.split("\n")):
            if i == 0:
                ogtext += line + "\n"
            else:
                ogtext += "\t        " + line + "\n"

        return (f"name: {self.channel_name}\n"
                f"\togtext: {ogtext}"
                f"\tlikes: {self.likes}")

class TopLevelComment(Comment):
    def __init__(self, yt_api_response):
        raw_top_level = yt_api_response["snippet"]["topLevelComment"]
        super(TopLevelComment, self).__init__(raw_top_level)

        self.replies = []
        if yt_api_response.get("replies"):
            for reply_raw in yt_api_response["replies"]["comments"]:
                self.replies.append(Reply(self, reply_raw))

    def __str__(self, replies=True):
        string = super(TopLevelComment, self).__str__()
        string += "\n"
        if replies:
            if self.replies:
                string += "\treplies:\n"
            for reply in self.replies:
                string += "\t\t" + str(reply).replace("\t", "\t\t\t") + "\n"
        return string

class Reply(Comment):
    def __init__(self, parent, raw):
        super(Reply, self).__init__(raw)
        self.parent = parent
