import hid_keymap
import fuggvenyek
from machine import Pin
from time import sleep
import usb.device
import touchpad_ps2
from usb.device.keyboard import KeyboardInterface
from usb.device.mouse import MouseInterface

sorok=[Pin(10, Pin.IN, Pin.PULL_UP),Pin(12, Pin.IN, Pin.PULL_UP)]
oszlopok=[Pin(13, Pin.OUT), Pin(11, Pin.OUT)]

kbd = KeyboardInterface()
eger = MouseInterface()
usb.device.get().init(kbd, eger, builtin_driver=True)

while not kbd.is_open() or not eger.is_open():
    sleep(0.1)

keymap=fuggvenyek.keymap_betoltes("keymap.txt")

elozo_bal_gomb = False 
elozo_jobb_gomb = False
elozo_kozepso_gomb = False

elozo_allapot = []

def touchpad_eredmeny_kuldes(eger, eredmeny):
    global elozo_bal_gomb, elozo_jobb_gomb, elozo_kozepso_gomb
    
    bal_gomb, jobb_gomb, kozepso_gomb, x, y = eredmeny
    
    if elozo_bal_gomb != bal_gomb:
        eger.click_left(bal_gomb)
        elozo_bal_gomb = bal_gomb
    if elozo_jobb_gomb != jobb_gomb:
        eger.click_right(jobb_gomb)
        elozo_jobb_gomb = jobb_gomb
    if elozo_kozepso_gomb != kozepso_gomb:
        eger.click_middle(kozepso_gomb)
        elozo_kozepso_gomb = kozepso_gomb
    if x is not None and y is not None:
        x = max(-127, min(x, 127))
        y = max(-127, min(y, 127))
        eger.move_by(x, y)
        

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
    eredmenyek = touchpad_ps2.touchpad_frissites()
    for eredmeny in eredmenyek:
        touchpad_eredmeny_kuldes(eger, eredmeny)










