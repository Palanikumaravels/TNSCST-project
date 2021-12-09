
def finger():
    x=1
    while (x==1):
        import numpy as np
        import cv2
        import glob
        import os
        import sys
        import time
        import busio
        import RPi.GPIO as GPIO
        from collections import OrderedDict
        from PIL import Image 

        from picamera import PiCamera
        from time import sleep
        from board import SCL, SDA
        from oled_text import OledText, Layout64, BigLine, SmallLine
        from matplotlib import pyplot as plt
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(19, GPIO.OUT)  
        pwm = GPIO.PWM(19, 100)   
        dc=0                              
        pwm.start(dc)          
        camera = PiCamera()
        i2c = busio.I2C(SCL, SDA)
        oled = OledText(i2c, 128, 64)
        oled.layout = Layout64.layout_3medium_3icons()

        oled.text("      WELCOME", 1)
        oled.text('         PLACE ', 2)
        oled.text('        FINGER', 3)
        time.sleep(1)
        oled.layout = Layout64.layout_icon_only()
        oled.text('\uf0a7', 1)
        time.sleep(2)
        oled.layout = Layout64.layout_icon_only()
        oled.text('\uf030', 1)
        time.sleep(2)

        p1=[]
        count=[]
        l1 = []
        i=1
        path = "/home/pi/Desktop/images/*.*"
        term={}
        nlist=[]
        nameoffile=[]
        pwm.ChangeDutyCycle(90)
        camera.capture('/home/pi/Desktop/image.jpg',0)
        img=cv2.imread('/home/pi/Desktop/image.jpg',0)
        cropped_image = img[120:660, 200:705]
        cv2.imwrite('/home/pi/Desktop/image.jpg',cropped_image )
        oled.layout = Layout64.layout_3medium_3icons()
        oled.text("    SCANNED", 1)
        oled.text('SUCCESSFULLY', 2)
        time.sleep(0.5)
        oled.clear()
        oled.layout = Layout64.layout_3medium_3icons()
        oled.text("PROCESSING...", 1)
        pwm.stop()
        camera.stop_preview()
        camera.close()

        for file in glob.glob(path):
            image_read = cv2.imread(file)
            #cv2.imshow('Color image', 0)
            MIN_MATCH_COUNT = 20
            names=glob.glob(file)
            filename_Absolute = os.path.basename(file)                 ## Now get the file name with os.path.basename
            #os.path.splitext(fileName)
            prt=os.path.splitext(filename_Absolute)[0]
            print(prt)
            nlist.append(prt)
           
            
            # queryImage
            img1 = cv2.imread('/home/pi/Desktop/image.jpg',0)
            #img2 = cv2.imread('3.bmp', 0) # trainImage
            img2=image_read
        # Initiate SIFT detector
            sift = cv2.xfeatures2d.SIFT_create()

        # find the keypoints and descriptors with SIFT
            kp1, des1 = sift.detectAndCompute(img1,None)
            kp2, des2 = sift.detectAndCompute(img2,None)



            FLANN_INDEX_KDTREE = 0
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 12)
            search_params = dict(checks = 200)

            flann = cv2.FlannBasedMatcher(index_params, search_params)

            matches = flann.knnMatch(des1, des2, k=2)


        # store all the good matches as per Lowe's ratio test.
            good = []
            for m,n in matches:
                if m.distance < 0.7*n.distance:
                    good.append(m)
                   
                   
                   
            if len(good)>MIN_MATCH_COUNT:
                src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
                dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
                matchesMask = mask.ravel().tolist()

                h,w, = img1.shape
                pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts,M)

                img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
               
               

            else:
                print ("%d/%d" % (len(good),MIN_MATCH_COUNT))
               
                matchesMask = None

            draw_params = dict(matchColor = (255,0,0), # draw matches in green color
                            singlePointColor = None,
                            matchesMask = matchesMask, # draw only inliers
                            flags = 2)
             
            img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
            
           
            l1.append(len(good))
            print(l1)
            #plt.imshow(img3, 'gray'),plt.show()    
        print("before",l1)
        p1=l1.copy()
        print(nlist)
        res = {}
        for key in nlist:
            for value in l1:
                res[key] = value
                l1.remove(value)
                break
        print(res)
        term=(sorted(res.items(), key =lambda kv:(kv[1], kv[0])))  
        kx = max(zip(res.values(), res.keys()))[1]
        print(term[-1])
        
        p1.sort(reverse=True)
        comp=p1[0]
        print(comp)
        print("after sorted")
        print(kx)
        time.sleep(2)
        if comp<10:
            oled.layout = Layout64.layout_icon_only()
            oled.text('\uf235', 1)
            time.sleep(1)
            oled.clear()
            oled.layout = Layout64.layout_1big_center()
            oled.text("    TRY ", 1)
            time.sleep(0.2)
            oled.clear()
            oled.layout = Layout64.layout_1big_center()
            oled.text("    AGAIN ", 1)
            time.sleep(0.2)
            k=1
            return(k)
        elif comp>=10:
            oled.layout = Layout64.layout_icon_only()
            oled.text('\uf4fc', 1)
            time.sleep(2)
            oled.layout = Layout64.layout_1big_center()
            oled.text('THANKS', 1)
            oled.text(kx, 1)
            time.sleep(2)
            return(kx)
        GPIO.cleanup()                    








