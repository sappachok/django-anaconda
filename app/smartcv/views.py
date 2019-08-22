from django.shortcuts import render
from smartcv.src import showvideo
from django.http import HttpResponse,StreamingHttpResponse
import cv2
from smartcv.src.kalman_multi import KalmanFilter_cv
import time

DISTANCE_THRESHOLD = 500 # max distance to satisfy tracker update
IOU_THRESHOLD = 0.09 # min IOU between detected and predicted point
FALSE_POSITIVE_THRESHOLD = 200 # max number of times to save the tracker
CASCADE = 'smartcv/src/model-haar/haarcascade_fullbody.xml'
count = 0
n = 20

class VideoCamera(object):
    def __init__(self):
        # self.video = cv2.VideoCapture(0)
        # self.video = cv2.VideoCapture('smartcv/src/test.mp4')
        self.video = cv2.VideoCapture('smartcv/src/street-music.mp4')
        self.start = time.time()
        self.tracker = FaceTracker()
        self.cascade = cv2.CascadeClassifier(CASCADE)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        detector = cv2.CascadeClassifier('smartcv/src/model-haar/haarcascade_fullbody.xml')        
        font = cv2.FONT_HERSHEY_SIMPLEX        
        color = (255,0,0)
        diff = time.time() - self.start
        ret,frame = self.video.read()

        image = frame.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = image[y:y+h, x:x+w]

            cv2.rectangle(image, (x,y), (x+w,y+h), color, 2)

        cv2.putText(image, "Time: {0}".format(diff), (20, 20), font, 0.6, color, thickness=2)        
        ret,jpeg = cv2.imencode('.jpg',image)
        # time.sleep(0.02)
        return jpeg.tobytes()
    
    def kalman_frame(self):
        font = cv2.FONT_HERSHEY_SIMPLEX        
        color = (255,0,0)
        diff = time.time() - self.start

        face_cascade = self.cascade
        reader = self.video
        tracker = self.tracker

        ret, frame = reader.read()
        image = frame.copy()
        
        if ret:
            # frame = cv2.resize(frame, (640, 360))
            # faces = face_cascade.detectMultiScale(frame, 1.3, 5)

            frame = cv2.resize(frame, (640, 360))
            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            tracker.update(faces)
            # tracker.check()
            # ids, points = tracker.get_coordinates()
            
            for (x, y, w, h) in faces:
                image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            '''    
            for idx, (x, y, w, h) in enumerate(points):
                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, str(ids[idx]), (x+10, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 2)
            cv2.imshow("Frame", frame)
            '''
            
        
        cv2.putText(image, "Time: {0}".format(diff), (20, 20), font, 0.6, color, thickness=2)        
        ret,jpeg = cv2.imencode('.jpg',image)
        # time.sleep(0.02)
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

def kalman_show(request):
    try:
        return StreamingHttpResponse(kalman_gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")        

def gen(camera):    
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def kalman_gen(camera):    
    while True:
        frame = camera.kalman_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')        

class Face(object):
    def __init__(self, face_id, point):
        self.id = face_id
        self.coordinates = [point]
        self.tracker = KalmanFilter_cv()
        self.nrof_pred = 0

    def add_coordinates(self, point):
        self.coordinates.append(point)

    def get_coordinate(self):
        return self.coordinates[-1]

    def update(self, point):
        self.nrof_pred = 0
        state = self.tracker.update(point)
        return state

    def predict(self):
        self.nrof_pred += 1
        state = self.tracker.predict()
        return state

class FaceTracker(object):
    def __init__(self):
        self.faces = []
        self.face_id = 0

    def update(self, points=[]):
        face_ids = []
        new_faces = []
        a = 0.09
        for point in points:
            scores = []
            
            for face in self.faces:
                
                if face.id in face_ids:
                    scores.append(1000)
                else:
                    pred_coord = face.tracker.predict()
                    a = bb_intersection_over_union(point, pred_coord)
                    '''
                    if bb_intersection_over_union(point, pred_coord) >= IOU_THRESHOLD:
                        pass
                        # pred_mid = get_midpoint(pred_coord)
                        #det_mid = get_midpoint(point)
                        #scores.append(get_distance(pred_mid, det_mid))
                    else:
                        pass
                        #scores.append(1000)
                    '''
                                    
            closest_point = np.amin(scores) if scores else 1000
            
            if closest_point <= DISTANCE_THRESHOLD: # add iou check as well
                idx = scores.index(closest_point)
                face_to_update = self.faces[idx].update(point)
                self.faces[idx].add_coordinates(face_to_update)
                face_ids.append(self.faces[idx].id)
            else:
                face = Face(self.face_id, point)
                face.tracker.update(face.coordinates[-1])
                self.face_id += 1
                new_faces.append(face)
        
        for face in self.faces:
            if face.id not in face_ids:
                pred = face.predict()
                face.add_coordinates(pred)

        self.faces.extend(new_faces)

    def check(self):
        to_del = []
        for face in self.faces:
            if face.nrof_pred == FALSE_POSITIVE_THRESHOLD:
                to_del.append(face)                
        for toX in to_del:
            self.faces.remove(toX)
    
    def get_coordinates(self):
        points = []
        ids = []
        for face in self.faces:
            ids.append(face.id)
            points.append(face.get_coordinate())
        return ids, points

def kalman():
    face_cascade = cv2.CascadeClassifier(CASCADE)
    reader = cv2.VideoCapture(0)
    tracker = FaceTracker()
    while True:
        ret, frame = reader.read()
        if ret:
            frame = cv2.resize(frame, (640, 360))
            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            tracker.update(faces)
            tracker.check()
            ids, points = tracker.get_coordinates()
            for (x, y, w, h) in faces:
                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            for idx, (x, y, w, h) in enumerate(points):
                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, str(ids[idx]), (x+10, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 2)
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    reader.release()
    cv2.destroyAllWindows()