import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

##import RPi.GPIO as GPIO
##import time
##
##GPIO.setmode(GPIO.BCM)
##GPIO.setup(3, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.HIGH)
##
##GPIO.output(3, GPIO.LOW)
##GPIO.output(21, GPIO.LOW)
##
##GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##
##while True:
##    input_state = GPIO.input(20)
##    if input_state == False:
##        break
##
##for x in range(10):
##    GPIO.output(3, GPIO.LOW)
##    GPIO.output(21, GPIO.HIGH)
##    time.sleep(1)
##    GPIO.output(3, GPIO.HIGH)
##    GPIO.output(21, GPIO.LOW)
##    time.sleep(1)
##    
##GPIO.output(3, GPIO.LOW)
##GPIO.output(21, GPIO.LOW)