# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms needs to be aware of.

## Prep

1.  Pull the new Github Repo.
2.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2021/Lab%202/prep.md), we offered the instruction at the bottom.
3.  Read about [OpenCV](https://opencv.org/about/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:

1. Raspberry Pi
1. Webcam 
1. Microphone (if you want to have speech or sound input for your design)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### OpenCV
A more traditional method to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python. We included 4 standard OpenCV examples: contour(blob) detection, face detection with the ``Haarcascade``, flow detection (a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (e.g. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example. 

Following is a nicer way you can run and see the flow of the `openCV-examples` we have included in your Pi. Instead of `ls`, the command we will be using here is `tree`. [Tree](http://mama.indstate.edu/users/ice/tree/) is a recursive directory colored listing command that produces a depth indented listing of files. Install `tree` first and `cd` to the `openCV-examples` folder and run the command:

```shell
pi@ixe00:~ $ sudo apt install tree
...
pi@ixe00:~ $ cd openCV-examples
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```

The flow detection might seem random, but consider [this recent research](https://cseweb.ucsd.edu/~lriek/papers/taylor-icra-2021.pdf) that uses optical flow to determine busy-ness in hospital settings to facilitate robot navigation. Note the velocity parameter on page 3 and the mentions of optical flow.

Now, connect your webcam to your Pi and use **VNC to access to your Pi** and open the terminal. Use the following command lines to try each of the examples we provided:
(***it will not work if you use ssh from your laptop***)

```
pi@ixe00:~$ cd ~/openCV-examples/contours-detection
pi@ixe00:~/openCV-examples/contours-detection $ python contours.py
...
pi@ixe00:~$ cd ~/openCV-examples/face-detection
pi@ixe00:~/openCV-examples/face-detection $ python face-detection.py
...
pi@ixe00:~$ cd ~/openCV-examples/flow-detection
pi@ixe00:~/openCV-examples/flow-detection $ python optical_flow.py 0 window
...
pi@ixe00:~$ cd ~/openCV-examples/object-detection
pi@ixe00:~/openCV-examples/object-detection $ python detect.py
```

**\*\*\*Try each of the following four examples in the `openCV-examples`, include screenshots of your use and write about one design for each example that might work based on the individual benefits to each algorithm.\*\*\***

![IMG_6756](https://user-images.githubusercontent.com/35357433/139716446-18410bec-a931-4996-aedb-268d6a2ec927.jpg)
> Contour Detection:
> > Contour detection would be useful to create an application that asseses the user's mood based on the contour of their facial expression. We can analyze common contours for certain emotions and evaluate the user's current emotion based on the trained data.

![IMG_6758](https://user-images.githubusercontent.com/35357433/139716473-8bb8bab1-bd74-4401-913a-ab8fe2c3b115.jpg)
> Face Detection:
> > Face detection would be useful to create a security system that checks who is allowed in and who isn't. If the system sees an unfamilar face, it can "learn" the face for next time.

![IMG_6759](https://user-images.githubusercontent.com/35357433/139716497-ca1dc888-e607-4a5c-be51-73620965ac1f.jpg)
> Flow Detection:
> > Flow detection would be useful to make a game where the user can "draw" a picture using head motion.

![IMG_6755](https://user-images.githubusercontent.com/35357433/139716513-efd3af5f-27a2-4b6d-8f65-6af7cfbe4480.jpg)
> Object Detection:
> > Object detection would be useful to make a grocery expiration list application where the user can take a picture of all their grocery items for the system to evaluate and make into a grocery list.

#### MediaPipe

A more recent open source and efficient method of extracting information from video streams comes out of Google's [MediaPipe](https://mediapipe.dev/), which offers state of the art face, face mesh, hand pose, and body pose detection.

![Alt Text](mp.gif)

To get started, create a new virtual environment with special indication this time:

```
pi@ixe00:~ $ virtualenv mpipe --system-site-packages
pi@ixe00:~ $ source mpipe/bin/activate
(mpipe) pi@ixe00:~ $ 
```

and install the following.

```
...
(mpipe) pi@ixe00:~ $ sudo apt install ffmpeg python3-opencv
(mpipe) pi@ixe00:~ $ sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23
(mpipe) pi@ixe00:~ $ pip3 install mediapipe-rpi4 pyalsaaudio
```

Each of the installs will take a while, please be patient. After successfully installing mediapipe, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the hand pose detection script we provide:
(***it will not work if you use ssh from your laptop***)


```
(mpipe) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(mpipe) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python hand_pose.py
```

Try the two main features of this script: 1) pinching for percentage control, and 2) "[Quiet Coyote](https://www.youtube.com/watch?v=qsKlNVpY7zg)" for instant percentage setting. Notice how this example uses hardcoded positions and relates those positions with a desired set of events, in `hand_pose.py` lines 48-53. 

**\*\*\*Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.\*\*\***

(You might also consider how this notion of percentage control with hand tracking might be used in some of the physical UI you may have experimented with in the last lab, for instance in controlling a servo or rotary encoder.)

![IMG_6853 2](https://user-images.githubusercontent.com/35357433/140796950-477a30b2-bc65-4239-9b0c-254429bfe47a.JPG)
![IMG_6854](https://user-images.githubusercontent.com/35357433/140796988-2b8475f6-f941-41f5-ba49-814a18e6eba8.JPG)
> I play the harp, and I think that this libary would be a wonderful tool to create an application where the system acts like a "hand position critique" and buzzes to let the user know every time the hand position is incorrect or the elbow / arm is slacking. The similar application would work for piano and some other instruments as well.
> It can also be used to simulate motion because it tracks the movement of different body parts (joints). One can use it to record a motion and put such motion on another object.
> The percengae control would be really useful in a mixed reality setting where the user can use their fingers to control things like volume, zoom, focus, etc..


#### Teachable Machines
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple. However, its simplicity is very useful for experimenting with the capabilities of this technology.

![Alt Text](tm.gif)

To get started, create and activate a new virtual environment for this exercise with special indication:

```
pi@ixe00:~ $ virtualenv tmachine --system-site-packages
pi@ixe00:~ $ source tmachine/bin/activate
(tmachine) pi@ixe00:~ $ 
```

After activating the virtual environment, install the requisite TensorFlow libraries by running the following lines:
```
(tmachine) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 5
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ sudo chmod +x ./teachable_machines.sh
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ ./teachable_machines.sh
``` 

This might take a while to get fully installed. After installation, connect your webcam to your Pi and use **VNC to access to your Pi**, open the terminal, and go to Lab 5 folder and run the example script:
(***it will not work if you use ssh from your laptop***)

```
(tmachine) pi@ixe00:~ Interactive-Lab-Hub/Lab 5 $ python tm_ppe_detection.py
```


(**Optionally**: You can train your own model, too. First, visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. Second, use the webcam on your computer to train a model. For each class try to have over 50 samples, and consider adding a background class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate, or export your model as a 'Tensorflow' model, and select 'Keras'. You will find an '.h5' file and a 'labels.txt' file. These are included in this labs 'teachable_machines' folder, to make the PPE model you used earlier. You can make your own folder or replace these to make your own classifier.)

**\*\*\*Whether you make your own model or not, include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.\*\*\***

![IMG_6857](https://user-images.githubusercontent.com/35357433/140797577-2a89431f-5f18-485a-97a0-1af534e4f22e.JPG)
> The TeachableMachines tool is extremely helpful to help building a classifier because it essentially does the classifying job for you. Its advantage over OpenCV or MediaPipe is that it can identify (supposedly) anything for you. On OpenCV and MediaPipe, one still has to analyze data and make classifications and predictions on their own. 
*Don't forget to run ```deactivate``` to end the Teachable Machines demo, and to reactivate with ```source tmachine/bin/activate``` when you want to use it again.*


#### Filtering, FFTs, and Time Series data. (optional)
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the accelerometer, try the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

**2. Set up averaging** Can you average your signal in N-sample blocks? N-sample running average?

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

**\*\*\*Include links to your code here, and put the code for these in your repo--they will come in handy later.\*\*\***


### Part B
### Construct a simple interaction.

Pick one of the models you have tried, pick a class of objects, and experiment with prototyping an interaction.
This can be as simple as the boat detector earlier.
Try out different interaction outputs and inputs.

**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***
The interaction that I am designing is a "rock, paper, scissor" game using the TeachableMachine library. User will play against a robot (raspberry pi). User will use their hand gesture to display their action, and the system will output a random gesture each time. The user score will start at 3 with every new game. Every time the user wins, the score increments, and every time they lose, the score decrements. If the user score goes below 1, user loses. If the user score goes to 15, the user wins. 

Here is an example of a losing game:
![Page1 4](https://user-images.githubusercontent.com/35357433/139748295-20aa19ac-6ca9-43fe-b27b-54b90384d570.jpg)
![Page2 4](https://user-images.githubusercontent.com/35357433/139748296-18373942-8b7d-4d01-8648-d0b6eedf971d.jpg)

Here is an example of a winning game:
![Page1 5](https://user-images.githubusercontent.com/35357433/139748334-7f40d072-6c3e-4224-9711-26463b55be43.jpg)
![Page2 5](https://user-images.githubusercontent.com/35357433/139748335-02e03ea1-24dc-448c-a6dc-fa149f917eb6.jpg)

### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it what it is supposed to do?
1. When does it fail?
1. When it fails, why does it fail?
1. Based on the behavior you have seen, what other scenarios could cause problems?

The first time that the tester lost to the system (raspberry pi), they thought that they lost the game completely. I had to later explain that they only lose the game completely once they have lost all of their points. Otherwise, the voice instruction helps, and the tester doesn't have issues navigating the game. The game is fairly simple so far, and "rock, paper, scissor" is a very universal and intuitive game.

However, one scenario that I have thought of that could cause problems is if someone doesn't know the game of "rock, paper, scissor", and put up a gesture that is not included as one of the three. The system does not recognize unfamiliar gestures yet. The system should either ask the user to try again or to use that as a losing case. Perhaps a game introduction to first time players would also help.

**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system?
> I am hoping that rock, paper, and scissor gestures are distinctive enough that there would be a smaller percentage of error. However, this should be communicated to the user so they are aware of their potential occasional random losses.
3. How bad would they be impacted by a miss classification?
> They can be fairly impacted by a miss classification, because their score would be impacted, and they can lose the game.
5. How could change your interactive system to address this?
> I am thinking that one of the buttons on the raspberry pi could be a revert button to revert a game if the gesture was incorrectly evaluated.
7. Are there optimizations you can try to do on your sense-making algorithm.
> It could be helpful for the machine to learn the gestures while the games are playing to improve its gesture identification accuracy. However, there might be some overhead from the machine performing analysis during the games, though.

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
> The game is meant to provide some interactive fun. It is a simple childhood game that is easy to understand and can help users relax in between work.
* What is a good environment for X?
> A well lit room would be a stellar room for the game. A clean background will also help a lot. These would help improving the classification accuracy.
* What is a bad environment for X?
> A bad environment would be somewhere dark or somewhere with a messy background. 
* When will X break?
> People do their rock, paper, and scissor gestures differently. If they do it differently than how the machine learned, the system might not understand and give a wrong prediction.
* When it breaks how will X break?
> The game will likely give a wrong prediction.
* What are other properties/behaviors of X?
> The camera resolution is quite low. I also trained the model using my computer camera instead of the webcam on the raspberry pi. The difference between the cameras might generate errors as well.
* How does X feel?
> The game is fairly simple and lightweight. It is pretty laggy, though. It could affect the user experience.
**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***
[Here is the link to me trying out the model. I tried to also see what the model would predict with just my head (no gestures).](https://youtu.be/8LGYaJlrDxE)

### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**\*\*\*Include a short video demonstrating the finished result.\*\*\***
