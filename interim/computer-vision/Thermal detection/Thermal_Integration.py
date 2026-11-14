# thermal_integration.py

from ultralytics import YOLO

# import your existing tracker functions
from Temp_tracker import detect_temperature_anomalies

# Load your already-trained YOLO model
model = YOLO("best.pt")


while True:

    # ------------------------------------------------
    # Get ONE thermal frame
    # ------------------------------------------------
    frame = get_thermal_frame()


    # ------------------------------------------------
    # Branch 1: YOLO
    # ------------------------------------------------
    results = model(frame, verbose=False)

    person_detected = False
    bird_detected = False

    for result in results:
        for box in result.boxes:

            class_id = int(box.cls[0])

            if class_id == 0:
                person_detected = True

            elif class_id == 1:
                bird_detected = True


    # ------------------------------------------------
    # Branch 2: EXISTING TEMPERATURE TRACKER
    # ------------------------------------------------
    thermal_anomaly = detect_temperature_anomalies(frame)


    # ------------------------------------------------
    # Combine outputs
    # ------------------------------------------------
    if person_detected:
        print("HAZARD: PERSON")

    elif bird_detected:
        print("HAZARD: BIRD")

    elif thermal_anomaly:
        print("HAZARD: UNKNOWN THERMAL ANOMALY")

    else:
        print("CLEAR")