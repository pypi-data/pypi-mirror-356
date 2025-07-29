import numpy as np
import hashlib
import cv2
import queue
import threading
import time
from collections import deque
import json
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

def get_timestamp_id():
    jst = timezone(timedelta(hours=9)) 
    return datetime.now(jst).strftime('%Y%m%d%H%M%S%f')

def get_current_date_time():
    return datetime.now(ZoneInfo("Asia/Tokyo"))

# def generate_unique_id(array: np.ndarray) -> str:
#     if not isinstance(array, np.ndarray) or array.ndim != 1 or len(array) != 512:
#         raise ValueError("Input must be a 1D NumPy array of length 512.")
    
#     array_bytes = array.tobytes()
    
#     unique_id = hashlib.sha256(array_bytes).hexdigest()
    
#     return unique_id

def generate_unique_id(array: np.ndarray, length: int = 32) -> str:
    if not isinstance(array, np.ndarray) or array.ndim != 1 or len(array) != 512:
        raise ValueError("Input must be a 1D NumPy array of length 512.")

    array_bytes = array.tobytes()
    unique_id = hashlib.sha256(array_bytes).hexdigest()[:length]  # Truncate hash

    return unique_id+"_"+get_timestamp_id()

# def crop_bbox_from_frame(frame,bbox, target_size=None):
#     h, w, c = frame.shape
#     x1, y1, x2, y2 = bbox

#     x1 = max(0,x1)
#     y1 = max(0,y1)
#     x2 = min(w,x2)
#     y2 = min(h,y2)

#     face_img = frame[y1:y2,x1:x2]

#     if target_size is not None:
#         face_img = cv2.resize(face_img, target_size)
    
#     return face_img

def crop_bbox_from_frame(input_frame, bbox, target_size=None):
    frame = input_frame.copy()
    h, w, c = frame.shape
    x1, y1, x2, y2 = bbox

    # Ensure coordinates are within the frame bounds
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w, x2)
    y2 = min(h, y2)

    # Draw a red rectangle around the bounding box
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Red color, thickness = 2

    if target_size:
        h, w = frame.shape[:2]  # Get original height and width

        # Determine the scaling factor (based on the larger dimension)
        scale = target_size / max(w, h)

        # Compute new dimensions and round to the nearest integer
        new_w = round(w * scale)
        new_h = round(h * scale)

        # Resize the frame
        frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    return frame

def write_image(img, path):
    bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, bgr_img)

def add_alert(frame, text = None, color=(255,0,0)):
    # Add alert text
    if text is None:
        text = "Alert: dined and dashed person detected!"
    if color is None:
        color = (255, 0, 0)

    # Add 3px border
    cv2.rectangle(frame, (0, 0), (frame.shape[1]-1, frame.shape[0]-1), color, 3)

    font, scale, thickness = cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
    text_size = cv2.getTextSize(text, font, scale, thickness)[0]
    cv2.rectangle(frame, (5, 5), (10 + text_size[0], 10 + text_size[1]), (255, 255, 255), -1)
    cv2.putText(frame, text, (10, 10 + text_size[1]), font, scale, color, thickness)
    return frame

class VideoCapture:
    def __init__(self, source, target_size=None):
        """
        Initialize the VideoCapture object with a source and optional target resolution.

        Args:
            name (str): The video source (e.g., RTSP URL).
            target_size (int, optional): Target size for the largest dimension (width or height).
                                         If None, no resizing will be applied.
        """
        self.source = source
        self.target_size = target_size
        self.target_width = None
        self.target_height = None

        if "rtsp" in str(source):
           
            gstreamer_pipeline = (
                f"rtspsrc location={source} latency=0 ! "
                "rtph265depay ! h265parse ! nvv4l2decoder enable-max-performance=1 ! "
                "nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! "
                "video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=True"
            )
            
            self.cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)
        else:
            self.cap = cv2.VideoCapture(source, cv2.CAP_V4L2)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if target_size:
            original_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            original_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            if original_width > 0 and original_height > 0:
        
                aspect_ratio = original_height / original_width
                if original_width > original_height:
                    self.target_width = target_size
                    self.target_height = int(target_size * aspect_ratio)
                else:
                    self.target_height = target_size
                    self.target_width = int(target_size / aspect_ratio)
                
                if "rtsp" not in str(self.source):
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.target_width)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.target_height)

    def read(self):
        ret, frame = self.cap.read()

        if not ret:
            return ret, None

        if self.target_width:
            frame = cv2.resize(frame,(self.target_width,self.target_height))

        # print(frame.shape)

        return ret, frame
    
    def release(self):
        """
        Release the video capture object and stop the reader thread.
        """
        self.cap.release()         # Release the video capture object

    def isOpened(self):
        """
        Check if the video capture object is opened.

        Returns:
            bool: True if opened, False otherwise.
        """
        return self.cap.isOpened()

