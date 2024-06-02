import numpy as np
import cv2 as cv
import joblib
import requests

score_threshold = 0.9
nms_threshold = 0.3
top_k = 5000

svc = joblib.load('./svm_model.pkl')
mydict = ['Anh Khoa', 'Minh Duc' ,'Thanh Loi']
result = None
result_temp = '' 
url = 'https://sgp1.blynk.cloud/external/api/update?token=uEXyRDz6wti8V6F3l7RTndWJI3yHzSlx&V0='
result_rq = '0'

def visualize(input, faces, fps, thickness=2):
    global result_temp, result
    if faces[1] is not None:
        for idx, face in enumerate(faces[1]):
            #print('Face {}, top-left coordinates: ({:.0f}, {:.0f}), box width: {:.0f}, box height {:.0f}, score: {:.2f}'.format(idx, face[0], face[1], face[2], face[3], face[-1]))
            coords = face[:-1].astype(np.int32)
            #print(coords[2]*coords[3])
            if face[-1] >= 0.92 and coords[2]*coords[3]>=20000:
                cv.putText(frame,result,(coords[0], coords[1]- 5),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv.rectangle(input, (coords[0], coords[1]), (coords[0]+coords[2], coords[1]+coords[3]), (0, 255, 0), thickness)
                cv.circle(input, (coords[4], coords[5]), 2, (255, 0, 0), thickness)
                cv.circle(input, (coords[6], coords[7]), 2, (0, 0, 255), thickness)
                cv.circle(input, (coords[8], coords[9]), 2, (0, 255, 0), thickness)
                cv.circle(input, (coords[10], coords[11]), 2, (255, 0, 255), thickness)
                cv.circle(input, (coords[12], coords[13]), 2, (0, 255, 255), thickness)
            else: 
                result = ''
    else:
        result = ''  
    cv.putText(input, 'FPS: {:.2f}'.format(fps), (1, 16), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)       
    if result_temp == result:
        return;
    else: 
        if result == 'Anh Khoa':
            result_rq='1'
        elif result == 'Minh Duc':
            result_rq='2'
        elif result == 'Thanh Loi':
            result_rq='3' 
        else: 
            result_rq='0'
        #print(url + result_rq)
        requests.get(url + result_rq)   


if __name__ == '__main__':
    detector = cv.FaceDetectorYN.create(
        "./face_detection_yunet_2023mar.onnx",
        "",
        (320, 320),
        score_threshold,
        nms_threshold,
        top_k
    )
    recognizer = cv.FaceRecognizerSF.create(
    "./face_recogniti0002on_sface_2021dec.onnx","")

    tm = cv.TickMeter()

    cap = cv.VideoCapture(0)
    frameWidth = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    detector.setInputSize([frameWidth, frameHeight])

    result = 'None'
    while True:
        hasFrame, frame = cap.read()
        if not hasFrame:
            print('No frames grabbed!')
            break

        # Inference
        tm.start()
        faces = detector.detect(frame) # faces is a tuple
        tm.stop()
        
        key = cv.waitKey(1)
        if key == 27:
            break
        if faces[1] is not None:
            face_align = recognizer.alignCrop(frame, faces[1][0])
            face_feature = recognizer.feature(face_align)
            test_predict = svc.predict(face_feature)
            result = mydict[test_predict[0]]

        # Draw results on the input image
        visualize(frame, faces, tm.getFPS())
        result_temp = result

        # Visualize results
        cv.imshow('Live', frame)
        
    cv.destroyAllWindows()
