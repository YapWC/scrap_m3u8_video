"""This module deal with url requests manipulation"""

import requests
import m3u8
import time
from bs4 import BeautifulSoup
from .data import VideoData
from alive_progress import alive_bar
from pathlib import Path

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
}


class Url:
    """Base class for url"""

    def __init__(self, url) -> None:
        """

        Args:
            url (str): The target url
        """
        self.url = url
        self.title = self.get_title()
        self.response = self.get_response(url, self.__class__.__name__)

    @staticmethod
    def get_response(url, class_name):
        """

        Args:
            url (str): The target url
            class_name(str): The name of the current associated base class

        Return:
            list: The response of the target url
        """
        while True:
            try:
                response = requests.get(url, headers=headers, timeout=5)
                # response.raise_for_status()
                print(
                    "Request Successful for %s with Status Code: %s"
                    % (class_name, response.status_code)
                )
            except requests.exceptions.ConnectionError as e:
                print("Request Fail for %s with Status Code: %s" % (class_name, e))
                wait_for_connection = 30
                print(f"Retrying to Connect in {wait_for_connection} seconds")
                time.sleep(wait_for_connection)
                continue
            except requests.exceptions.RequestException as e:
                print("Request Fail for %s with Status Code: %s" % (class_name, e))
            break
        return response

    def get_base_url(self):
        """

        Returns:
            str: The parent/base or the prefix of the url
        """
        split_original_url = self.url.split("/")
        new_url = split_original_url[0:-1]
        base_url = "/".join(new_url)
        return base_url

    def get_title(self):
        filename_without_extension = Path(self.url).stem
        return filename_without_extension


class Mp4Url(Url):
    """Target mp4 url"""

    extension = ".mp4"

    def __init__(self, url) -> None:
        """

        Args:
            url (str): The target url for video with mp4 format
        """
        super().__init__(url)
        self.data = VideoData(self.response)


class M3u8Url(Url):
    """Target m3u8 url"""

    extension = ".m3u8"
    video_key_in_m3u8_file = ["playlists", "media", "segments"]

    def __init__(self, url) -> None:
        """

        Args:
            url (str): The target url for video with m3u8 format
        """
        super().__init__(url)
        self.metadata = self.__get_metadata()
        self.ts_video_binary_contents = self.__get_ts_contents()
        self.data = VideoData(self.ts_video_binary_contents)

    def __get_metadata(self):
        """

        Returns:
            str: Metadata of the m3u8 video file
        """
        m3u8_master = m3u8.loads(self.response.text)
        metadata = m3u8_master.data
        return metadata

    def __get_ts_contents(self):
        """To extract the video data from ts files that was stored in m3u8 file

        Returns:
            list: The content of the video data in ts files
        """
        for key in self.video_key_in_m3u8_file:
            specific_metadata = self.metadata[key]
            if specific_metadata:
                print("More Links found in m3u8 %s", key)
                # First link are always connected to the highest resolution video
                first_data_link = specific_metadata[0]["uri"]
                if self.check_if_word_exist_in_the_link(first_data_link, "https"):
                    response = self.get_response(
                        first_data_link, self.__class__.__name__
                    )
                    return [response.content]
                elif self.check_if_word_exist_in_the_link(
                    first_data_link, self.extension
                ):
                    # if instead .m3u8 was found in the link then we need to dig deeper for ts video link/uri
                    base_url = self.get_base_url()
                    new_url = "/".join([base_url, first_data_link])
                    # Use the new url whenever we found a new url path
                    new_instance = M3u8Url(new_url)
                    # When ts is found then we return its contents
                    return new_instance.ts_video_binary_contents
                elif self.check_if_word_exist_in_the_link(first_data_link, ".ts"):
                    contents = []
                    with alive_bar(len(specific_metadata), title="Downloading") as bar:
                        for segments in specific_metadata:
                            ts_url = "/".join([self.get_base_url(), segments["uri"]])
                            ts = TsUrl(ts_url)
                            contents.append(ts.video_binary_data)
                            bar()
                    return contents
                else:
                    raise Exception("No link found")

    @staticmethod
    def check_if_word_exist_in_the_link(link, word_to_search_for):
        """To find if certain keyword exist in the link

        Returns:
            bool: Whether if keyword exist or not
        """
        position = link.find(word_to_search_for)
        if position != -1:  # If position == -1 then word does not exist
            return True
        else:
            return False


class TsUrl(Url):
    """Target ts url file"""

    def __init__(self, url) -> None:
        """

        Args:
            url (str): The target url for ts file
        """
        super().__init__(url)
        self.video_binary_data = self.response.content


class WebsiteUrl(Url):
    """For website url"""

    def __init__(self, url) -> None:
        """

        Args:
            url (str): The target url for website
        """
        super().__init__(url)
        self.html = self.__get_html()

    def __get_html(self):
        return BeautifulSoup(self.response.text, "html.parser")

    def get_specific_html_content(self, element, attribute=None, value=None):
        """

        Args:
            element (str): The html element
            attribute (str): The attribute of the html element
            value (str): The value of the element attribute

        Returns:
            str: The content of the html element
        """
        top_level_element = self.html.find(element, {attribute: value})
        next_lower_element = top_level_element.next_element
        return next_lower_element.contents[0]
