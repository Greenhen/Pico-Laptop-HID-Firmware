import hid_keymap
import fuggvenyek
from machine import Pin
from time import sleep
import usb.device
from usb.device.keyboard import KeyboardInterface

sorok=[Pin(14, Pin.IN, Pin.PULL_UP),Pin(12, Pin.IN, Pin.PULL_UP)]
oszlopok=[Pin(13, Pin.OUT), Pin(11, Pin.OUT)]

kbd = KeyboardInterface()
usb.device.get().init(kbd, builtin_driver=True)

while not kbd.is_open():
    sleep(0.1)

keymap=fuggvenyek.keymap_betoltes("keymap.txt")

elozo_allapot = []

while True:
    aktualis_allapot=fuggvenyek.scan_matrix(sorok, oszlopok)
    aktualis_hid=fuggvenyek.hid_allapot_keszit(aktualis_allapot, keymap, hid_keymap.hid_keymap)
    lenyomas,felengedes=fuggvenyek.compare_states(aktualis_allapot, elozo_allapot)
    if len(lenyomas)!=0 or len(felengedes)!=0:
        sleep(0.01)
        masodik_meres = fuggvenyek.scan_matrix(sorok, oszlopok)
        if aktualis_allapot == masodik_meres:
            kbd.send_keys(aktualis_hid)
            elozo_allapot=masodik_meres
    










