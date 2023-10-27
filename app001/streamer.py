import time
import cv2
import imutils
import platform
import numpy as np
from threading import Thread
from queue import Queue
from tensorflow.keras.models import load_model
import mediapipe as mp
from datetime import datetime
now = datetime.now()
from app001.line_module import Line_module
from threading import Thread
import time

class Streamer :
    
    def __init__(self ):
        
        if cv2.ocl.haveOpenCL() :
            cv2.ocl.setUseOpenCL(True)
        print('OpenCL : ', cv2.ocl.haveOpenCL())
        self.model = load_model( './app001/model/model.h5')
        self.actions = ['fall','stand','walking','lie','sit']
        self.seq_length = 30
        
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        
        self.seq = []
        self.action_seq = []
        self.last_action = None
        
        self.capture = None
        self.thread = None
        self.width = 640
        self.height = 480
        self.stat = False
        self.current_time = time.time()
        self.preview_time = time.time()
        self.sec = 0
        self.Q = Queue(maxsize=128)
        self.started = False
        self.line_module = Line_module()
        self.count = 0
        
        self.th = Thread(target=self.countdown)
        self.th.daemon = True
        
    def run(self, src = 0 ) :
        
        self.stop()
    
        self.capture = cv2.VideoCapture( src )
            
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
         
        if self.thread is None :
            self.thread = Thread(target=self.update, args=())  
            self.thread.daemon = False
            self.thread.start()
            self.thread2 = Thread(target=self.process)
            self.thread2.daemon = True
            self.thread2.start()    
        
        self.started = True
        
    def process(self):
        count = 0
        queue = []
        while True:
            # print("실행중")
            img = self.read()
            
            img = cv2.flip(img, 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = self.pose.process(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            if result.pose_landmarks is not None:
                res = result.pose_landmarks
                joint = np.zeros((33, 4))
                for j, lm in enumerate(res.landmark):
                    joint[j] = [lm.x, lm.y, lm.z, lm.visibility]

                v1 = joint[[26,24,25,23,14,16,13,15], :3] # Parent joint
                v2 = joint[[28,26,27,25,12,14,11,13], :3] # Child joint
                v = v2 - v1 # [20, 3]
                # Normalize v
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                angle = np.arccos(np.einsum('nt,nt->n',
                        v[[0,2,5,7],:], 
                        v[[1,3,4,6],:] # [4,]15,]
                        )
                    )

                angle = np.degrees(angle) # Convert radian to degree

                # 벡터의 방향성
                if count == 0:
                    queue.append(joint[:,:3])
                pre_v = queue.pop()
                queue.append(joint[:, :3])
                new_v = joint[:,:3] - pre_v
                
                #벡터의 가속도 
                cur_time = float(datetime.now().strftime('%Y%m%d%H%M%S.%f'))
                if count== 0:
                    pre_time = cur_time-0.001
                speed = (joint[:,:3] - pre_v) / (cur_time-pre_time) # 현재 프레임의 속도
                pre_time = cur_time
                
                d = np.concatenate([joint[:].flatten(), new_v.flatten(),speed.flatten(),angle])
                d = np.nan_to_num(d)
                
                self.seq.append(d)

                self.mp_drawing.draw_landmarks(img, res, self.mp_pose.POSE_CONNECTIONS)

                if len(self.seq) < self.seq_length:
                    continue

                input_data = np.expand_dims(np.array(self.seq[-self.seq_length:], dtype=np.float32), axis=0)

                y_pred = self.model.predict(input_data).squeeze()

                i_pred = int(np.argmax(y_pred))
                conf = y_pred[i_pred]

                if conf < 0.8:   # 넘어지는 순간 정확도가 애매해지기 때문에 계속해서 continue 처리가 된다. continue 처리가 되면 새로운 이미지가 들어오기때문에 송출시에는 끊어지는 것 처럼 보인다.
                    continue

                
                action = self.actions[i_pred]
                self.action_seq.append(action)

                if len(self.action_seq) < 3:
                    # cv2.imshow('img',img)
                    continue

                this_action = '?'
                if self.action_seq[-1] == self.action_seq[-2] == self.action_seq[-3]:
                    this_action = action
                print(this_action)
                if this_action == "fall" and self.count == 0:
                    self.count = 1
                    self.line_module.send_msg()
                    self.th.start()
                           
    def countdown(self):
        for i in range(10):
            time.sleep(1)
        self.count = 0
              

    def stop(self):
        
        self.started = False
        
        if self.capture is not None :
            
            self.capture.release()
            self.clear()
            
    def update(self):
                    
        while True:

            if self.started :
                (grabbed, self.copy_frame) = self.capture.read()
                
                if grabbed : 
                    self.Q.put(self.copy_frame)
                          
    def clear(self):
        
        with self.Q.mutex:
            self.Q.queue.clear()
            
    def read(self):
        return self.Q.get()

    def blank(self):
        
        return np.ones(shape=[self.height, self.width, 3], dtype=np.uint8)
    
    def bytescode(self):
        
        if not self.capture.isOpened():
            
            frame = self.blank()

        else :
            
            # frame = self.read()
            frame = imutils.resize(self.copy_frame, width=int(self.width) )
            # frame = self.process(frame)
        
            if self.stat :  
                cv2.rectangle( frame, (0,0), (120,30), (0,0,0), -1)
                fps = 'FPS : ' + str(self.fps())
                cv2.putText  ( frame, fps, (10,20), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1, cv2.LINE_AA)
            
            
        return cv2.imencode('.jpg', frame )[1].tobytes()
    
    def fps(self):
        
        self.current_time = time.time()
        self.sec = self.current_time - self.preview_time
        self.preview_time = self.current_time
        
        if self.sec > 0 :
            fps = round(1/(self.sec),1)
            
        else :
            fps = 1
            
        return fps
                   
    def __exit__(self) :
        print( '* streamer class exit')
        self.capture.release()