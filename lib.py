import requests
import m3u8
import time
import math


video_key_in_m3u8_file = ["playlists", "media", "segments"]

class M3u8VideoInformation:
    def __init__(self, m3u8_link, file_name):
        self.file_name = file_name
        self.link = m3u8_link
        self.metadata = self.get_metadata()
        self.video_ts_uri_list = self.__get_complete_ts_uri()

    def get_metadata(self):
        try:
            response = requests.get(self.link)
            #response.raise_for_status()
            print("Request Metadata Succesful for %s with Status Code: %s" % (self.file_name, response.status_code))
            m3u8_master = m3u8.loads(response.text)
            metadata = m3u8_master.data
        except requests.exceptions.RequestException as e:
            print("Request Metadata Fail for %s with Status Code: %s" % (self.file_name, e))
            metadata = None
        
        return metadata
    
    def get_video(self, url):
        try:
            response = requests.get(url)
            #response.raise_for_status()
            print("Request Download Video Succesful with Status Code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Request Download Video Fail with Status Code:", e)
            response = None
        
        return response
    def __get_complete_ts_uri(self):
        for key in video_key_in_m3u8_file:
            if self.metadata[key]:
                if self.metadata[key][0]["uri"].find("https") != -1:
                    return [self.metadata[key][0]["uri"]]
                elif self.metadata[key][0]["uri"].find(".m3u8") != -1:
                    another_m3u8_url = self.__get_new_path_to_uri(self.metadata[key][0]["uri"])
                    self.link = another_m3u8_url
                    self.metadata = self.get_metadata()
                    #self.video_ts_uri_list = self.__get_complete_for_ts_uri()
                elif self.metadata[key][0]["uri"].find(".ts") != -1:
                    list_of_ts_uri = []
                    for segments in self.metadata[key]:
                        list_of_ts_uri.append(self.__get_new_path_to_uri(segments["uri"]))
                    return list_of_ts_uri
                else:
                    raise Exception("No link found")
    
    def __get_new_path_to_uri(self, extension_of_url):
        splitted_original_url = self.link.split("/")
        for index, text in enumerate(splitted_original_url):
            if ".m3u8" in text:
                # to exclude the text path that contain .m3u8
                restructured_url = "/".join(splitted_original_url[0:index])
        # to create a continous path to get the ts file
        return "/".join([restructured_url, extension_of_url])

    def download_video(self, output_folder_path):
        self.record_process_time(starting=True)
        list_binary_data = []
        for ts_uri in self.video_ts_uri_list:
            response = self.get_video(ts_uri)
            if response:
                self.video_in_ts_format = m3u8.loads(response.text)
                list_binary_data.append(response.content)
        with open(f"{output_folder_path}/{self.file_name}", "wb") as file:
            for data in list_binary_data:
                file.write(data)
        file.close()
                
        mins, seconds = self.record_process_time(starting=False)
        print("%s | Downloaded | %s mins %s seconds" % (self.file_name, mins, seconds))

    def record_process_time(self, starting=True):
        global start_time
        if starting == True:
            start_time = time.time()
        else:
            end_time = time.time()
            duration = (end_time - start_time)/60  # In second unit
            rounded_duration = duration
            fraction_in_minutes, minutes = math.modf(rounded_duration)
            seconds = round(fraction_in_minutes*60, 0)
            return minutes, seconds
