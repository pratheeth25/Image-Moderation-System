from ultralytics import YOLO


def load_models():

    # YOLO for violence / person / weapon detection
    yolo = YOLO("models/yolo.pt")

    return yolo, None
