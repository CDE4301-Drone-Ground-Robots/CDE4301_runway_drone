import cv2
import numpy as np


DELTA_THRESHOLD = 25
MIN_AREA = 150
PERSISTENCE_FRAMES = 5

persistent_count = 0


def detect_temperature_anomalies(frame):

    global persistent_count

    # Convert to grayscale thermal intensity
    if len(frame.shape) == 3:
        thermal = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        thermal = frame.copy()

    # Smooth noise
    thermal_blur = cv2.GaussianBlur(
        thermal,
        (5, 5),
        0
    )

    # Background thermal level
    background_value = np.median(thermal_blur)

    # Difference from background
    difference = cv2.absdiff(
        thermal_blur,
        np.full_like(
            thermal_blur,
            int(background_value)
        )
    )

    # Threshold
    _, anomaly_mask = cv2.threshold(
        difference,
        DELTA_THRESHOLD,
        255,
        cv2.THRESH_BINARY
    )

    # Remove noise
    kernel = np.ones((3, 3), np.uint8)

    anomaly_mask = cv2.morphologyEx(
        anomaly_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    anomaly_mask = cv2.morphologyEx(
        anomaly_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # Find regions
    contours, _ = cv2.findContours(
        anomaly_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    anomaly_found = False
    anomaly_regions = []

    for contour in contours:

        area = cv2.contourArea(contour)

        if area < MIN_AREA:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        anomaly_found = True

        anomaly_regions.append(
            (x, y, w, h)
        )

    # Persistence logic
    if anomaly_found:
        persistent_count += 1
    else:
        persistent_count = 0

    persistent_hazard = (
        persistent_count >= PERSISTENCE_FRAMES
    )

    return (
        persistent_hazard,
        anomaly_regions,
        anomaly_mask,
        background_value
    )