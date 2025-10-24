import os
import tempfile
from moviepy.editor import *
import pyttsx3
from PIL import Image
import numpy as np

class VideoGenerator:
    def __init__(self):
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speech rate
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
    def create_video(self, images_folder, scripts_file, music_file, output_file):
        """
        Create a video from images, scripts, and background music.
        
        Args:
            images_folder (str): Path to folder containing numbered images
            scripts_file (str): Path to text file with scripts for each image
            music_file (str): Path to background music file
            output_file (str): Path for output video file
        """
        print("Starting video generation...")
        
        # Load scripts
        scripts = self._load_scripts(scripts_file)
        
        # Get sorted image files
        image_files = self._get_sorted_images(images_folder)
        
        if len(image_files) != len(scripts):
            raise ValueError(f"Number of images ({len(image_files)}) doesn't match number of scripts ({len(scripts)})")
        
        # Generate audio for each script
        audio_clips = []
        video_clips = []
        
        for i, (image_file, script) in enumerate(zip(image_files, scripts)):
            print(f"Processing image {i+1}/{len(image_files)}: {os.path.basename(image_file)}")
            
            # Generate speech audio
            audio_file = self._text_to_speech(script, f"temp_audio_{i}.wav")
            audio_clip = AudioFileClip(audio_file)
            audio_clips.append(audio_clip)
            
            # Create video clip from image
            img_clip = ImageClip(image_file, duration=audio_clip.duration)
            img_clip = img_clip.resize(height=720)  # Standardize height
            video_clips.append(img_clip)
            
            # Clean up temporary audio file
            os.remove(audio_file)
        
        # Concatenate all video clips
        final_video = concatenate_videoclips(video_clips, method="compose")
        
        # Add background music
        if music_file and os.path.exists(music_file):
            background_music = AudioFileClip(music_file)
            # Loop music if it's shorter than video
            if background_music.duration < final_video.duration:
                background_music = background_music.loop(duration=final_video.duration)
            else:
                background_music = background_music.subclip(0, final_video.duration)
            
            # Reduce background music volume
            background_music = background_music.volumex(0.3)
            
            # Combine speech and background music
            speech_audio = concatenate_audioclips(audio_clips)
            final_audio = CompositeAudioClip([speech_audio, background_music])
            final_video = final_video.set_audio(final_audio)
        else:
            # Use only speech audio
            final_audio = concatenate_audioclips(audio_clips)
            final_video = final_video.set_audio(final_audio)
        
        # Write the final video
        print(f"Writing video to {output_file}...")
        final_video.write_videofile(
            output_file,
            fps=24,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Clean up
        for clip in video_clips + audio_clips:
            clip.close()
        final_video.close()
        
        print(f"Video generation complete! Output: {output_file}")
    
    def _load_scripts(self, scripts_file):
        """Load scripts from text file."""
        with open(scripts_file, 'r', encoding='utf-8') as f:
            scripts = [line.strip() for line in f.readlines() if line.strip()]
        return scripts
    
    def _get_sorted_images(self, images_folder):
        """Get sorted list of image files."""
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        image_files = []
        
        for filename in os.listdir(images_folder):
            if filename.lower().endswith(image_extensions):
                image_files.append(os.path.join(images_folder, filename))
        
        # Sort by filename (assuming numbered like 1.jpg, 2.jpg, etc.)
        image_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
        return image_files
    
    def _text_to_speech(self, text, output_file):
        """Convert text to speech and save as audio file."""
        temp_file = os.path.join(tempfile.gettempdir(), output_file)
        self.tts_engine.save_to_file(text, temp_file)
        self.tts_engine.runAndWait()
        return temp_file

# Example usage
if __name__ == "__main__":
    generator = VideoGenerator()
    
    # Test with sample data 1
    try:
        generator.create_video(
            images_folder="./sample_data_1/images",
            scripts_file="./sample_data_1/scripts.txt",
            music_file="./sample_data_1/background.mp3",
            output_file="output_video_1.mp4"
        )
    except Exception as e:
        print(f"Error with sample data 1: {e}")
    
    # Test with sample data 2
    try:
        generator.create_video(
            images_folder="./sample_data_2/images",
            scripts_file="./sample_data_2/scripts.txt",
            music_file="./sample_data_2/background.mp3",
            output_file="output_video_2.mp4"
        )
    except Exception as e:
        print(f"Error with sample data 2: {e}")