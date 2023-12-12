from url import M3u8Url, Mp4Url, WebsiteUrl
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("video_link", help="The video link to download.")
parser.add_argument("output_folder", help="Example: ./video/")


"""
    Example 1: 
        python3 main.py "<the_link>" ./downloaded_video/ <name the file as you like>
"""
# if __name__=="__main__":
#     parser.add_argument("name_file_as", help="Name the downloaded file as.")
#     args = parser.parse_args()

#     if not os.path.exists(args.output_folder):
#         os.makedirs(args.output_folder)

#     video_link = M3u8Url(args.video_link)
#     video_link.video_instance.download(args.output_folder, args.name_file_as)

"""
    Example 2: (Help you get the title of the video based on the website)
        python3 main.py "<the_link>" ./downloaded_video/ "<website_link>"

"""
if __name__=="__main__":
    parser.add_argument("website_link", help="The url of the website")
    args = parser.parse_args()
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    website = WebsiteUrl(args.website_link)
    title = website.get_specific_html_content("title")
    video_link = M3u8Url(args.video_link)
    video_link.video_instance.download(args.output_folder, title)
