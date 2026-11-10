from ultralytics import YOLO

model = YOLO("yolo11s.pt")

model.train(
    data="Thermal.yml",
    epochs=1,
    imgsz=640,
    batch=8,
    device=0,
    workers=0,
    project="Thermal_YOLO",
    name="local_test"
)