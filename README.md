# Flask-Classification
This project uses Flask to render a web page where a user can take a picture using the Pi Camera and then classify the image with OpenVINO'

## Getting Started

Before you can run the application be sure to have OpenVINO installed. This [gist](https://gist.github.com/sentairanger/caf11a2432ceebd715c6b33c224f4960) helps you with the process. This project has only been tested on Bullseye 64 bit but I will test on Bookworm. This works on the Pi 4 and the Pi 3B+ but I will test on the Pi 5. After installing OpenVINO then you can run the application on the terminal with `python3 app.py`. Be sure to create an `images` subdirectory under the `static` directory first. Take a picture, then choose the file and display it on the page. Then press the `classify` button and then it should tell you what the image is. Note, that the classification is only as accurate as it can be due to the quality of the image so be sure the background isn't busy.

![image](https://github.com/sentairanger/Flask-Classification/blob/main/classify.png)
