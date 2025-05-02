# wake-on-lan-sms-pi

#Steps to config SIM7600e h on rpi 4B:
1. ssh into your rpi
2. sudo raspi-config
  Here get into interface options (3), then serial port (6), login shell to be accessible over serial? - NO, serial port hardware to be enabled? YES,
3. sudo reboot

# Wake on Lan configuration using provided .sh file (automatic)
Assuming newly installed linux OS:
1. sudo apt update
2. udo apt install git
3. mkdir wol
4. cd wol
5. git clone https://github.com/AlexSzczygielski/wake-on-lan-sms-pi.git
6. cd wake-on-lan-sms-pi/
7. chmod +x setup_wol_sms.sh
8. ./setup_wol_sms.sh


# Steps to manually configure wake on lan (after GSM module is up and running)
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