def add_border_and_text(frame, text, bbox_size=3, color=(0, 255, 0)):
    """
    Adds a border of specified size and color to the frame, and places text
    on the top-left corner (below the border) in the same color.

    Parameters:
        frame (numpy.ndarray): The input video frame.
        text (str): The text to add to the frame.
        bbox_size (int): The thickness of the border (default is 3).
        color (tuple): The color of the border and text in (B, G, R) format (default is (0, 0, 255)).

    Returns:
        numpy.ndarray: The modified frame with the border and text.
    """
    # Add the border
    frame_with_border = cv2.copyMakeBorder(
        frame,
        top=bbox_size,
        bottom=bbox_size,
        left=bbox_size,
        right=bbox_size,
        borderType=cv2.BORDER_CONSTANT,
        value=color
    )
    
    # Add the text
    text_x, text_y = bbox_size + 5, bbox_size + 20  # Position text below the border
    font_scale = 0.6
    thickness = 1
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    text_w, text_h = text_size

    # Background rectangle for text
    cv2.rectangle(
        frame_with_border,
        (text_x - 5, text_y - text_h - 5),
        (text_x + text_w + 5, text_y + 5),
        color,
        -1
    )

    # Text in white
    cv2.putText(
        frame_with_border,
        text,
        (text_x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (255, 255, 255),  # White color for text
        thickness
    )
    
    return frame_with_border

class EfficientIDCounter:
    def __init__(self, retention_time=2):
        self.retention_time = retention_time  # Retention time in seconds
        self.queue = deque()  # Store tuples of (id, timestamp)
        self.data = {}  # Dictionary to track counts of IDs

    def add_id(self, id_strs):
        """
        Add a single ID or a list of IDs to the counter.
        """
        if not isinstance(id_strs, list):  # Handle a single ID
            id_strs = [id_strs]

        current_time = time.time()
        # Remove old entries from the deque and dictionary
        self._remove_old_ids(current_time)

        for id_str in id_strs:
            if id_str is None:
                continue
            # Update or add the new ID
            if id_str in self.data:
                self.data[id_str] += 1
            else:
                self.data[id_str] = 1
            self.queue.append((id_str, current_time))  # Add to the deque

    def _remove_old_ids(self, current_time):
        while self.queue and current_time - self.queue[0][1] > self.retention_time:
            old_id, _ = self.queue.popleft()
            self.data[old_id] -= 1
            if self.data[old_id] == 0:
                del self.data[old_id]

    def get_largest_count_id(self):
        """
        Get the ID with the largest count.
        """
        if not self.data:
            return None, 0
        return max(self.data.items(), key=lambda x: x[1])

    def get_data(self):
        """
        Get the current state of the counter.
        """
        return dict(self.data)

    def reset_data(self):
        """
        Reset the counter, clearing all stored data.
        """
        self.queue.clear()
        self.data.clear()

def change_value(value, replace_value):
    if value is None: return replace_value
    if value == "": return replace_value
    return value

def format_json(json_data, indent_level=0):
    if json_data is None:
        return "None"
    # If json_data is a string, parse it as JSON
    if isinstance(json_data, str):
        return json_data

    # Initialize an empty string to store formatted output
    formatted_data = ""
    
    # Loop through each key-value pair in the dictionary
    for key, value in json_data.items():
        # Create an indentation prefix based on the current indent level
        indent = "\t" * indent_level
        
        if isinstance(value, dict):
            # Recursively call format_json if the value is a dictionary (nested JSON)
            formatted_data += f"{indent}🞄 {key}:\n"  # Key with no value shown, just heading
            formatted_data += format_json(value, indent_level + 1)  # Increase indent level for nested JSON
        else:
            # Format and add the key-value pair
            formatted_data += f"{indent}🞄 {key}: {value}\n"
    
    return formatted_data

# Helper function to calculate the perpendicular distance from a point to a line
def calculate_perpendicular_distance(point, line_start, line_end):
    line_vector = np.array([line_end[0] - line_start[0], line_end[1] - line_start[1]])
    perpendicular_vector = np.array([-line_vector[1], line_vector[0]])  # Perpendicular to line
    perpendicular_vector = perpendicular_vector / np.linalg.norm(line_vector)  # Normalize
    point_vector = np.array([point[0] - line_start[0], point[1] - line_start[1]])
    return abs(np.dot(point_vector, perpendicular_vector))

# # Function to classify the face based on nose, eyes, and perpendicular middle line
# def is_frontal_face(keypoints, front_face_angle_threshold=0.5):
#     # Extract keypoints
#     left_eye, right_eye, nose, left_mouth, right_mouth = keypoints

#     if nose[0] < min(left_eye[0], right_eye[0]) or \
#         nose[0] > max(left_eye[0], right_eye[0]):
#         return False

#     # Calculate the eye line vector
#     eye_line_vector = np.array([right_eye[0] - left_eye[0], right_eye[1] - left_eye[1]])

#     # Calculate the middle line's perpendicular direction
#     perpendicular_vector = np.array([-eye_line_vector[1], eye_line_vector[0]])  # Perpendicular to eye line
#     perpendicular_vector = perpendicular_vector / np.linalg.norm(perpendicular_vector)  # Normalize

#     # Calculate the middle line (nose-centered perpendicular line)
#     middle_line_end_x = int(nose[0] + perpendicular_vector[0] * 100)  # Extend by 100 pixels
#     middle_line_end_y = int(nose[1] + perpendicular_vector[1] * 100)

#     # Calculate distances from each eye to the middle line
#     def calc_eye_to_middle_distance(eye):
#         return abs((middle_line_end_y - nose[1]) * (eye[0] - nose[0]) - (middle_line_end_x - nose[0]) * (eye[1] - nose[1])) / np.linalg.norm([middle_line_end_x - nose[0], middle_line_end_y - nose[1]])

#     left_eye_to_middle_line = calc_eye_to_middle_distance(left_eye)
#     right_eye_to_middle_line = calc_eye_to_middle_distance(right_eye)

#     # Check if eye-to-middle distances are within an acceptable threshold (50% difference)
#     if min(left_eye_to_middle_line, right_eye_to_middle_line) / max(left_eye_to_middle_line, right_eye_to_middle_line) < front_face_angle_threshold:
#         return False

#     # Calculate distances from nose to eye line and mouth line
#     def calc_line_distance(line_start, line_end, reference_point):
#         return abs((line_end[1] - line_start[1]) * (reference_point[0] - line_start[0]) - (line_end[0] - line_start[0]) * (reference_point[1] - line_start[1])) / np.linalg.norm([line_end[0] - line_start[0], line_end[1] - line_start[1]])

#     eye_line_distance = calc_line_distance(left_eye, right_eye, nose)
#     mouth_line_distance = calc_line_distance(left_mouth, right_mouth, nose)

#     # Check if distances from nose to eye line and mouth line are within a 50% threshold
#     if min(eye_line_distance, mouth_line_distance) / max(eye_line_distance, mouth_line_distance) < front_face_angle_threshold-0.1:
#         return False

#     return True

# Function to classify the face based on nose, eyes, and perpendicular middle line
def is_frontal_face(bbox, keypoints, threshold=0.4):
    # Extract keypoints
    left_eye, right_eye, nose, left_mouth, right_mouth = keypoints

    # Calculate bbox dimensions
    bbox_width = bbox[2] - bbox[0]
    bbox_height = bbox[3] - bbox[1]

    # Check if bbox width is less than 0.4 of bbox height
    if bbox_width < threshold * bbox_height:
        return False

    # Check if both eyes are within 0.4 left or 0.4 right of bbox
    left_eye_x, right_eye_x = left_eye[0], right_eye[0]
    left_bound = bbox[0] + threshold * bbox_width
    right_bound = bbox[2] - threshold * bbox_width

    if left_eye_x < left_bound and right_eye_x < left_bound:
        return False
    if left_eye_x > right_bound and right_eye_x > right_bound:
        return False

    return True

def remove_small_faces(analyzed_faces, frame, threshold=0.1, front_face_angle_threshold=0.5, get_largest_face=False):
    filter_result = []
    h, w, c = frame.shape

    largest_face = None
    largest_face_size = 0

    for analyzed_face in analyzed_faces:
        bbox = analyzed_face.bbox.astype(int)        
        x1, y1, x2, y2 = bbox

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

        # Check if face size meets the threshold
        if (y2 - y1) / h >= threshold and (x2 - x1) / w >= threshold:
            filter_result.append(analyzed_face)

            face_size = (y2-y1)*(x2-x1)
            if face_size > largest_face_size:
                largest_face_size = face_size
                largest_face = analyzed_face

    if get_largest_face:
        if largest_face: 
            return [largest_face]
        else:
            return []

    return filter_result  # Return all filtered faces if get_largest_face is False

