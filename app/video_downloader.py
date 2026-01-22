from .src.url import Mp4Url, M3u8Url
import argparse
import os


def download_video(video_link, name_file_as):
    """
    Downloads a video from the given link to the specified output folder.

    Args:
        video_link (str): The URL of the video to download.
        output_folder (str): The directory to save the downloaded video.
        name_file_as (str, optional): The name to save the file as. If None, uses the video title.
    """
    output_folder = "./downloaded_video/"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if ".mp4" in video_link:
        return __mp4_video_download(video_link, output_folder, name_file_as)
    elif ".m3u8" in video_link:
        return __m3u8_video_download(video_link, output_folder, name_file_as)
    else:
        raise "This file is not supported"


def __mp4_video_download(video_link, output_folder, name_file_as=None):
    video = Mp4Url(video_link)
    return video.data.download(output_folder, name_file_as or video.title)


def __m3u8_video_download(video_link, output_folder, name_file_as=None):
    print("Running m3u8 download.")
    video = M3u8Url(video_link)
    return video.data.download(output_folder, name_file_as or video.title, remux=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_link", help="The video link to download.")
    parser.add_argument(
        "--name-file-as",
        dest="name_file_as",
        required=False,
        help="Name the downloaded file as.",
    )
    args = parser.parse_args()

    """
    Example 1: 
        python3 video_downloader.py "<the_link>" --name-file-as custom_name

    Example Link for MP4: https://www.tourism.gov.my/videos/uploads/a1c8683c-367e-473a-a295-dcead096a4f7.mp4
    """
    download_video(args.video_link, args.name_file_as)
