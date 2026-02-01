from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid
from pathlib import Path

app = Flask(__name__)

# Use a relative folder instead of /tmp
DOWNLOAD_FOLDER = Path("downloads")
DOWNLOAD_FOLDER.mkdir(exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return "Please provide a valid URL.", 400

        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp4"
        filepath = DOWNLOAD_FOLDER / filename

        ydl_opts = {
            "outtmpl": str(filepath),
            "format": "best",
            "quiet": True,
            "noplaylist": True,  # Avoid playlist errors
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Send file to user
            return send_file(filepath, as_attachment=True)

        except yt_dlp.utils.DownloadError as e:
            return f"Download failed. Probably private or login required.\nDetails: {str(e)}", 400

        except Exception as e:
            return f"An unexpected error occurred: {str(e)}", 500

        finally:
            # Cleanup downloaded file after sending (optional)
            if filepath.exists():
                try:
                    os.remove(filepath)
                except:
                    pass

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
