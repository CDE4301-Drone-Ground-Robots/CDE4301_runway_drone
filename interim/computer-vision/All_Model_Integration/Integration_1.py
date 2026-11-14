import cv2


from Patchcore_Detection import (
    detect_anomaly
)

from FOD_detection import (
    FODDetector
)

from Crack_Detection import (
    CrackDetector
)

from Thermal_Detection import (
    ThermalDetector
)


# ============================================================
# SETTINGS
# ============================================================

CAMERA_ID = 1

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720


# ============================================================
# MODEL PATHS
# ============================================================

YOLO_MODEL_PATH = (
    "C:/Users/Chara/OneDrive/Documents/YR4_SEM1/CDE4301/All_Model_Integration/FOD_yolo11s.pt"
)


CRACK_MODEL_PATH = (
    "C:/Users/Chara/OneDrive/Documents/YR4_SEM1/CDE4301/All_Model_Integration/best_crack_model.pth"
)


# ============================================================
# INITIALIZE DETECTORS
# ============================================================

print("\n========================================")
print("INITIALIZING UAV DETECTION SYSTEM")
print("========================================")


# ------------------------------------------------------------
# FOD YOLO
# ------------------------------------------------------------

fod_detector = FODDetector(
    model_path=YOLO_MODEL_PATH,
    confidence=0.30,
    device=0
)


print("FOD YOLO: READY")


# ------------------------------------------------------------
# Crack U-Net
# ------------------------------------------------------------

crack_detector = CrackDetector(
    model_path=CRACK_MODEL_PATH,
    image_size=512,
    threshold=0.5
)


print("Crack detector: READY")


# ------------------------------------------------------------
# Thermal
# ------------------------------------------------------------

thermal_detector = ThermalDetector()


# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(
    CAMERA_ID
)


cap.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    FRAME_WIDTH
)


cap.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    FRAME_HEIGHT
)


if not cap.isOpened():

    print(
        "ERROR: Could not open camera."
    )

    exit()


print("\nCamera: READY")

print("\nControls:")
print("1 → Simulate thermal obstacle")
print("q → Quit")


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    # --------------------------------------------------------
    # Read frame
    # --------------------------------------------------------

    ret, frame = cap.read()


    if not ret:

        print(
            "ERROR: Failed to read frame."
        )

        break


    frame_height, frame_width = (
        frame.shape[:2]
    )


    # ========================================================
    # CAMERA CENTRE
    # ========================================================

    camera_center_x = (
        frame_width // 2
    )

    camera_center_y = (
        frame_height // 2
    )


    # Draw camera centre

    cv2.circle(
        frame,
        (
            camera_center_x,
            camera_center_y
        ),
        6,
        (0, 255, 0),
        -1
    )


    # ========================================================
    # THERMAL MONITORING
    # ========================================================

    key = cv2.waitKey(1) & 0xFF


    thermal_obstacle = (
        thermal_detector.check(
            key
        )
    )


    # --------------------------------------------------------
    # THERMAL OBSTACLE
    # --------------------------------------------------------

    if thermal_obstacle:

        print("\n========================================")
        print("THERMAL OUTPUT: OBSTACLE")
        print("CEASING OPERATIONS")
        print("========================================")

        break


    # --------------------------------------------------------
    # Quit
    # --------------------------------------------------------

    if key == ord("q"):

        break


    # ========================================================
    # STAGE 1 — PATCHCORE
    # ========================================================

    anomaly_detected, anomaly_bbox = (
        detect_anomaly(
            frame
        )
    )


    if not anomaly_detected:

        cv2.putText(
            frame,
            "NO ANOMALY",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )


        cv2.imshow(
            "UAV Integrated Detection",
            frame
        )


        continue


    # ========================================================
    # STAGE 2 — CROP ANOMALY
    # ========================================================

    x1, y1, x2, y2 = (
        anomaly_bbox
    )


    crop = frame[
        y1:y2,
        x1:x2
    ]


    if crop.size == 0:

        continue


    # ========================================================
    # ZOOM
    # ========================================================

    zoomed_crop = cv2.resize(
        crop,
        (
            frame_width,
            frame_height
        )
    )


    # ========================================================
    # STAGE 3 — FOD YOLO
    # ========================================================

    fod_results = (
        fod_detector.detect(
            zoomed_crop
        )
    )


    # ========================================================
    # FOD RESULTS
    # ========================================================

    for detection in fod_results:

        object_name = (
            detection["object"]
        )


        confidence = (
            detection["confidence"]
        )


        x1, y1, x2, y2 = (
            detection["bbox"]
        )


        object_center_x, object_center_y = (
            detection["center"]
        )


        # ----------------------------------------------------
        # Coordinate relative to camera centre
        # ----------------------------------------------------

        relative_x = (
            object_center_x
            - camera_center_x
        )


        relative_y = (
            object_center_y
            - camera_center_y
        )


        # ----------------------------------------------------
        # OUTPUT
        # ----------------------------------------------------

        print("\n========================================")

        print(
            "Object detected:",
            object_name
        )

        print(
            "Coordinate from camera center:",
            f"({relative_x}, {relative_y})"
        )

        print(
            "Confidence:",
            f"{confidence:.3f}"
        )

        print(
            "========================================")


        # ----------------------------------------------------
        # Draw bounding box
        # ----------------------------------------------------

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )


        # Centre

        cv2.circle(
            frame,
            (
                object_center_x,
                object_center_y
            ),
            6,
            (0, 0, 255),
            -1
        )


        # Label

        cv2.putText(
            frame,
            f"{object_name} {confidence:.2f}",
            (
                x1,
                max(
                    20,
                    y1 - 10
                )
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


    # ========================================================
    # STAGE 4 — CRACK DETECTION
    # ========================================================

    crack_result = (
        crack_detector.detect(
            zoomed_crop
        )
    )


    # ========================================================
    # CRACK RESULT
    # ========================================================

    if crack_result is not None:

        x1, y1, x2, y2 = (
            crack_result["bbox"]
        )


        crack_center_x, crack_center_y = (
            crack_result["center"]
        )


        # ----------------------------------------------------
        # Relative coordinate
        # ----------------------------------------------------

        relative_x = (
            crack_center_x
            - camera_center_x
        )


        relative_y = (
            crack_center_y
            - camera_center_y
        )


        # ----------------------------------------------------
        # OUTPUT
        # ----------------------------------------------------

        print("\n========================================")

        print(
            "Object detected: CRACK"
        )

        print(
            "Coordinate from camera center:",
            f"({relative_x}, {relative_y})"
        )

        print(
            "========================================")


        # ----------------------------------------------------
        # Draw crack bounding box
        # ----------------------------------------------------

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            2
        )


        # Crack centre

        cv2.circle(
            frame,
            (
                crack_center_x,
                crack_center_y
            ),
            6,
            (255, 0, 0),
            -1
        )


        cv2.putText(
            frame,
            "CRACK",
            (
                x1,
                max(
                    20,
                    y1 - 10
                )
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )


    # ========================================================
    # DISPLAY
    # ========================================================

    cv2.imshow(
        "UAV Integrated Detection",
        frame
    )


# ============================================================
# SHUTDOWN
# ============================================================

cap.release()

cv2.destroyAllWindows()


print("\n========================================")
print("UAV DETECTION SYSTEM STOPPED")
print("========================================")