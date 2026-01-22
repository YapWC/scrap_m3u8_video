"""This module suppose to deal with any data type (photo, video, text, etc.) and format (raw, mp4, etc.)"""

import os


class Data:
    """Base class for any kind of data like photo, video, text, etc"""

    def __init__(self, data) -> None:
        """

        Args:
            data (object): The data content in any format
        """
        self.data = data

    def download(self, output_folder_path, title):
        """Write the data into a file format."""

        video_file_path = f"{output_folder_path}{title}{self.output_file_format}"
        with open(video_file_path, "wb") as file:
            # If data is one big byte object, write it directly
            if isinstance(self.data, (bytes, bytearray)):
                file.write(self.data)
            # If data is a list/generator of chunks
            else:
                for chunk in self.data:
                    file.write(chunk)

        print("%s | Downloaded " % (title))
        return video_file_path


class VideoData(Data):
    """Parent class for video data receive in any format but return in .mp4 format"""

    output_file_format = ".mp4"

    def __init__(self, data):
        """

        Args:
            data (object): The data content in any format
        """
        super().__init__(data)

    def download(self, output_folder_path, title, remux=False):
        """Write the data into a file format."""

        full_filename = title + self.output_file_format

        video_file_path = output_folder_path + full_filename
        with open(video_file_path, "wb") as file:
            # If data is one big byte object, write it directly
            if isinstance(self.data, (bytes, bytearray)):
                file.write(self.data)
            # If data is a list/generator of chunks
            else:
                for chunk in self.data:
                    file.write(chunk)

        if remux:
            full_filename = title + "-remuxed" + self.output_file_format
            output_video_file_path = output_folder_path + full_filename

            self.__remux_ts_to_mp4(video_file_path, output_video_file_path)
            os.remove(video_file_path)

        print(f"{full_filename} | Downloaded ")
        return full_filename

    def __remux_ts_to_mp4(self, input, output):
        os.system(f"static_ffmpeg -i {input} -y -c copy {output}")
