import json
import os

import googleapiclient.discovery


class Downloader:
    # Limit per page
    request_limit_pp = 100
    data_dir = "/data"

    def __init__(self):
        err = f"Make {self.data_dir} with write permissions"
        assert os.path.exists(self.data_dir), err

        api_service_name = "youtube"
        api_version = "v3"
        try:
            key = os.environ["DEVELOPER_KEY"]
        except KeyError:
            key = input("DEVELOPER_KEY was not found in your env vars."
                        " Please enter now: ")

        self.yt = googleapiclient.discovery.build(api_service_name,
                                                  api_version,
                                                  DeveloperKey=key)

    def run(self, video_id="lU1qpBwQFmc", num_comments=1000):
        # Next page token is none since we are on the first page
        page_token = None
        # Iterate over all the pages and download the JSON
        for page_num in range(num_comments // self.request_limit_pp):
            page_token = self._download(page_num,
                                        video_id,
                                        page_token=page_token)

    def _download(self, page_num, video_id, page_token=None): 
        kwargs = {"part": "replies, snippet",
                  "maxResults": self.request_limit_pp,
                  "order": "relevance",
                  "videoId": video_id}
        # https://towardsdatascience.com/
        # how-to-build-your-own-dataset-of-youtube-comments-39a1e57aade
        # Get the next page since we are limited to 100 results per page
        if page_token:
            kwargs["pageToken"] = page_token

        # Get the request/response
        request = self.yt.commentThreads().list(**kwargs)
        response = request.execute()
        # Save the response
        path = os.path.join(self.data_dir, f"{video_id}_page_{page_num}.json")
        with open(path, "w") as f:
            json.dump(response, f)

        return response.get("next_page_token")
