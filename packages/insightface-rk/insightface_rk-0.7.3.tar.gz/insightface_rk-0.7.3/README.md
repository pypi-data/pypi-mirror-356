# InsightFace-Rk

An enhanced face analysis package built on top of InsightFace, with additional features for frontal face detection, largest face filtering, and improved gender/age estimation.

## Features

- All features from InsightFace base package
- Enhanced frontal face detection with angle validation
- Automatic largest face filtering
- Improved gender and age estimation
- Configurable face size thresholds

## Installation

```bash
pip install insightface-rk
```

## Usage

```python
from insightface.app import FaceAnalysis

# Initialize face analyzer with enhanced features
face_analyzer = FaceAnalysis(
    name='buffalo_l',
    root='.insightface',
    providers=['CUDAExecutionProvider', 'CPUExecutionProvider'],
    allowed_modules=['detection', 'recognition', 'genderage']
)

# Prepare the model with custom thresholds
face_analyzer.prepare(
    ctx_id=0,
    det_size=(960, 960),
    det_thresh=0.7
)

# Get faces with enhanced filtering
faces = face_analyzer.get(
    img,
    max_num=1,                    # Maximum number of faces to detect
    small_face_threshold=0.05,    # Minimum relative face size
    largest_face_only=True,       # Only return the largest face
    genderage=True               # Enable gender and age estimation
)

# Process detected faces
for face in faces:
    print(f"Age: {face.age}")
    print(f"Gender: {'Male' if face.gender == 1 else 'Female'}")
    print(f"Detection score: {face.det_score}")
```

## Enhanced Features Explained

### Frontal Face Detection

The package includes additional validation to ensure detected faces are sufficiently frontal-facing, improving the accuracy of subsequent recognition tasks.

### Largest Face Filtering

When `largest_face_only=True`, the system will automatically select the largest detected face in the image, useful for processing portrait photos or when the main subject should be prioritized.

### Face Size Thresholding

The `small_face_threshold` parameter allows filtering out faces that are too small relative to the image dimensions, helping to focus on the most relevant faces in the scene.

## Credits

This package is built on top of [InsightFace](https://github.com/deepinsight/insightface) (v0.7.3), an excellent face analysis toolkit. We extend our gratitude to the InsightFace team for their foundational work.

## License

This package is released under the MIT License. However, please note that the pretrained models from InsightFace are available for non-commercial research purposes only.

## Requirements

- Python >= 3.8
- CUDA-compatible GPU (optional, but recommended for better performance)
- See requirements.txt for full dependencies
