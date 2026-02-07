from ultralytics import YOLO


def predict_nsfw(img_path, model):
    return 0.0


def predict_violence(img_path, yolo):

    result = yolo(img_path)[0]

    if len(result.boxes) == 0:
        return 0.0

    return float(result.boxes.conf.mean())
