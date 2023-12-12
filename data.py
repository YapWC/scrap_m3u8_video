import time
import math

class Data:
    def __init__(self, data) -> None:
        self.data= data

class VideoData(Data):
    name_extension = ".mp4"
    def __init__(self, data):
        super().__init__(data)

    def download(self, output_folder_path, title):
        self.record_process_time(starting=True)
        with open(f"{output_folder_path}/{title}{self.name_extension}", "wb") as file:
            for data in self.data:
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
