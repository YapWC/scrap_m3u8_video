from .src.url import Mp4Url
import argparse
import os

def download_video(video_link, name_file_as=None):
    """
    Downloads a video from the given link to the specified output folder.

    Args:
        video_link (str): The URL of the video to download.
        output_folder (str): The directory to save the downloaded video.
        name_file_as (str, optional): The name to save the file as. If None, uses the video title.
    """
    output_folder='./downloaded_video/'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = Mp4Url(video_link)
    video.data.download(output_folder, name_file_as or video.title)
    return video.title

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_link", help="The video link to download.")
    parser.add_argument("--name-file-as", dest="name_file_as", default=None, required=False, help="Name the downloaded file as.")
    args = parser.parse_args()

    """
    Example 1: 
        python3 video_downloader.py "<the_link>" --name-file-as custom_name
    """
    download_video(args.video_link, args.name_file_as)
