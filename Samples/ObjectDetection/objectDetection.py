from ultralytics import YOLO
import cv2
from picamera2 import Picamera2
import math 

# start webcam
picam2 = Picamera2()
picam2.start()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# model
model = YOLO("yolo-Weights/yolov8n.pt")

# object classes
classNames = ["Clovek", "Kolo", "Auto", "Motorka", "Letadlo", "Autobus", "Vlak", "Nakladak", "Lod",
              "Semafor", "Hydrant", "Stop", "Automat", "Lavicka", "Ptak", "Kocka",
              "Pes", "Kun", "Ovce", "Krava", "Slon", "Medved", "Zebra", "Zirafa", "Batoh", "Destnik",
              "Kabelka", "Kravata", "Kufrik", "Litajici talir", "Lyze", "Snowboard", "Mic", "Drak", "Palka",
              "Rukavice", "Skateboard", "Prkno", "Raketa", "Flaska", "Sklenicka", "Hrnecek",
              "Vidlicka", "Nuz", "Lzicka", "Miska", "Banan", "Jabko", "Toast", "Pomik", "Fuj",
              "Mrkev", "Horky pes", "Pizza", "Donut", "Dort", "zidle", "Gauc", "Kytka", "Postel",
              "Stul", "Zachod", "Monitor", "Notebook", "Mys", "Ovladac", "Klavesnice", "Telefon",
              "Mikrovlnka", "Trouba", "Toastovac", "Drez", "Lednicka", "Knizka", "Hodiny", "Vaza", "Nuzky",
              "Medvidek", "Fen", "Kartacek"]


while True:
    frame = picam2.capture_array()

    # Convert to RGB (sRGB) if necessary
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = model(frame_rgb, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
             # confidence
            confidence = math.ceil((box.conf[0]*100))/100

            if confidence > 0.5:
                print("Confidence --->",confidence)
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                # put box in cam
                cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # class name
                cls = int(box.cls[0])
                print("Class name -->", classNames[cls])

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(frame_rgb, classNames[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', frame_rgb)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()