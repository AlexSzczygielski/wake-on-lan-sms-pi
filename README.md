# Wake-on-Lan via SMS using RaspberryPi

Remotely wake on your home computer or NAS using an SMS message. <br>
**This script allows sending magic packet inside your LAN network, without opening any of it's ports to the public.** <br>

This project uses RaspberryPi 4B with Waveshare SIM7600E-H Hat GSM module (https://www.waveshare.com/wiki/SIM7600E-H_4G_HAT).

## Issue genesis

As an EE engineering student I often need to use Windows machine to run specific software, however my favourite and most used computer is a Macbook that runs on MacOS.<br> **Solution?** <br> 
Leave Windows machine at home and run remote desktop to access it and do work anywhere, from my macbook laptop. <br>
**However, a new problem arises:** <br>
Leaving my PC always on would lead to immense power consumption over time, as well as faster component wear. <br>
**Solution II?** <br>
Turn on my Windows remotely by sending magic packet to it's mac address. The most common way to do that would be to set up a VPN, open a communication port and access my LAN network remotely. <br>
**But this action poses a serious security threat, as opening your LAN to the internet means two things:**
- Difficult configuration - correctly setting DHCP, opening network port, generating SSH key for safe communication, mocking a static public IP (as most home networks don't have a static public IP)
- **Exposing your LAN for dangerous attacks** - there are malicious bots that scan WAN in search for open networks, try breaking into them and then can pose **serious attacks, like e.g Man in the Middle attack**. Not correctly configure open LAN can mean not only unwanted users inside your LAN, attacks on devices in your home network, but also a threat for your passwords, bank accounts, etc.<br>

While opening your LAN and making a vpn might have sense when you need to remotely access files, servers, etc. it doesn't make sense when the only thing that needs remote access is sending a magic packet to wake on your PC. **This is, where my project comes in handy as it allows to send WOL packets, without opening your network.**

# How does it work?

## Steps to config SIM7600e h on rpi 4B:
1. ssh into your rpi
2. sudo raspi-config
  Here get into interface options (3), then serial port (6), login shell to be accessible over serial? - NO, serial port hardware to be enabled? YES,
3. sudo reboot

## Wake on Lan configuration using provided .sh file (automatic)
Assuming newly installed linux OS:
1. sudo apt update
2. udo apt install git
3. mkdir wol
4. cd wol
5. git clone https://github.com/AlexSzczygielski/wake-on-lan-sms-pi.git
6. cd wake-on-lan-sms-pi/
7. chmod +x setup_wol_sms.sh
8. ./setup_wol_sms.sh


## Steps to manually configure wake on lan (after GSM module is up and running)
1. sudo apt update
2. (optional - if you want to debug) sudo apt-get install minicom
3. sudo apt install wakeonlan
4. python --version (check if you have python installed)
5. sudo apt install python3-pip -y (if not already installed) !!DElete!!!
6. pip3 install pyserial !!!Delete!!!
7. sudo apt-get install python3-serial
8. sudo apt install git
9. mkdir wol
10. cd wol
11. git clone https://github.com/AlexSzczygielski/wake-on-lan-sms-pi.git
12. cd wake-on-lan-sms-pi/
13. nano config.ini (fill it with required data and save)
14. nano smsWake.py
15. Here change line: config.read('/home/pi/Desktop/config.ini'), Change this to your file path (line 27), save and exit
16. (optional) python smsWake.py - check if the file compiles correctly
17. cd ~
18. crontab -e
19. @reboot python /home/pi/Desktop/smsWake.py' (Add this at the end of crontab file, change this to your file path, save and exit)
20. sudo reboot

After that the python script should automatically start, every time the RPi turns on. To check if it runs you can use:

ps aux|grep python

To see what happens at the serial port you can use minicom:

minicom -D /dev/ttyS0 (may need to adjust port)

Remeber that when you use minicom, the serial port will be occupied by it, so magic packet won't be send.
