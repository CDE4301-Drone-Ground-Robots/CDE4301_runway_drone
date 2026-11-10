from pathlib import Path
import cv2
import numpy as np
import torch

from torch.utils.data import Dataset, DataLoader, random_split
import segmentation_models_pytorch as smp


# ============================================================
# SETTINGS
# ============================================================

IMAGE_DIR = Path(r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_CRACKS_DETECTION\Crack_Dataset\images")
MASK_DIR = Path(r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_CRACKS_DETECTION\Crack_Dataset\masks")

IMAGE_SIZE = 512
BATCH_SIZE = 16
EPOCHS = 100
LR = 1e-3

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("Device:", DEVICE)


# ============================================================
# DATASET
# ============================================================

class CrackDataset(Dataset):

    def __init__(self, image_dir, mask_dir):

        self.image_dir = image_dir
        self.mask_dir = mask_dir

        self.images = sorted([
            f for f in image_dir.iterdir()
            if f.suffix.lower() in [".jpg", ".jpeg", ".png"]
        ])


    def __len__(self):
        return len(self.images)


    def __getitem__(self, idx):

        image_path = self.images[idx]

        # assumes:
        # 001.jpg -> 001_mask.jpg

        mask_path = (
            self.mask_dir /
            f"{image_path.stem}_mask.jpg"
        )


        image = cv2.imread(str(image_path))

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )


        mask = cv2.imread(
            str(mask_path),
            cv2.IMREAD_GRAYSCALE
        )


        # Resize

        image = cv2.resize(
            image,
            (IMAGE_SIZE, IMAGE_SIZE)
        )

        mask = cv2.resize(
            mask,
            (IMAGE_SIZE, IMAGE_SIZE),
            interpolation=cv2.INTER_NEAREST
        )


        # Normalize image

        image = image.astype(np.float32) / 255.0

        image = (
           image - np.array([0.485, 0.456, 0.406])
            ) / np.array([0.229, 0.224, 0.225])


        # Binary mask

        mask = (
            mask > 127
        ).astype(np.float32)


        # HWC -> CHW

        image = torch.from_numpy(
            image
        ).permute(2, 0, 1)


        mask = torch.from_numpy(
            mask
        ).unsqueeze(0)


        return image, mask


# ============================================================
# LOAD DATASET
# ============================================================

dataset = CrackDataset(
    IMAGE_DIR,
    MASK_DIR
)


train_size = int(
    0.8 * len(dataset)
)

val_size = (
    len(dataset) - train_size
)


train_set, val_set = random_split(
    dataset,
    [train_size, val_size],
    generator=torch.Generator().manual_seed(42)
)


train_loader = DataLoader(
    train_set,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)


val_loader = DataLoader(
    val_set,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)


# ============================================================
# PRETRAINED U-NET
# ============================================================

model = smp.Unet(
    encoder_name="resnet34",
    encoder_weights="imagenet",
    in_channels=3,
    classes=1
)

model = model.to(DEVICE)


# ============================================================
# FREEZE PRETRAINED ENCODER
# ============================================================

for parameter in model.encoder.parameters():

    parameter.requires_grad = False


# ============================================================
# LOSS
# ============================================================

dice_loss = smp.losses.DiceLoss(
    mode="binary",
    from_logits=True
)

bce_loss = torch.nn.BCEWithLogitsLoss()


def loss_fn(prediction, target):

    return (
        dice_loss(prediction, target)
        +
        bce_loss(prediction, target)
    )


# ============================================================
# OPTIMIZER
#
# Only parameters that are NOT frozen
# ============================================================

optimizer = torch.optim.Adam(
    filter(
        lambda p: p.requires_grad,
        model.parameters()
    ),
    lr=LR
)


# ============================================================
# TRAIN
# ============================================================

best_val_loss = float("inf")


for epoch in range(EPOCHS):

    # ---------------- TRAIN ----------------

    model.train()

    train_loss = 0


    for images, masks in train_loader:

        images = images.to(DEVICE)
        masks = masks.to(DEVICE)


        optimizer.zero_grad()


        prediction = model(images)


        loss = loss_fn(
            prediction,
            masks
        )


        loss.backward()

        optimizer.step()


        train_loss += loss.item()


    train_loss /= len(train_loader)


    # ---------------- VALIDATION ----------------

    model.eval()

    val_loss = 0


    with torch.no_grad():

        for images, masks in val_loader:

            images = images.to(DEVICE)
            masks = masks.to(DEVICE)


            prediction = model(images)


            loss = loss_fn(
                prediction,
                masks
            )


            val_loss += loss.item()


    val_loss /= len(val_loader)


    print(
        f"Epoch {epoch+1}/{EPOCHS} | "
        f"Train: {train_loss:.4f} | "
        f"Val: {val_loss:.4f}"
    )


    # ---------------- SAVE BEST ----------------

    if val_loss < best_val_loss:

        best_val_loss = val_loss

        torch.save(
            model.state_dict(),
            "best_crack_model.pth"
        )

        print("Saved best model")


print("Training complete.")