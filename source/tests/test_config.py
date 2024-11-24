import sys
import os

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"

# Function to check if a library is installed
def check_library(library_name):
    """Check if a library is installed."""
    try:
        __import__(library_name)
        print(f"Library '{library_name}' is installed.")
        return True
    except ImportError:
        print(f"Library '{library_name}' is {COLOR_YELLOW}NOT{COLOR_RESET} installed.")
        return False

# List of required libraries
libraries = ["gpiozero", "RPi.GPIO", "board", "busio", "adafruit_ssd1306", "PIL"]
missing_libraries = []

print("\nChecking libraries...\n")
for lib in libraries:
    if not check_library(lib):
        missing_libraries.append(lib)

# Exit if any libraries are missing
if missing_libraries:
    print(f"\n{COLOR_RED}The following libraries are missing and need to be installed:{COLOR_RESET}")
    for lib in missing_libraries:
        print(f" - {COLOR_RED}{lib}{COLOR_RESET}")
    sys.exit("\nExiting script due to missing libraries.\n")
else:
    print(f"\n{COLOR_GREEN}All required libraries are installed.{COLOR_RESET}\n\nProceeding with the script...\n")

# Import verified libraries
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from gpiozero import Motor
import RPi.GPIO as GPIO
import time

print("\nLibraries imported successfully.")

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
 
# Function to test the i2c display
def test_i2c(screen_width=128, screen_height=64):
    """Test i2c connection and display functionality."""
    print("\nTesting display i2c connection...")

    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        disp = SSD1306_I2C(screen_width, screen_height, i2c)

        disp.fill(1)
        disp.show()
        print("Screen turned on. Waiting for 2 seconds...")
        time.sleep(2)

        disp.fill(0)
        disp.show()
        print("Screen turned off")

        print(f"{COLOR_GREEN}Screen is configured correctly{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_RED}Screen isn't configured correctly.{COLOR_RESET}\nError: {e}")

# Function to test fan functionality
def test_fan(cntrl_ain1=12, cntrl_ain2=13, cntrl_standby=22):
    """Test fan connection and control functionality."""
    print("\nTesting fan connection...")

    try:
        GPIO.setup(cntrl_standby, GPIO.OUT)
        
        # Use `with` statement for automatic cleanup with gpiozero Motor
        with Motor(cntrl_ain1, cntrl_ain2) as fan:
            GPIO.output(cntrl_standby, True)
            
            print("Running fan at half speed for 5 seconds...")
            fan.forward(0.5)
            time.sleep(5)

            print("Running fan at full speed for 5 seconds...")
            fan.forward(1)
            time.sleep(5)

            print(f"{COLOR_GREEN}Fan is configured correctly{COLOR_RESET}")

    except Exception as e:
        print(f"{COLOR_RED}Fan isn't configured correctly.{COLOR_RESET}\nError: {e}")


def test_files():
    directory = "/usr/local/share/temp_manager/"
    files = {"Font": "lucon.ttf", "Boot Logo": "raspberrypi_logo_inverted.bmp"}

    if not os.path.isdir(directory):
        print(f"\n{COLOR_RED}The directory {directory} does not exist.{COLOR_RESET}")
        print(f"Hint: Please create {directory} and place {files['Font']} and {files['Boot Logo']} into it.")
        print(f"Commands:")
        print(f"mkdir -p {directory}")
        print(f"cp ../fonts/{files['Font']} {directory}")
        print(f"cp ../images/{files['Boot Logo']} {directory}{COLOR_RESET}")
        return

    for file_name in files:
        file_path = os.path.join(directory, files[file_name])
        if os.path.isfile(file_path):
            print(f"\n{COLOR_GREEN}{file_name} is places correctly in {directory}{COLOR_RESET}")
        else:
            print(f"\n{COLOR_RED}{file_name} is missing.{COLOR_RESET}")
            source_hint = "fonts" if file_name == "Font" else "images"
            print(f"Hint: Please copy {files[file_name]} from 'repo'/source/{source_hint}/ to {directory}")
            print(f"Command: cp ../{source_hint}/{files[file_name]} {directory}{COLOR_RESET}")


# Main function
def main():
    """Main function to test fan and screen."""
    print("\nStarting tests for fan and screen...")
    test_i2c()
    test_fan()
    print("\nAll hardware tests completed.")
    print("\nChecking for essntial files...")
    test_files()
    print("\nAll tests are done")

# main() function calling
if __name__ == "__main__":
    main()
