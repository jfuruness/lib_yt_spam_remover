import textwrap

class Comment:
    def __init__(self, raw: dict, parent=None):
        self.raw: dict = raw
        self.spam = None

#############################
# Properties related to API #
#############################

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

########################
# Properties we define #
########################

    @property
    def num_letters(self):
        """Number of letters in the text"""

        return sum(x.isalpha() for x in self.og_text)

    @property
    def num_numbers(self):
        """Number of numbers in the text"""

        return sum(x.isdigit() for x in self.og_text)

    @property
    def num_not_numbers_letters(self):
        """Number of chars that are not letters or numbers"""

        return sum(not (x.isdigit() or x.isalpha()) for x in self.og_text)

    @property
    def percent_letters_numbers(self):
        """Remove all spaces. letters + numbers / len"""

        normal_chars = self.num_letters + self.num_numbers
        return normal_chars / len(self.og_text.replace(" ", ""))

    @property
    def percent_letters(self):
        """Removes all spaces. letters / len"""
        return self.num_letters / len(self.og_text.replace(" ", ""))

    @property
    def num_non_ascii(self):
        
        return len(self.non_ascii)

    @property
    def non_ascii(self):
        ascii_safe = set(["’", "”", "“"])
        return "".join([x for x in self.og_text if (0 > ord(x) or 127 < ord(x)) and x not in ascii_safe])
        
    @property
    def ten_nums_next_to_each_other(self):
        """Strip everything but letters/nums. returns True if 10 in a row"""

        og_stripped = "".join(x for x in self.og_text
                              if (x.isdigit() or x.isalpha()))
        total_count_in_a_row = 0
        for c in og_stripped:
            if c.isdigit():
                total_count_in_a_row += 1
            else:
                total_count_in_a_row = 0

            if total_count_in_a_row >= 10:
                return True
        return False

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
