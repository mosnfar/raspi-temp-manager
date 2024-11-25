# RasPi Temp Manager

A comparative tool and hardware setup for Raspberry Pi (RasPi) to manage temperature and monitor essential information.

This repository outlines a project designed to enhance the thermal management and monitoring capabilities of a Raspberry Pi 4 housed in an Argon NEO case. The project combines hardware modifications and custom software to provide effective cooling and real-time system monitoring through a small OLED display.

> [!NOTE]
> You can read the complete instructions on [The Forge blog](https://forge.mosn.me/keeping-your-raspberry-pi-cool-a-temperature-manager-tool).

<table style="width: 100%;">
  <tr>
    <th style="text-align: left;"> Final Product </th>
    <th style="text-align: left;"> Demo Video </th>
  </tr>
  <tr>
    <td><img src="/assets/images/device_final_preview.jpg" alt="Image of final product" width="300"></td>
    <td><a href="https://www.youtube.com/watch?v=cTe1wpACoGw"><img src="https://img.youtube.com/vi/cTe1wpACoGw/0.jpg" alt="Image of final product" width="300"></a></td>
  </tr>
</table>

---

Table of contents:

<!-- TOC depthfrom:2 depthto:3 -->

- [Features](#features)
- [Hardware](#hardware)
    - [Hardware Components](#hardware-components)
    - [Schematic](#schematic)
- [3D Case](#3d-case)
- [Software](#software)
- [More Information](#more-information)
    - [Image Gallery](#image-gallery)
    - [Complete Instruction](#complete-instruction)
    - [Contribution](#contribution)

<!-- /TOC -->

---

## Features
- **Dynamic Cooling**: Automatically adjusts the fan speed according to system temperature thresholds.
- **Real-Time Monitoring**: Displays key metrics like:
  - CPU & GPU temperature
  - Network status
  - System overview
- **Compact Design**: Retains the Argon NEO case's form factor with minimal modifications.

## Hardware

### Hardware Components

1. **128×64 px OLED Display (SSD1306):** Uses I2C protocol to display system metrics, including temperature, system, and network status.
2. **Miniature 5V Fan:** Provides active cooling to maintain optimal system temperature.
3. **DRV8833 Dual Motor Driver:** Controls the 5V fan with PWM for precise speed adjustments.
4. **Raspberry Pi 4:** Serves as the mainboard.

### Schematic

Here is the schematic for connecting all components to the Raspberry Pi GPIO.

![Schematic Diagram](/assets/images/diagram.png)

#### DRV8833 Driver ←→ Rasberry Pi
| *DRV8833* | *Raspberry Pi 4 GPIO* |
| --- | --- |
| AIN1 | GPIO13 |
| AIN2 | GPIO12 |
| VM | 5V (Pin #4) |
| GND | GND (Pin #6) |
| STBY | GPIO27 |

#### 5V Fan ←→ DRV8833 Driver
| *5V Fan* | *DRV8833 Driver* |
| --- | --- |
| 5V (RED) | AIO1 |
| GND (BLACK) | AIO2 |

#### OLED (SSD1306) ←→ Raspberry Pi
| *OLED - SSD1306* | *Raspberry Pi 4 GPIO* |
| --- | --- |
| VCC | 3v3 (Pin #1) |
| SDA | GPIO2 |
| SCL | GPIO3 |
| GND | GND (Pin #9) |



## 3D Case

![Image of 3D printed part](/assets/images/image_of_3d_print.jpg)

I used the [Argon NEO Case](https://argon40.com/products/argon-neo-case-for-raspberry-pi-4) for my raspberry pi 4 and I modified this case to place the components. You can find the 3D design file in the [`./3d-files` directory](/3d-files/) or through this [link](https://www.printables.com/model/1085113-rascase-raspberry-pi-argon-neo-case-add-on). You can also 3D print any other case of your choice to house the components. 

## Software

#### 01. Clone Repository

Clone the repository into your raspberry pi:

```bash
git clone https://github.com/mosnfar/raspi-temp-manager
```

#### 02. Install Requirements

To run this script you need these libraries gpiozero, Pillow(PIL), and adafruit_ssd1306 that are not in raspberry pi, install requirements libraries:

```bash
pip install -r requirements.txt
```

> [!TIP]
> If you are using a newer version of Python, install the libraries globally rather than in a virtual environment.

#### 03. Copy essential files

You should copy essential files "font and boot lofo" to `/usr/local/share`, use the following command:

```bash
mkdir -p /usr/local/share/temp_manager
cp ./fonts/lucan.ttf /usr/local/share/temp_manager
cp ./images/raspberrypi_logo_inverted.bmp /usr/local/share/temp_manager
```

#### 04. Test Configs

You can test everything to make sure configs are working correctly by running `test_config.py` to check "Required libraries installation", "I2C connection", "Fan connection", and "Essential files". You can run test by this:

```bash
python test_config.py
```

#### 05. Configure Boot Script

After successful testing, configure a service to add that into system boot and the script will be running at startup. First copy `temp_manager.py` script into `/usr/local/bin`:

```bash
sudo cp ./source/temp_manager.py /usr/local/bin/
```

Now add new service for temperature manager:

```bash
sudo nano /etc/systemd/system/temp_manager.service
```

And add content below to service file:

```
[Unit]
Description=Temperature Manager
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/temp_manager.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Finally enable and start the service to run at startup:

```bash
sudo systemctl enable temp_manager.service
sudo systemctl start temp_manager.service
```

**:smiley: Awesome, everything is set up perfectly and should work great!**


## More Information

### Image Gallery
Here are some images that highlight the project:
<table>
    <tr>
        <td align="center">
            <figure>
                <img src="/assets/images/measuring_case.jpeg" style="width: 100%;" alt="Image">
                <figcaption>Measuring Case</figcaption>
            </figure>
        </td>
        <td align="center">
            <figure>
                <img src="/assets/images/soldering_components.jpeg" style="width: 100%;" alt="Image">
                <figcaption>Soldering Components</figcaption>
            </figure>
        </td>
        <td align="center">
            <figure>
                <img src="/assets/images/component_preview.jpeg" style="width: 100%;" alt="Image">
                <figcaption>Component Preview</figcaption>
            </figure>
    </tr>
    <tr>
        <td align="center">
            <figure>
                <img src="/assets/images/glue_magnets.jpeg" style="width: 100%;" alt="Image">
                <figcaption>Glue Magnets</figcaption>
            </figure>
        </td>
        <td align="center">
            <figure>
                <img src="/assets/images/connection.jpeg" style="width: 100%;" alt="Image">
                <figcaption>Connection Preview</figcaption>
            </figure>
        </td>
        <td align="center">
            <figure>
                <img src="/assets/images/assembled.jpeg" style="width: 100%;" alt="Image">
                <figcaption>Assembled Product</figcaption>
            </figure>
        </td>
    </tr>
</table>

### Complete Instruction
I wrote a complete guide and instructions on my blog "The Forge" you can read it through [this link](https://forge.mosn.me/keeping-your-raspberry-pi-cool-a-temperature-manager-tool).

### Contribution
Feel free to customize and improve the project however you'd like! Your contributions are always welcome, and together we can make it even better. Don't hesitate to jump in and help out! 😊
