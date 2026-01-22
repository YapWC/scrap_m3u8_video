"""This module suppose to deal with any data type (photo, video, text, etc.) and format (raw, mp4, etc.)"""


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
        if self.extension_type not in title:
            title = title + self.extension_type
        
        video_file_path = f"{output_folder_path}{title}"
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

    def __init__(self, data, extension):
        """

        Args:
            data (object): The data content in any format
        """
        super().__init__(data)
        self.extension_type = extension
