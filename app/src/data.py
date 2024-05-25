"""This module suppose to deal with any data type (photo, video, text, etc.) and format (raw, mp4, etc.)"""


class Data:
    """Base class for any kind of data like photo, video, text, etc"""
    def __init__(self, data) -> None:
        """

        Args:
            data (object): The data content in any format
        """
        self.data = data


class VideoData(Data):
    """Parent class for video data receive in any format but return in .mp4 format"""
    name_extension = ".mp4"

    def __init__(self, data):
        """

        Args:
            data (object): The data content in any format
        """
        super().__init__(data)

    def download(self, output_folder_path, title):
        """Write the data into a file format."""
        with open(f"{output_folder_path}{title}{self.name_extension}", "wb") as file:
            for data in self.data:
                file.write(data)
        file.close()
        print("%s%s | Downloaded " % (title, self.name_extension))
