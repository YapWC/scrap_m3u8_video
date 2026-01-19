"""This module suppose to deal with any data type (photo, video, text, etc.) and format (raw, mp4, etc.)"""


class Data:
    """Base class for any kind of data like photo, video, text, etc"""
    def __init__(self, data, title) -> None:
        """

        Args:
            data (object): The data content in any format
        """
        self.data = data
        self.title = title


class VideoData(Data):
    """Parent class for video data receive in any format but return in .mp4 format"""
    name_extension = ".mp4"

    def __init__(self, data, title):
        """

        Args:
            data (object): The data content in any format
        """
        super().__init__(data, title)

    def download(self, output_folder_path, title):
        """Write the data into a file format."""
        if title is None:
            title = self.title
        
        with open(f"{output_folder_path}{title}{self.name_extension}", "wb") as file:
            # If data is one big byte object, write it directly
            if isinstance(self.data, (bytes, bytearray)):
                file.write(self.data)
            # If data is a list/generator of chunks
            else:
                for chunk in self.data:
                    file.write(chunk)

        print("%s%s | Downloaded " % (title, self.name_extension))
