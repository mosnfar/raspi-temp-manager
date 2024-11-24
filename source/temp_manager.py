#!/usr/bin/python

# Setting up libraries
from gpiozero import Motor
import RPi.GPIO as GPIO
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont
import time
import subprocess
import re
import os



# ------ FAN CONFIG ------

# Set fan contoroler pins
cntrl_ain1 = 12
cntrl_ain2 = 13
cntrl_standby = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(cntrl_standby, GPIO.OUT)
fan = Motor(cntrl_ain1, cntrl_ain2)



# ------ DISPLAY CONFIG ------

# Setup I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Setup display (SSD136 module)
screen_width = 128
screen_height = 64 
display = SSD1306_I2C(screen_width, screen_height, i2c)

# Test display
display.fill(0)
display.show()

# Create blank canvas using Pillow Library
width = display.width
height = display.height
canvas = Image.new('1', (width, height), color=0)

# Setup draw command
draw = ImageDraw.Draw(canvas)

# Setup custom font (custom font = Lucida Console font, 12px Size)
font_path = "/usr/local/share/temp_manager/lucon.ttf"
if os.path.exists(font_path):
    font = ImageFont.truetype(font_path, 12)
else:
    font = ImageFont.load_default()



# ----- SETTING FUNCTIONS -----

def boot_screen(interval_loading=1):
    """ Show boot screen until system booted """

    # Logo Config
    logo_path = "/usr/local/share/temp_manager/raspberrypi_logo_inverted.bmp"
    logo = Image.open(logo_path).resize((32, 32), Image.LANCZOS).convert("1")

    for i in range(1, 4):

        canvas.paste(0, (0, 0, width, height))
        display.fill(0)
        display.show()        

        canvas.paste(logo, (48, 8))
        draw = ImageDraw.Draw(canvas)

        dots = "." * i
        x_position = 64 - (4 * i)
        draw.text((x_position, 42), dots, font=font, fill=255)

        display.image(canvas)
        display.show()

        time.sleep(interval_loading)


def is_system_booted():
    """ Check for system is booted """
    try:
        result = subprocess.run(["systemctl", "is-system-running"], capture_output=True, text=True, check=True)
        # Return True if is booted
        return result.stdout.strip() == "running"
    except subprocess.CalledProcessError:
        # Return False if is not booted
        return False

def get_temps():
    """ Get CPU & GPU temperature """
    try:
        raw_gpu_result = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True, check=True)
        gpu_temp_match = re.search(r'temp=(\d+\.\d+)', raw_gpu_result.stdout)
        if gpu_temp_match:
            gpu_temp = float(gpu_temp_match.group(1))
        else:
            return None
    except subprocess.CalledProcessError:
        return None
    
    try:
        raw_cpu_result = subprocess.run(["cat", "/sys/class/thermal/thermal_zone0/temp"], capture_output=True, text=True, check=True)
        cpu_temp = float(raw_cpu_result.stdout) / 1000
    except subprocess.CalledProcessError:
        return None
    
    return {
        # Return temperatures as float numbers
        "cpu": cpu_temp,
        "gpu": gpu_temp
    }

def get_uptime():
    """ Get system uptime """
    try:
        result = subprocess.run(["uptime", "-p"], capture_output=True, text=True, check=True)
        uptime_str = result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    
    days = hours = minutes = 0

    day_match = re.search(r'(\d+)\s+days?', uptime_str)
    hour_match = re.search(r'(\d+)\s+hours?', uptime_str)
    minute_match = re.search(r'(\d+)\s+minutes?', uptime_str)

    if day_match:
        days = int(day_match.group(1))
    if hour_match:
        hours = int(hour_match.group(1))
    if minute_match:
        minutes = int(minute_match.group(1))

    return {
        # Return uptime days, hours, minutes as array
        "days": days,
        "hours": hours,
        "minutes": minutes
    }



def check_network():
    """ Get network status by attempt to ping Google CDN (8.8.8.8)"""
    try:
        response = subprocess.run(["ping", "-c", "1", "-W", "2", "8.8.8.8" ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Return UP if internet is connected and DOWN otherwise
        if response.returncode == 0:
            return "UP"
        else:
            return "DOWN"
        
    except subprocess.SubprocessError:
        return "DOWN"


def temp_checker():
    """ Check maximum temperature and return fan speed mode """
    
    local_temps = get_temps()

    FAN_SPEEDS = {
        "QUIET": 0.0,
        "ECHO": 0.3,
        "AIRING": 0.6,
        "TURBO": 1.0,
        "OVERHEAT": 1.0
    }
    
    MAX_TEMP = max(local_temps["cpu"], local_temps["gpu"])

    if MAX_TEMP < 40:
        mode = "QUIET"
        active = False
    elif MAX_TEMP < 45:
        mode = "ECHO"
        active = True
    elif MAX_TEMP < 60:
        mode = "AIRING"
        active = True
    elif MAX_TEMP < 80:
        mode = "TURBO"
        active = True
    else:
        mode = "OVERHEAT"
        active = True

    fan_speed = FAN_SPEEDS[mode]

    return {
        # Return fan mode and speed based on max temp
        "mode": mode,
        "fan_speed": fan_speed,
        "max_temp": MAX_TEMP,
        "fan_active": active
    }



def main():
    """ Loop for main script function """

    while not is_system_booted():
        # Load boot screen until system is booted
        boot_screen()
        time.sleep(1)

    while True:

        # Store function result data
        uptime_data = get_uptime()
        fan_data = temp_checker()
        network_data = check_network()
        temp_data = get_temps()

        # Clear screen
        canvas.paste(0, (0, 0, width, height))
        display.fill(0)
        display.show()

        # Set data in screen canvas
        draw.text((0, 0), "Up: " + str(uptime_data["days"]) + "d " + str(uptime_data["hours"]) + "h " + str(uptime_data["minutes"]) + "m", font=font, fill=255)
        draw.text((0, 12), "Network: " + network_data, font=font, fill=255)
        draw.text((0, 24), "Fan: " + fan_data['mode'], font=font, fill=255)
        draw.text((0, 36), "CPU: ", font=font, fill=255)
        draw.text((64, 36), "GPU: ", font=font, fill=255)
        draw.text((0, 48), str(round(temp_data["cpu"],1)) + "°C", font=font, fill=255)
        draw.text((64, 48), str(round(temp_data["gpu"],1)) + "°C", font=font, fill=255)

        # Show canvas on screen
        display.image(canvas)
        display.show()

        # Set fan contoroler STNDBY pin
        GPIO.output(cntrl_standby, fan_data["fan_active"])
        # Run fan based on fan setup
        fan.forward(fan_data['fan_speed'])

        time.sleep(10)

# main() function calling
if __name__ == "__main__":
    main()