# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal
# mish mash of code from wipy documentation and forums

from network import WLAN
import time
import os
import machine

# Substitute your wifi network name & password
SSID = 'My-wifi-network'
AUTH = (WLAN.WPA2, 'My-wifi-password')

# duplicate terminal on USB-UART                     
uart = machine.UART(0, 115200)
os.dupterm(uart)

# Try connecting in station mode
wlan = WLAN(mode=WLAN.STA)
wlan.ifconfig(config='dhcp')
wlan.connect(ssid=SSID, auth=AUTH)

# Try for 30 seconds
retry = 60
while not wlan.isconnected():
    if retry > 0:
        time.sleep_ms(500)
        print('.', end='')
        retry = retry - 1
    else:
        break
      
# If connected print ipaddr and info    
if wlan.isconnected():
    print('Connected to My-wifi-network\n')
    ip, mask, gateway, dns = wlan.ifconfig()
    print('IP address: ', ip)
    print('Netmask:    ', mask)
    print('Gateway:    ', gateway)
    print('DNS:        ', dns)
    if machine.reset_cause() != machine.SOFT_RESET:
        # Copy https://github.com/andrewmk/untplib/blob/master/untplib.py to \flash\lib on wipy
        import untplib
        from machine import RTC
        rtc = RTC()
        c=untplib.NTPClient()
        resp=c.request('1.fr.pool.ntp.org', version=3, port=123)
    rtc.init(time.localtime(time.time() + resp.offset))
    print("Current time", time.localtime())
else:
    wlan.init(mode=WLAN.AP, ssid='wipy-wlan', auth=(WLAN.WPA2,'www.wipy.io'), channel=7, antenna=WLAN.INT_ANT)