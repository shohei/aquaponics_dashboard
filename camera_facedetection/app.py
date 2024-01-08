import cv2
from flask import Flask, render_template, Response

from camera import Camera

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"

@app.route("/stream2")
def stream2():
    return render_template("stream2.html")

def gen(camera):
    while True:
        frame = camera.get_frame()

        if frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

            #yield (b'--frame\r\n'
            #    b'Content-Type:image/jpeg\r\n'
            #    b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n'
            #    b'\r\n' + frame + b'\r\n')

        else:
            print("frame is none")

@app.route("/video_feed")
def video_feed():
    return Response(gen(Camera()),
            mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5001, threaded=True)
