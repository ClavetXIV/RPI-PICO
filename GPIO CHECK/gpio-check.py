import machine
import time

# Definice testovacích dvojic (Pin A, Pin B)
PIN_PAIRS = [
    (0, 1), (2, 3), (4, 5), (6, 7), (8, 9),
    (10, 11), (12, 13), (14, 15), (16, 17),
    (20, 21), (22, 26), (27, 28)
]

def test_pair(p_out, p_in):
    # Nastavení: jeden ven, druhý dovnitř s pull-downem
    out_pin = machine.Pin(p_out, machine.Pin.OUT)
    in_pin = machine.Pin(p_in, machine.Pin.IN, machine.Pin.PULL_DOWN)
    
    success = True
    
    # Test logické 1
    out_pin.value(1)
    time.sleep_ms(5)
    if in_pin.value() != 1:
        success = False
        
    # Test logické 0
    out_pin.value(0)
    time.sleep_ms(5)
    if in_pin.value() != 0:
        success = False
        
    return success

print("=" * 40)
print("   HARDWAROVÁ DIAGNOSTIKA GPIO PINŮ   ")
print("=" * 40)
print("Ujisti se, že máš zapojené dráty v dvojicích!\n")
time.sleep(1)

all_ok = True

for p1, p2 in PIN_PAIRS:
    # Směr A -> B
    res_a = test_pair(p1, p2)
    # Směr B -> A
    res_b = test_pair(p2, p1)
    
    if res_a and res_b:
        print(GEN_STATUS := f"Dvojice GP{p1} <-> GP{p2}: [ V POŘÁDKU ]")
    else:
        all_ok = False
        status_a = "OK" if res_a else "CHYBA"
        status_b = "OK" if res_b else "CHYBA"
        print(f"Dvojice GP{p1} <-> GP{p2}: [ POŠKOZENO ]")
        print(f"  -> Směr GP{p1} na GP{p2}: {status_a}")
        print(f"  -> Směr GP{p2} na GP{p1}: {status_b}")

print("\n" + "=" * 40)
if all_ok:
    print("VÝSLEDEK: Všechny testované piny jsou 100% ZDRAVÉ!")
else:
    print("VÝSLEDEK: Detekovány vadné piny. Viz report výše.")
print("=" * 40)
