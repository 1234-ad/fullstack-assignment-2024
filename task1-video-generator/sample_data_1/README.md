# Sample Data 1 - README

This directory contains sample data for testing the video generator:

## Files:
- `images/` - Contains numbered images (1.jpg, 2.jpg, etc.)
- `scripts.txt` - Text scripts corresponding to each image
- `background.mp3` - Background music file

## Usage:
```python
generator = VideoGenerator()
generator.create_video(
    images_folder="./sample_data_1/images",
    scripts_file="./sample_data_1/scripts.txt", 
    music_file="./sample_data_1/background.mp3",
    output_file="output_video_1.mp4"
)
```

Note: For actual testing, replace placeholder files with real images and audio.