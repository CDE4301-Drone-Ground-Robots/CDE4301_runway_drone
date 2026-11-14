import cv2
import numpy as np
import torch

import segmentation_models_pytorch as smp


class CrackDetector:

    def __init__(
        self,
        model_path,
        image_size=512,
        threshold=0.5
    ):

        self.image_size = image_size
        self.threshold = threshold


        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )


        # ----------------------------------------------
        # Create model
        # ----------------------------------------------

        self.model = smp.Unet(
            encoder_name="resnet34",
            encoder_weights=None,
            in_channels=3,
            classes=1
        )


        # ----------------------------------------------
        # Load trained weights
        # ----------------------------------------------

        self.model.load_state_dict(
            torch.load(
                model_path,
                map_location=self.device
            )
        )


        self.model = self.model.to(
            self.device
        )


        self.model.eval()


        # ----------------------------------------------
        # ImageNet normalization
        # ----------------------------------------------

        self.mean = np.array(
            [0.485, 0.456, 0.406],
            dtype=np.float32
        )


        self.std = np.array(
            [0.229, 0.224, 0.225],
            dtype=np.float32
        )


    def detect(self, image):

        original_height, original_width = (
            image.shape[:2]
        )


        # ----------------------------------------------
        # Resize
        # ----------------------------------------------

        resized = cv2.resize(
            image,
            (
                self.image_size,
                self.image_size
            )
        )


        # ----------------------------------------------
        # BGR → RGB
        # ----------------------------------------------

        resized = cv2.cvtColor(
            resized,
            cv2.COLOR_BGR2RGB
        )


        # ----------------------------------------------
        # Normalize
        # ----------------------------------------------

        resized = (
            resized.astype(
                np.float32
            ) / 255.0
        )


        resized = (
            resized - self.mean
        ) / self.std


        # ----------------------------------------------
        # HWC → CHW
        # ----------------------------------------------

        tensor = torch.from_numpy(
            resized
        ).permute(
            2,
            0,
            1
        ).unsqueeze(
            0
        ).float()


        tensor = tensor.to(
            self.device
        )


        # ----------------------------------------------
        # Prediction
        # ----------------------------------------------

        with torch.no_grad():

            prediction = self.model(
                tensor
            )


        # ----------------------------------------------
        # Sigmoid
        # ----------------------------------------------

        probability = torch.sigmoid(
            prediction
        )


        mask = (
            probability[0, 0]
            .cpu()
            .numpy()
        )


        # ----------------------------------------------
        # Binary mask
        # ----------------------------------------------

        binary_mask = (
            mask > self.threshold
        ).astype(
            np.uint8
        )


        # ----------------------------------------------
        # Resize mask
        # ----------------------------------------------

        binary_mask = cv2.resize(
            binary_mask,
            (
                original_width,
                original_height
            ),
            interpolation=cv2.INTER_NEAREST
        )


        # ----------------------------------------------
        # Find crack pixels
        # ----------------------------------------------

        ys, xs = np.where(
            binary_mask > 0
        )


        if len(xs) == 0:

            return None


        # ----------------------------------------------
        # Bounding box
        # ----------------------------------------------

        x1 = int(xs.min())
        y1 = int(ys.min())

        x2 = int(xs.max())
        y2 = int(ys.max())


        # ----------------------------------------------
        # Centre
        # ----------------------------------------------

        center_x = int(
            (x1 + x2) / 2
        )

        center_y = int(
            (y1 + y2) / 2
        )


        return {

            "type": "crack",

            "bbox": (
                x1,
                y1,
                x2,
                y2
            ),

            "center": (
                center_x,
                center_y
            ),

            "mask": binary_mask
        }