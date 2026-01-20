from flask import (
    Blueprint,
    render_template,
    request,
    send_file,
)
import os

from ..video_downloader import download_video

bp = Blueprint("routes", __name__)
DOWNLOAD_FOLDER = "downloaded_video"


@bp.route("/index", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        video_url = request.form["video-url"]
        filename = request.form["name-file-as"]
        title = download_video(video_url, filename)
        return render_template("index.html", video_file=title)

    return render_template("index.html")


@bp.route("/download/<filename>")
def download_file(filename):
    # Ensure the path is absolute and within the expected directory for security
    file_path = os.path.join(os.getcwd(), DOWNLOAD_FOLDER, filename)

    # Use send_file with as_attachment=True to prompt download
    return send_file(file_path, as_attachment=True)
