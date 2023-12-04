from lib import M3u8VideoInformation
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("video_link", help="The video link to download.")
parser.add_argument("name_file_as", help="Name the downloaded file as.")
parser.add_argument("output_folder", help="Example: ./video/")
# the arguments given
args = parser.parse_args()

if __name__=="__main__":
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    video = M3u8VideoInformation(args.video_link, args.name_file_as)
    ts_video = video.download_video(args.output_folder)
