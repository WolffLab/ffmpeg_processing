# ffmpeg_processing
This repo containing python code to process videos. It will trim and concatenate videos of rats as appropriate using ffmpeg

It takes in a .mat file as an input and processes the video based on the information in the .mat file

This code assumes that you are running a device that has a nvidia graphics card. If not, remove the CUDA tag from the OS commands in the vid_process.py file

In the the setting.py file you should include:
1. The path to where you have the ffmpeg executive file installed
2. The path where where you would like the processed videos to be saved
3. The path of the .mat file that contains the relavant info for processing the videos.

The requirements.txt file contains all the necessary libraries you need to run the code smoothly.

# How to run:

**1.**
Create a new virtual environment:
```
python -m venv env_ffmpeg
```

If you do not have the virtual environment tool you can install it using:
```
python -m pip install virtualenv
```

The acitivate the virtual environment:
```
.\env_ffmpeg\Scripts\activate
```

**2.**
Install the required packages:
```
python -m pip install -r .\requirements.txt
```

**3.**
Edit the settings.py file to include the relavant paths

**4.**
Run the code then sit back and relax
```
python .\ffmpeg_process.py
```
