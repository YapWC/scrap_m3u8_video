class Data:
    def __init__(self, data) -> None:
        self.data = data

class VideoData(Data):
    name_extension = ".mp4"
    def __init__(self, data):
        super().__init__(data)

    def download(self, output_folder_path, title):
        with open(f"{output_folder_path}{title}{self.name_extension}", "wb") as file:
            for data in self.data:
                file.write(data)
        file.close()
        print("%s%s | Downloaded " % (title, self.name_extension))
