# importing the necessary packages
import cv2
import dlib
import numpy as np

# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
# Dlib shape predictor model path
MODEL_PATH = "../resource/lib/publicdata/models/shape_predictor_68_face_landmarks.dat"
# Load model
shape_predictor = dlib.shape_predictor(MODEL_PATH)

def smile_detector(imDlib):
    faces = detector(imDlib, 0)
    if len(faces):
        landmarks = shape_predictor(imDlib, faces[0])
    else:
        return False
    
    isSmiling = False
    
    landmarks = shape_predictor(imDlib, faces[0])
    
    # Get mouth corners (points 48 and 54 in 0-based index)
    left_mouth = (landmarks.part(48).x, landmarks.part(48).y)
    right_mouth = (landmarks.part(54).x, landmarks.part(54).y)
    lip_width = ((right_mouth[0] - left_mouth[0])**2 + (right_mouth[1] - left_mouth[1])**2) ** 0.5
    
    # Get jaw corners (points 0 and 16)
    left_jaw = (landmarks.part(0).x, landmarks.part(0).y)
    right_jaw = (landmarks.part(16).x, landmarks.part(16).y)
    jaw_width = ((right_jaw[0] - left_jaw[0])**2 + (right_jaw[1] - left_jaw[1])**2) ** 0.5
    
    # Calculate ratio and determine smile
    ratio = lip_width / jaw_width
    isSmiling = ratio > 0.3  # Threshold optimized for video input
    
    return isSmiling

# Initializing video capture object.
capture = cv2.VideoCapture("../resource/lib/publicdata/videos/smile.mp4")
if(False == capture.isOpened()):
    print("[ERROR] Video not opened properly")    

# Create a VideoWriter object
smileDetectionOut = cv2.VideoWriter("smileDetectionOutput.avi",
                                   cv2.VideoWriter_fourcc('M','J','P','G'),
                                   15,(int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), 
                                       int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    
frame_number = 0
smile_frames = []
while (True):
    # grab the next frame
    isGrabbed, frame = capture.read()
    if not isGrabbed:
        break
        
    imDlib = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_has_smile = smile_detector(imDlib)
    if (True == frame_has_smile):
        cv2.putText(frame, "Smiling :)", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)
        smile_frames.append(frame_number)
#         print("Smile detected in Frame# {}".format(frame_number))
    if frame_number % 50 == 0:
        print('\nProcessed {} frames'.format(frame_number))
        print("Smile detected in Frames: {}".format(smile_frames))
    # Write to VideoWriter
    smileDetectionOut.write(frame)
    
    frame_number += 1

capture.release()
smileDetectionOut.release()
