from flask import Flask,render_template,Response
import cv2

app=Flask(__name__)


camera=cv2.VideoCapture(0)
def generate_frames():
    while True:
        success, frame = camera.read()  # success returns True if the camera is reading properly
        if not success:
            break
        else:
            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()  # Convert the buffer to bytes
            
            # Yield the image as a byte stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
     return render_template('index.html')


@app.route('/video')
def video():
     return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame' ) # this function we will define and it return response to index.html and we need to set mimetype it is some kind of information we need to pass 



if __name__=="__main__":
     app.run(debug=True)