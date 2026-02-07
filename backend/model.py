from ultralytics import YOLO


def load_models():
    yolo = YOLO("models/yolo.pt")

    return yolo, None
