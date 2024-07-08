import cv2
import imutils
import os
import uuid
import img2pdf
import glob
from skimage.metrics import structural_similarity
from io import BytesIO

FRAME_RATE = 3
WARMUP = FRAME_RATE
FGBG_HISTORY = FRAME_RATE * 15
VAR_THRESHOLD = 16
DETECT_SHADOWS = False
MIN_PERCENT = 0.1
MAX_PERCENT = 3
SSIM_THRESHOLD = 0.9

def get_frames(video_path):
    vs = cv2.VideoCapture(video_path)
    if not vs.isOpened():
        raise Exception(f'unable to open file {video_path}')
    frame_time = 0
    frame_count = 0
    while True:
        vs.set(cv2.CAP_PROP_POS_MSEC, frame_time * 1000)
        frame_time += 1/FRAME_RATE
        (_, frame) = vs.read()
        if frame is None:
            break
        frame_count += 1
        yield frame_count, frame_time, frame
    vs.release()

def detect_unique_screenshots(video_path, output_folder_screenshot_path):
    fgbg = cv2.createBackgroundSubtractorMOG2(history=FGBG_HISTORY, varThreshold=VAR_THRESHOLD, detectShadows=DETECT_SHADOWS)
    captured = False
    (W, H) = (None, None)
    screenshoots_count = 0
    last_screenshot_file_path = ""
    for frame_count, frame_time, frame in get_frames(video_path):
        orig = frame.copy()
        frame = imutils.resize(frame, width=600)
        mask = fgbg.apply(frame)
        if W is None or H is None:
            (H, W) = mask.shape[:2]
        p_diff = (cv2.countNonZero(mask) / float(W * H)) * 100
        if p_diff < MIN_PERCENT and not captured and frame_count > WARMUP:
            captured = True
            filename = f"{screenshoots_count:03}_{round(frame_time/60, 2)}.png"
            path = os.path.join(output_folder_screenshot_path, filename)
            image_ssim = 0.0
            if last_screenshot_file_path != "":
                image_last = cv2.imread(last_screenshot_file_path)
                image_ssim = structural_similarity(image_last, orig, channel_axis=2, data_range=255)
            if image_ssim < SSIM_THRESHOLD:
                cv2.imwrite(path, orig)
                last_screenshot_file_path = path
                screenshoots_count += 1
        elif captured and p_diff >= MAX_PERCENT:
            captured = False
    return screenshoots_count

def initialize_output_folder():
    output_folder_screenshot_path = f"./output/{uuid.uuid4()}"
    os.makedirs(output_folder_screenshot_path, exist_ok=True)
    return output_folder_screenshot_path

def convert_screenshots_to_pdf(output_folder_screenshot_path, output_pdf_path):
    with open(output_pdf_path, "wb") as f:
        f.write(img2pdf.convert(sorted(glob.glob(f"{output_folder_screenshot_path}/*.png"))))

def video_to_slides(video_path):
    output_folder_screenshot_path = initialize_output_folder()
    detect_unique_screenshots(video_path, output_folder_screenshot_path)
    return output_folder_screenshot_path

def slides_to_pdf(output_folder_screenshot_path):
    output_pdf_path = f"{output_folder_screenshot_path}.pdf"
    convert_screenshots_to_pdf(output_folder_screenshot_path, output_pdf_path)
    return output_pdf_path
