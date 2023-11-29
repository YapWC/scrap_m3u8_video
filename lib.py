import requests
import m3u8
import time
import math

class VideoFile:
    def __init__(self, m3u8_link, video_name, output_folder_path):
        self.video_name = video_name
        self.link = m3u8_link
        self.metadata = self.get_metadata()
        self.output_folder_path = output_folder_path
        self.video_ts_uri = self.metadata["playlists"][0]["uri"]

    def get_metadata(self):
        try:
            response = requests.get(self.link)
            response.raise_for_status()
            print("Request Metadata Succesful with Status Code:", response.status_code)
            m3u8_master = m3u8.loads(response.text)
            metadata = m3u8_master.data
        except requests.exceptions.RequestException as e:
            print("Request Metadata Fail with Status Code:", e)
            metadata = None
        
        return metadata
    
    def get_video(self):
        try:
            response = requests.get(self.video_ts_uri)
            response.raise_for_status()
            print("Request Download Video Succesful with Status Code:", response.status_code)
        except requests.exceptions.MissingSchema as e:
            completed_url = self.get_missing_url()
            response = requests.get(completed_url)
            response.raise_for_status()
            print("Request Download Video Succesful with Status Code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Request Download Video Fail with Status Code:", e)
            response = None
        
        return response
    
    def get_missing_url(self):
        split_original_url = self.link.split("/")
        missing_url = "/".join(split_original_url[0:-1])
        complete_url = "/".join([missing_url, self.video_ts_uri])
        return complete_url

    def download_video(self):
        response = self.get_video()
        if response:
            video_in_ts_format = m3u8.loads(response.text)
            with open(f"{self.output_folder_path}/{self.video_name}", "wb") as file:
                self.record_process_time(starting=True)
                file.write(response.content)
            
            mins, seconds = self.record_process_time(starting=False)
            print("%s | Downloaded | %s mins %s seconds" % (self.video_name, mins, seconds))

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