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

    title = info.get("title")

    formats = []

    for f in info["formats"]:
        if f.get("height") and f.get("ext") == "mp4":
            formats.append({
                "format_id": f["format_id"],
                "resolution": f"{f['height']}p"
            })

    return render_template(
        "yt_preview.html",
        title=title,
        formats=formats,
        url=url
    )


# DOWNLOAD VIDEO
@app.route("/download_youtube", methods=["POST"])
def download_youtube():

    url = request.form["url"]
    format_id = request.form["format_id"]

    filename = str(uuid.uuid4()) + ".mp4"

    ydl_opts = {
        "format": format_id,
        "outtmpl": filename,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    response = send_file(filename, as_attachment=True)

    @response.call_on_close
    def cleanup():
        if os.path.exists(filename):
            os.remove(filename)

    return response

    @response.call_on_close
    def cleanup():
        if os.path.exists(filename):
            os.remove(filename)

    return response


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)