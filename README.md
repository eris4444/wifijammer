# WiFi Jammer  ERIS

WiFi Jammer is a Python script designed for ethical hacking and security research purposes.

#youtube video

https://youtu.be/FLR-lLb6Kjk?si=N_Ol1fQsi7PKrnJR

# Installation Requirements

- aircrack-ng
- python3
- python3-pip


## Features

- **Monitor Mode Setup:** airmon-ng start wlanX
- **WiFi Scanning:** select your WiFi adapter to start snanning.
- **Deauthentication Attack:** Launches a deauthentication attack on a selected WiFi network.
- **User Disconnection:** Disconnects all users connected to the targeted WiFi network temporarily.
- **User-Friendly:** Simple and interactive script with easy-to-follow instructions.

## Installation

To use WiFi Jammer, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/eris4444/wifijammer
    ```
2. Change to the project directory:

    ```bash
    cd wifiJammer
    ```
3. Run the script with elevated privileges:

    ```bash
    sudo python3 wifideauth.py
    ```
    ## Usage

Once you have executed the script, follow the on-screen instructions:

1. Select your WiFi adapter for monitor mode setup.
2. Scan for available WiFi networks.
3. Choose a target WiFi network for the deauthentication attack.
4. Initiate the deauthentication attack.
5. Press `Ctrl+C` to stop the attack.

**Note:** This tool is intended for educational and research purposes only. Ensure that you have the necessary permissions before using it.

## Disclaimer

The author is not responsible for any misuse or damage caused by this script. Use it responsibly and only in environments where you have explicit authorization.
