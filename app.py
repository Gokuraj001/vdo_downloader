from flask import Flask, render_template, request, send_file
import yt_dlp
import uuid
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# INSTAGRAM PREVIEW
@app.route("/preview", methods=["POST"])
def preview():

    url = request.form["url"]

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    video_url = info["url"]
    title = info.get("title", "Instagram Video")

    return render_template(
        "preview.html",
        video_url=video_url,
        title=title
    )


# YOUTUBE PREVIEW
@app.route("/youtube_preview", methods=["POST"])
def youtube_preview():

    url = request.form["yt_url"]

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    video_url = info["url"]
    title = info.get("title", "YouTube Video")

    return render_template(
        "preview.html",
        video_url=video_url,
        title=title
    )


# DOWNLOAD VIDEO
@app.route("/download", methods=["POST"])
def download():

    video_url = request.form["video_url"]

    filename = str(uuid.uuid4()) + ".mp4"

    ydl_opts = {
        "format": "best",
        "outtmpl": filename,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    response = send_file(filename, as_attachment=True)

    @response.call_on_close
    def cleanup():
        if os.path.exists(filename):
            os.remove(filename)

    return response


if __name__ == "__main__":
    app.run(debug=True)