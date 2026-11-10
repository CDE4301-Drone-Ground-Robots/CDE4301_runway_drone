from ultralytics import YOLO


class FODDetector:

    def __init__(
        self,
        model_path,
        confidence=0.30,
        device=0
    ):

        self.model = YOLO(
            model_path
        )

        self.confidence = confidence
        self.device = device


    def detect(self, image):

        results = self.model.predict(
            source=image,
            conf=self.confidence,
            device=self.device,
            verbose=False
        )


        detections = []


        for result in results:

            if result.boxes is None:
                continue


            for box in result.boxes:

                # ------------------------------------------
                # Bounding box
                # ------------------------------------------

                x1, y1, x2, y2 = (
                    box.xyxy[0]
                    .cpu()
                    .numpy()
                    .astype(int)
                )


                # ------------------------------------------
                # Class
                # ------------------------------------------

                class_id = int(
                    box.cls[0]
                )


                class_name = (
                    self.model.names[
                        class_id
                    ]
                )


                # ------------------------------------------
                # Confidence
                # ------------------------------------------

                confidence = float(
                    box.conf[0]
                )


                # ------------------------------------------
                # Centre
                # ------------------------------------------

                center_x = int(
                    (x1 + x2) / 2
                )

                center_y = int(
                    (y1 + y2) / 2
                )


                detections.append({

                    "object": class_name,

                    "class_id": class_id,

                    "confidence": confidence,

                    "bbox": (
                        x1,
                        y1,
                        x2,
                        y2
                    ),

                    "center": (
                        center_x,
                        center_y
                    )
                })


        return detections