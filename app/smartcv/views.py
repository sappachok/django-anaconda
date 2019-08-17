from django.shortcuts import render
from smartcv.src import showvideo
from django.http import HttpResponse,StreamingHttpResponse
import cv2
import time

class VideoCamera(object):
    def __init__(self):
        # self.video = cv2.VideoCapture(0)
        self.video = cv2.VideoCapture('smartcv/train.mp4')
    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret,image = self.video.read()
        ret,jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

# Create your views here.
def smartcv(request):
    # db_output = connectdb()
    showvideo.show()
    data = {'blog_title': 'Datasci App', 'get_project_url': 'getproject'}
    return render(request, 'index.html', data)

def show(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")

def gen(camera):    
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')