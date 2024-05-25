"""This module deal with reading the content of a file."""


class File:
    """Base class for any file"""
    def __init__(self, path) -> None:
        """

        Args:
            path (str): Path to the file ("/")
        """
        self.path = path
        self.name = self.get_filename()
    
    def get_filename(self):
        """

        Returns:
            str: name of the file
        """
        split_text = self.path.split("/")
        file_name = split_text[-1]
        return file_name


class TextFile(File):
    """Subclass for text file"""
    def __init__(self, path) -> None:
        """

        Args:
            path (str): Path to the text file
        """
        super().__init__(path)

    def get_file_contents(self):
        """Read the content of the text file line by line
        and store the texts

        Returns:
            list: lines of strings of the text file contents
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
