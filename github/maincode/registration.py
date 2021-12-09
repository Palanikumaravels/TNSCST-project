def reg():
    import time
    import cv2
    import busio
    import RPi.GPIO as GPIO 
    import time
    import pathlib
    import numpy as np
    from PIL import Image 
     
    from board import SCL, SDA
    from oled_text import OledText, Layout64, BigLine, SmallLine 
    from picamera import PiCamera
    from time import sleep
    GPIO.setmode(GPIO.BCM)


    GPIO.setup(19, GPIO.OUT)  
    pwm = GPIO.PWM(19, 100)   
    i2c = busio.I2C(SCL, SDA)


    oled = OledText(i2c, 128, 64)

    dc=0                              
    pwm.start(dc)                      
    camera = PiCamera()
    oled.layout = Layout64.layout_3medium_3icons()
    oled.text('ENTER NAME', 2)
    name=input('enter name')
    oled.layout = Layout64.layout_3medium_3icons()
    oled.text('NAME ENTERED:', 1)
    oled.text(name, 2)
    oled.text('\uf891', 5)
    time.sleep(3)
    oled.clear()
    #j=15
    oled.layout = Layout64.layout_icon_only()
    oled.text('\uf017', 1)
    for i in range(1):
        pwm.ChangeDutyCycle(90)
        camera.capture("/home/pi/Desktop/images//"+ name+"%s.jpg" % i)
        img = cv2.imread("/home/pi/Desktop/images//"+ name+"%s.jpg" % i,0)
        cropped_image = img[120:660, 200:705]
        cv2.imwrite("/home/pi/Desktop/images//"+name+"%s.jpg"% i, cropped_image)
    oled.layout = Layout64.layout_icon_only()
    oled.text('\uf00c', 1)
    time.sleep(1)
    oled.layout = Layout64.layout_3medium_3icons()
    oled.text('THANK YOU', 1)
    time.sleep(1)
    pwm.stop()                         
    GPIO.cleanup()
    camera.close()
    ok=1
    return(ok)
