import yt_dlp
from flask import Flask, render_template, request, send_file, redirect, url_for
import os

app = Flask(__name__)

# Directory where videos will be temporarily stored
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html', message=None)


@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    try:
        ydl_opts = {
            'format': 'best',  # Download the best available quality
            # Save with video title
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }

        # Use yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(video_url, download=True)
            video_path = ydl.prepare_filename(result)

        # Send the file to the user
        return send_file(video_path, as_attachment=True)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('index.html', message=error_message)


@app.route('/complete', methods=['GET'])
def download_complete():
    return render_template('index.html', message="Download Completed Successfully!")


if __name__ == "__main__":
    app.run(debug=True)
