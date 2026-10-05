from time import sleep_us

def scan_matrix(sorok, oszlopok):
    koordinatak=[]
    for elem in oszlopok:
        elem.value(1)
    for oszlop_index, oszlop_ertek in enumerate(oszlopok):
        oszlop_ertek.value(0)
        sleep_us(10)
        for sor_index, sor_ertek in enumerate(sorok):
            if sor_ertek.value() == 0:
                koordinatak.append((sor_index,oszlop_index))
        oszlop_ertek.value(1)
    return koordinatak



def compare_states(aktualis_allapot, elozo_allapot):
    elozo_halmaz=set(elozo_allapot)
    aktualis_halmaz=set(aktualis_allapot)
    lenyomas=list(aktualis_halmaz-elozo_halmaz)
    felengedes=list(elozo_halmaz-aktualis_halmaz)
    return lenyomas,felengedes


def esemenyek_feldolgozasa(lenyomas, felengedes, keymap):
    lenyomott=[]
    felengedett=[]
    for koordinata in lenyomas:
        billentyu=keymap.get(koordinata)
        if billentyu is not None:
            lenyomott.append(billentyu)
    for koordinata in felengedes:
        billentyu=keymap.get(koordinata)
        if billentyu is not None:
            felengedett.append(billentyu)
    return lenyomott, felengedett


def hid_allapot_keszit(aktualis_allapot, keymap, hid_keymap):
    aktualis_billentyu=[]
    aktualis_hid = []
    for koordinata in aktualis_allapot:
        if keymap.get(koordinata) is not None:
            aktualis_billentyu.append(keymap[koordinata])
    for billentyu in aktualis_billentyu:
        if hid_keymap.get(billentyu) is not None:
            aktualis_hid.append(hid_keymap[billentyu])
    return aktualis_hid

def keymap_mentes(keymap, fajlnev):
    with open(fajlnev, "w") as fajl:
        for koordinata, billentyu in keymap.items():
            fajl.write(f"{koordinata[0]},{koordinata[1]},{billentyu}\n")
            

def keymap_betoltes(fajlnev):
    keymap = {}
    with open(fajlnev, "r") as fajl:
        for sor in fajl:
            if sor.strip() != "":
                adatok = sor.strip().split(",",2)
                try:
                    keymap[(int(adatok[0]), int(adatok[1]))] = adatok[2]
                except ValueError:
                    print("Hibás koordináta a fájlban.")
                except IndexError:
                    print("Hiányos sor a fájlban.")
    return keymap