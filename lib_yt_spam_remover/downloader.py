import json
import logging
import os

import googleapiclient.discovery


class Downloader:
    """Downloads the JSON for youtube comment threads"""

    # Limit per page, set by the youtube API
    request_limit_pp = 100
    # Dir to save all the JSON files
    data_dir = "/data"

    def __init__(self):
        """Ensures data dir exists, ensures key exists, and inits yt API"""

        err = f"Make {self.data_dir} with write permissions"
        assert os.path.exists(self.data_dir), err

        api_service_name = "youtube"
        api_version = "v3"
        try:
            key = os.environ["DEVELOPER_KEY"]
        except KeyError:
            key = input("DEVELOPER_KEY was not found in your env vars."
                        " Please enter now: ")

        # Initialize youtube API
        self.yt = googleapiclient.discovery.build(api_service_name,
                                                  api_version,
                                                  developerKey=key)

    def run(self, video_id="lU1qpBwQFmc", num_comments=10000):
        """Downloads comment threads from a video"""

        # Next page token is none since we are on the first page
        page_token = None
        # Total number of comments to download:
        comments_left = num_comments
        # Iterate over all the pages and download the JSON
        while comments_left > 0:
            logging.info(f"Comments_left: {comments_left}")
            (page_token,
             comments_left) = self._download(video_id,
                                             comments_left=comments_left,
                                             page_token=page_token)

    def _download(self, video_id, page_token=None, comments_left=None):
        """Downloads the JSON for a particular request"""

        # Sets the max_results
        if comments_left > self.request_limit_pp:
            max_results = self.request_limit_pp
        else:
            max_results = comments_left

        # Kwargs for youtube API call
        kwargs = {"part": "replies, snippet",
                  "maxResults": max_results,
                  "order": "relevance",
                  "videoId": video_id}
        # https://towardsdatascience.com/
        # how-to-build-your-own-dataset-of-youtube-comments-39a1e57aade
        # Get the next page since we are limited to 100 results per page
        if page_token:
            kwargs["pageToken"] = page_token

        # Get the request/response from the youtube API
        request = self.yt.commentThreads().list(**kwargs)
        response = request.execute()
        # Save the response
        path = os.path.join(self.data_dir, f"{video_id}_{comments_left}.json")
        with open(path, "w") as f:
            json.dump(response, f)

        # Return the next page token and comments left
        return (response.get("nextPageToken"),
                comments_left - response["pageInfo"]["totalResults"])
