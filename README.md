# wake-on-lan-sms-pi

#Steps to config SIM7600e h on rpi 4B:
1. ssh into your rpi
2. sudo raspi-config
  Here get into interface options (3), then serial port (6), login shell to be accessible over serial? - NO, serial port hardware to be enabled? YES,
3. sudo reboot

#Steps to configure wake on lan (after GSM module is up and running)
1. sudo apt update
2. (optional - if you want to debug) sudo apt-get install minicom
3. python --version (check if you have python installed)
4. sudo apt install python3-pip -y (if not already installed) !!!!
5. pip3 install pyserial !!!!!!
6. sudo apt-get install python3-serial
7. sudo apt install git
8. mkdir wol
9. cd wol
10. git clone https://github.com/AlexSzczygielski/wake-on-lan-sms-pi.git
11. cd wake-on-lan-sms-pi/
12. nano config.ini (fill it with required data and save)
13. nano smsWake.py
14. Here change line: config.read('/home/pi/Desktop/config.ini'), Change this to your file path (line 27), save and exit
15. (optional) python smsWake.py - check if the file compiles correctly
16. cd ~
17. crontab -e
18. @reboot python /home/pi/Desktop/smsWake.py' (Add this at the end of crontab file, change this to your file path, save and exit)
19. sudo reboot

After that the python script should automatically start, every time the RPi turns on. To check if it runs you can use:
ps aux|grep python

To see what happens at the serial port you can use minicom:
minicom -D /dev/ttyS0 (may need to adjust port)
