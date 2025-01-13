# Simple Screen Recorder

## Overview
[Video Demostration](video_demostration/grabacion_final.gif)

> .[!IMPORTANT]
> If the video does not have audio when playing, you can try using VLC Media Player

This project allows you to record your screen along with audio and a custom cursor overlay. It captures a selected screen area, records audio from your microphone, and combines them into a final video. The application provides a graphical user interface (GUI) using `tkinter` to interact with the user and select the recording area. The recording is done with video and audio synchronization, with the cursor image being added to the video.

## Features

- **Screen Area Selection**: Select a custom area to record using a GUI.
- **Audio Recording**: Records audio from the microphone while screen recording.
- **Cursor Overlay**: Adds a custom cursor image to the video.
- **Pause and Resume**: Allows pausing and resuming the recording.
- **Final Video Export**: Combines the recorded video and audio into a final video file.

## Requirements

Before running the script, ensure that you have the following Python libraries installed:

- `opencv-python` (for video processing)
- `mss` (for screen capturing)
- `pyautogui` (for capturing cursor position)
- `pyaudio` (for audio recording)
- `pydub` (for audio conversion and processing)
- `tkinter` (for the GUI)
- `numpy` (for array handling)
- `ffmpeg` (for video and audio combining)

### Install the required libraries

You can install the required libraries using `pip`:

```bash
pip install opencv-python mss pyautogui pyaudio pydub numpy
```

Additionally, you need to have ffmpeg installed on your system. You can install it via your package manager or download it from the official [FFmpeg website](https://ffmpeg.org/download.html).

For Linux (Ubuntu/Debian)
```bash
sudo apt-get install ffmpeg
```

For Linux (Fedora/RedHat)
```bash
sudo dnf install ffmpeg
```

For macOS (Using Homebrew)
```bash
brew install ffmpeg
```

For Windows:
Download and install FFmpeg from the official website and add it to your system's PATH.

## How to Use
- **Step 1:** Prepare the Cursor Image
Ensure you have a cursor image (e.g., cursor.png) in the cursor folder of the project. This image will be used to overlay the cursor on the recorded screen.

- **Step 2:** Run the Script
You can run the script directly:

```bash
python3 screen-recorder.py
```

- **Step 3:** Select the Area to Record
1. When you launch the application, click and drag to select the area of the screen you want to record.
2. The selected area will be highlighted on the screen.

- **Step 4:** Start Recording
1. Click Iniciar Grabación (Start Recording) to begin the screen and audio recording.
2. The application will capture both video and audio from the selected area and your microphone.
3. You can pause and resume the recording using the Pausar/Reanudar Grabación (Pause/Resume Recording) button.

- **Step 5:** Stop Recording and Save the File
When you are finished, click Detener Grabación (Stop Recording).
The video and audio will be combined into a final .mp4 file, which will be saved as grabacion_final.mp4.

- **Step 6:** View the Final Video
After the recording is complete, the application will show a message with the final video file path. You can open this file to view the combined screen recording and audio.

## Code Explanation
1. Cursor Image Handling
The cursor image is loaded from the file system, resized to fit within the selected screen area, and drawn on the screen while recording. The code handles transparent PNGs to properly overlay the cursor with alpha blending.

2. Audio Recording
The audio is recorded using the pyaudio library. The recorded audio is saved as a WAV file, then converted to MP3 using pydub.

3. Screen Recording
The screen recording is done using mss for fast and efficient screen capturing. The captured frames are processed using opencv to add the cursor and save the video.

4. FFmpeg for Final Video
After the recording, the video and audio files are combined using ffmpeg into a final video. This step is handled with a system call to FFmpeg.

## Troubleshooting
- **Missing Libraries:** Make sure you have installed all required dependencies using pip install.
- **FFmpeg Issues:** Ensure FFmpeg is installed and accessible in your system's PATH. You can test this by running ffmpeg -version in your terminal.
- **Audio Not Syncing with Video:** Ensure the correct fps value is set for video recording. A mismatch in frame rates between audio and video may cause syncing issues.

## Contributing
Feel free to fork the repository and create a pull request for any improvements or bug fixes. Please make sure to test any changes you make.

