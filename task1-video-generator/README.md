# Task 1: Video Generator

A Python module that compiles videos from images, scripts, and background music with text-to-speech functionality.

## Features

- Combines 5-10 images in sequential order
- Text-to-speech narration for each image
- Background music throughout the video
- Automatic timing based on speech duration
- Support for multiple datasets

## Requirements

```bash
pip install -r requirements.txt
```

## Usage

```python
from video_generator import VideoGenerator

generator = VideoGenerator()
generator.create_video(
    images_folder="./sample_data/images",
    scripts_file="./sample_data/scripts.txt",
    music_file="./sample_data/background.mp3",
    output_file="output_video.mp4"
)
```

## Sample Data Structure

```
sample_data/
├── images/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
├── scripts.txt
└── background.mp3
```

## Scripts File Format

Each line corresponds to an image:
```
Welcome to our presentation about nature
This beautiful landscape shows the mountains
The sunset creates amazing colors in the sky
```

## Dependencies

- `moviepy`: Video editing
- `pyttsx3`: Text-to-speech
- `Pillow`: Image processing
- `numpy`: Array operations

## Testing

Two sample datasets are provided:
- `sample_data_1/`: Nature presentation
- `sample_data_2/`: Technology showcase