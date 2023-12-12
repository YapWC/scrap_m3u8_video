import requests
import m3u8
from bs4 import BeautifulSoup
from data import VideoData

class Url:
    def __init__(self, url) -> None:
        self.url = url
        self.response = self.get_response(url, self.__class__.__name__)

    def get_response(self, url, class_name):
        try:
            response = requests.get(url)
            #response.raise_for_status()
            print("Request Succesful for %s with Status Code: %s" % (class_name, response.status_code))
        except requests.exceptions.RequestException as e:
            print("Request Fail for %s with Status Code: %s" % (class_name, e))
        
        return response
    
    def get_base_url(self):
        splitted_original_url = self.url.split("/")
        new_url = splitted_original_url[0:-1]
        base_url = "/".join(new_url)
        return base_url


class Mp4Url(Url):
    extension = ".mp4"

    def __init__(self, url) -> None:
        super().__init__(url)
        self.response = self.get_response(url, self.__class__.__name__)
        self.data = VideoData(self.response.content)


class M3u8Url(Url):
    extension = ".m3u8"
    video_key_in_m3u8_file = ["playlists", "media", "segments"]

    def __init__(self, url) -> None:
        super().__init__(url)
        self.response = self.get_response(url, self.__class__.__name__)
        self.metadata = self.__get_metadata()
        self.ts_video_binary_contents = self.__get_ts_contents()
        self.video_instance = VideoData(self.ts_video_binary_contents)
    
    def __get_metadata(self):
        m3u8_master = m3u8.loads(self.response.text)
        metadata = m3u8_master.data
        return metadata
    
    def __get_ts_contents(self):
        for key in self.video_key_in_m3u8_file:
            specific_metadata = self.metadata[key]
            if specific_metadata:
                # First link are always connected to the highest resolution video
                first_data_link = specific_metadata[0]["uri"]
                if self.check_if_word_exist_in_the_link(first_data_link, "https"):
                    response = self.get_response(first_data_link, self.__class__.__name__)
                    return [response.content]
                elif self.check_if_word_exist_in_the_link(first_data_link, self.extension):
                    # if instead .m3u8 was found in the link then we need to dig deeper for ts video link/uri
                    base_url = self.get_base_url()
                    new_url = "/".join([base_url, first_data_link])
                    self.__init__(new_url)
                elif self.check_if_word_exist_in_the_link(first_data_link, ".ts"):
                    contents = []
                    for segments in specific_metadata:
                        ts = TsUrl("/".join([self.get_base_url(), segments["uri"]]))
                        contents.append(ts.video_binary_data)     
                    return contents
                else:
                    raise Exception("No link found")
    
    def check_if_word_exist_in_the_link(self, link, word_to_search_for):
        position = link.find(word_to_search_for)
        if position != -1:
            return True
        else:
            return False
        
class TsUrl(Url):
    def __init__(self, url) -> None:
        super().__init__(url)
        self.response = self.get_response(url, self.__class__.__name__)
        self.video_binary_data = self.response.content

class WebsiteUrl(Url):
    def __init__(self, url) -> None:
        super().__init__(url)
        self.response = self.get_response(url, self.__class__.__name__)
        self.html = self.__get_html()
    
    def __get_html(self):
        return BeautifulSoup(self.response.text, 'html.parser')
    
    def get_specific_html_content(self, element, attribute=None):
        element_contents = self.html.find_all(element)
        if attribute:
            return [content.get(attribute) for content in element_contents]
        else:
            return [content.text for content in element_contents]
