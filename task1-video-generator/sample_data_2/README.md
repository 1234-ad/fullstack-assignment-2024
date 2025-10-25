# Sample Data 2 - Technology Showcase

This dataset contains technology-themed content for testing the video generator.

## Contents

- **7 images** (1.jpg through 7.jpg)
- **scripts.txt** - Technology-themed narration scripts
- **background.mp3** - Background music file

## Theme

This dataset focuses on modern technology topics including:
- Artificial Intelligence
- Cloud Computing
- Cybersecurity
- Internet of Things
- Blockchain
- Quantum Computing
- Virtual Reality

## Usage

```python
from video_generator import VideoGenerator

generator = VideoGenerator()
generator.create_video(
    images_folder="./sample_data_2/images",
    scripts_file="./sample_data_2/scripts.txt",
    music_file="./sample_data_2/background.mp3",
    output_file="tech_showcase.mp4"
)
```

## Expected Output

A video approximately 30-45 seconds long showcasing technology concepts with narration and background music.

## Notes

- Images are placeholder files for testing purposes
- Replace with actual images for production use
- Background music is a placeholder - use royalty-free music for actual videos
- Scripts are synchronized with image count (7 scripts for 7 images)
