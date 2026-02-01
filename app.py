from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "/tmp"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")

        unique_id = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOAD_DIR, unique_id + ".mp4")

        ydl_opts = {
            "outtmpl": output_path,
            "format": "mp4/best",
            "quiet": True,
            "noplaylist": True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return send_file(
                output_path,
                as_attachment=True,
                download_name="video.mp4"
            )

        except Exception as e:
            return f"Error: {str(e)}"

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
