from machine import Pin
import utime

# Definice pinů přesně podle tvého funkčního formátu
pins_labels = ['D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12']

# Inicializace pinů (na začátku jako vstupy)
sensors = [Pin(p, Pin.IN) for p in pins_labels]

def read_line_sensors():
    # 1. NABÍJENÍ: Nastavit na výstup a poslat HIGH
    for s in sensors:
        s.init(mode=Pin.OUT)
        s.value(1)
    
    utime.sleep_us(10) # Čas na nabití kondenzátorů
    
    # 2. PŘEPNUTÍ: Nastavit zpět na vstup pro měření vybíjení
    for s in sensors:
        s.init(mode=Pin.IN)
        
    start_time = utime.ticks_us()
    times = [0] * 8
    done_count = 0
    max_wait = 3000 # Timeout v mikrosekundách (černá barva)
    
    # 3. MĚŘENÍ: Sledujeme, kdy piny spadnou na 0
    while done_count < 8:
        current_time = utime.ticks_us()
        elapsed = utime.ticks_diff(current_time, start_time)
        
        # Pokud čekáme moc dlouho, zbytek označíme za černou
        if elapsed >= max_wait:
            for i in range(8):
                if times[i] == 0: times[i] = max_wait
            break
            
        for i in range(8):
            if times[i] == 0: # Pokud senzor ještě neskončil
                if sensors[i].value() == 0:
                    times[i] = elapsed
                    done_count += 1
                    
    return times

# Hlavní smyčka
print("Startuju QTR-8RC test (Teensy 4.1)...")
while True:
    results = read_line_sensors()
    
    # Formátovaný výstup: Čím vyšší číslo, tím víc ČERNÁ barva
    # (Bílá bývá kolem 100-500, černá nad 1500-2000)
    print(" | ".join(["{:4d}".format(t) for t in results]))
    
    utime.sleep_ms(100)