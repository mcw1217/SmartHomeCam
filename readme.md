## Introduction

- This project was produced based on the fall detection paper published in 2023.
- The program detects human fall in real time. In addition, the program itself supports the website, so you can access the website from anywhere and check the Cam at home.
- fall detected in real time are notified to the user's mobile phone registered ion the website. ( Currently, it is replaced with Line because it does not have its own mobile app )
- It was confirmed through experiments that this program runs on low-end hardware. Therefore, when actual products are launched, they have an advantage in price competition.
  

## One Touch Install and Run
1. After downloading the mysql database from the link below, put it in the main directory of the project.
2. You just need to run the install.exe program
3. Then python and mysql service wiil be installed automatically.
4. Once the installation is complete, SmartHomeCam will run if you run install.exe from then on.

### [!] Install Mysql database link
https://drive.google.com/file/d/11xw8XUPPMWz_babnNe7B2qriffAxANgG/view?usp=drive_link


## Using Skills
- Parameters: Time and Direction to reach fall
- Deep Learning: Mediapipe, GRU 

- Mediapipe: After extracting the coordinates of the human joint using the mediapie, we obtained the rotation ange using it.

- GRU: The extraced joint coordinates, rotation angle, time and direction of fall were made into one data and the data was trained on the GRU model.


*** For more details on fall detection, please check the paper! ***

