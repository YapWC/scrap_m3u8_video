from src.url import M3u8Url
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("video_link", help="The video link to download.")
parser.add_argument("output_folder", help="Example: ./video/")


"""
    Example 1: 
        python3 main.py "<the_link>" ./downloaded_video/ <name the file as you like>
"""
if __name__=="__main__":
    parser.add_argument("name_file_as", help="Name the downloaded file as.")
    args = parser.parse_args()

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    video_link = M3u8Url(args.video_link)
    video_link.video_instance.download(args.output_folder, args.name_file_as)
