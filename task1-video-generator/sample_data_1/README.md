# Sample Data 1 - Nature Presentation

This dataset contains nature-themed content for testing the video generator.

## Contents

- **5 images** (1.jpg through 5.jpg)
- **scripts.txt** - Nature-themed narration scripts
- **background.mp3** - Background music file

## Theme

This dataset focuses on natural landscapes and environmental topics including:
- Mountain landscapes
- Sunset scenery
- Natural harmony
- Sustainable development
- Environmental beauty

## Usage

```python
from video_generator import VideoGenerator

generator = VideoGenerator()
generator.create_video(
    images_folder="./sample_data_1/images",
    scripts_file="./sample_data_1/scripts.txt",
    music_file="./sample_data_1/background.mp3",
    output_file="nature_presentation.mp4"
)
```

## Expected Output

A video approximately 20-30 seconds long showcasing nature scenes with narration and background music.

## Notes

- Images are placeholder files for testing purposes
- Replace with actual nature photographs for production use
- Background music is a placeholder - use royalty-free music for actual videos
- Scripts are synchronized with image count (5 scripts for 5 images)
- Each image displays for the duration of its corresponding narration

## File Structure

```
sample_data_1/
├── images/
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── 3.jpg
│   ├── 4.jpg
│   └── 5.jpg
├── scripts.txt
├── background.mp3
└── README.md
```
