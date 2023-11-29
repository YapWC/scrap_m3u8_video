from lib import VideoFile
import requests
import sys
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
        os.makedirs(output_folder)

    video = VideoFile(args.video_link, args.name_file_as, args.output_folder)
    ts_video = video.download_video()
