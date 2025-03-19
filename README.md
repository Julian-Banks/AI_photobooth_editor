# Raspberry Pi Ai Photobooth

**This is a basic Proof of Concept!!!**   
The project is designed to use a Raspberry Pi and a PiCamera to create a fun photobooth!

The script streams video from the PiCam to a PyGame window. When the user takes a photo (currently with a basic capture button but could be any input) the camera takes a photo. The OpenAI API for image editing is then used to send the photo, a mask, a prompt and some configuration. The API returns a URL that contains the edited image. The script then downloads the image and displays it for 10 seconds before quiting. 

Some example photos: [Example Photos](https://docs.google.com/document/d/1Bnb4FEQ76sIsDPlZo-fERJYLpB0Q9isZ0czeuLQ6R7w/edit?usp=sharing)

## Setup
python -m venv --system-site-packages env \ 
This is necessary to include pre-installed packages like PiCamera2

source env/bin/activate

pip3 install openai

export OPENAI_API_KEY="YOUR_API_KEY" //Sets the environment variable for your OPENAI_API_KEY

## Improvements 

AI Image Edit: 
- Improve the prompt!!!
- Use a higher quality image (using 512*512) 
- Try a higher number of inferences (only tried with 1 and 3)
- Improve setting. Nice background and lighting ect.
- Try different mask settings + try generate new mask for each photo?
- Try find a different Image model.

Application:
- Nicer window to display video stream.
- More modern and sleek button to capture video.
- Rework Script to be modular and pythonic
 
Repo:
- Add requirements.txt
  
# Documentation used: 
- [OpenAI API image editing](https://platform.openai.com/docs/guides/images) 
