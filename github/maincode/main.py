while True:
    import time
    import busio
    from board import SCL, SDA
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    from oled_text import OledText, Layout64, BigLine, SmallLine
    i2c = busio.I2C(SCL, SDA)
    # Instantiate the display, passing its dimensions (128x64 or 128x32)
    oled = OledText(i2c, 128, 64)
    from board import SCL, SDA
    import registration
    import black
    import poi
    import RPi.GPIO as GPIO
    
    import datetime, time
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
    GPIO.setwarnings(False)
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('mydata.json', scope) 
    client = gspread.authorize(creds)
    sheet = client.open("raspi_dataa").sheet1
    GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(21,GPIO.OUT)
    GPIO.output(21,GPIO.HIGH)

    
    i2c = busio.I2C(SCL, SDA)
    oled = OledText(i2c, 128,64)
    oled.layout = Layout64.layout_3medium_3icons()
    oled.text("1-SCAN", 1)
    oled.text("2-REGISTATION", 2)
    oled.text("3-RESET", 3)


    while True:
        button_state1 = GPIO.input(25)
        button_state2 = GPIO.input(24)
        button_state3 = GPIO.input(8)
        if button_state1 == False:
            print("reg")
            data1=registration.reg()
            print(data1)
            break
        elif button_state2 == False:
            print("scan")
            data2=black.finger()
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print(time)
            data = data2
            values =[time,data]
            sheet.append_row(values)
            print(data2)
            break
        elif button_state3 == False:
            print("reset")
            ok=poi.printer()
            print(ok)
            break
    GPIO.cleanup()

