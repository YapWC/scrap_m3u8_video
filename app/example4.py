from src.url import M3u8Url, WebsiteUrl
from src.file import TextFile
from multiprocessing import Process, Queue
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("videos_url_file_path", help="The video link to download.")
parser.add_argument("websites_url_file_path", help="The url of the website")
parser.add_argument("output_folder", help="Example: ./video/")
args = parser.parse_args()


"""
    Example 4: Parse in 2 txt file that have the m3u8 videos and websites urls
                multiprocessing is being used in this case for faster download.
        python3 main.py "<videos_url_file_path>" "<websites_url_file_path> ./downloaded_video/"

"""


def parse_links(video_tasks):
    while video_tasks.empty() is False:
        task = video_tasks.get()
        website = WebsiteUrl(task[0])
        title = website.get_specific_html_content("h1")
        video_link = M3u8Url(task[1])
        video_link.video_instance.download(args.output_folder, title)


if __name__ == "__main__":
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    videos_url_file = TextFile(args.videos_url_file_path)
    websites_url_file = TextFile(args.websites_url_file_path)

    list_of_videos_link = videos_url_file.get_file_contents()
    list_of_websites_link = websites_url_file.get_file_contents()

    number_of_task = len(list_of_websites_link)
    number_of_processor = 2
    video_queue = Queue()
    process_list = []

    for i in range(number_of_task):
        video_queue.put([list_of_websites_link[i], list_of_videos_link[i]])

    for i in range(number_of_processor):
        process = Process(target=parse_links, args=(video_queue,))
        process_list.append(process)
        process.start()

    for process in process_list:
        process.join()
