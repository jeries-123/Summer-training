this repository has a list of files containing codes for each sensor used in the smart beehive project and a core file containing all the sensors combined together. And the code for the website.
api.php receives the sensor readings from the flask application which can then be used in the website.
beez.py is the simple python program ran on raspberry pi before then implemented into flask.
calibrate.py is used to calibrate the weight sensor before measuring weight.
dht11.py is the code to measure temp and humidity
distance.py is used to measure distance before then adding treshold in the core program
light.py is used to detect light
measureweight.py is used to measure weight after the weight sensor has been calibrated with the calibrate.py program.
sendtourl.pi is the core flask program of the project which will record the sensor readings and send it to the api.php file to be used by the website.
sound.py is the code to detect sound.
