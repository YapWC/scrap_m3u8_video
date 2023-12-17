class File:
    def __init__(self, path) -> None:
        self.path = path
        self.name = self.get_filename()
    
    def get_filename(self):
        splitted_text = self.path.split("/")
        file_name = splitted_text[-1]
        return file_name


class TextFile(File):
    def __init__(self, path) -> None:
        super().__init__(path)
    

    def get_file_contents(self):
        """
        Reads a file line by line using a while loop.

        Args:
            filename: The path to the file to read.

        Returns:
            A list of lines in the file.
        """
        lines = []

        # Open the file in read mode
        with open(self.path, "r") as f:
            # Loop through each line in the file
            while line := f.readline():
                # Strip any trailing newline characters
                line = line.strip()
                print(line)

                # Add the line to the list
                lines.append(line)

        # Return the list of lines
        return lines
