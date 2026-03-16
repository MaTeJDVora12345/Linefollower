# Technická dokumentace: Linefollower 2026 (Lite Version)

**Tým:** [Doplňte jména členů týmu]  
[cite_start]**Škola:** Střední škola informatiky a finančních služeb (INFIS) [cite: 1]  
**Soutěž:** ROBO2026  
[cite_start]**Verze:** 3.0 (Lite) [cite: 1]

---

## 1. Úvod a cíle projektu
Projekt "Linefollower 2026 lite version" byl vyvinut jako soutěžní robot pro autonomní sledování černé čáry na světlém podkladu. Hlavním cílem byla konstrukce robota s vysokou dynamikou, čehož bylo dosaženo použitím výkonného mikrokontroléru Teensy 4.1 a lehkého 3D tištěného šasi.

## 2. Mechanická konstrukce
Konstrukce robota se zaměřuje na nízké těžiště a tuhost, což je klíčové pro stabilitu v zatáčkách při vysokých rychlostech.
* **Návrh:** Šasi bylo kompletně navrženo v CAD prostředí **Autodesk Fusion 360**.
* **Výroba:** Hlavní díly jsou vyrobeny 3D tiskem z materiálu PLA.
* **Povrchová úprava:** Pro dosažení estetického standardu požadovaného porotou byl povrch ošetřen metalickým sprejem Primalex, což robotovi dodává profesionální vzhled.
* [cite_start]**Pohon:** Robot využívá dva převodové motory řady Pololu 25D s integrovanými magnetickými enkodéry pro zpětnou vazbu o rychlosti a poloze[cite: 19, 57].

## 3. Hardware a elektronika
Elektronický systém je navržen s důrazem na modularitu a spolehlivost. [cite_start]Základem je vlastní PCB navržené v programu KiCad[cite: 1].

### Klíčové komponenty:
* [cite_start]**Řídicí jednotka:** Teensy 4.1 (ARM Cortex-M7, 600 MHz), která poskytuje dostatečný výkon pro výpočty PID regulace v reálném čase[cite: 27, 35, 54].
* [cite_start]**Motorové budiče:** 2× breakout board s čipy DRV8871, které disponují proudovou ochranou a umožňují plynulé PWM řízení[cite: 8, 49, 51].
* [cite_start]**Senzorové pole:** 8 infračervených senzorů QTR-8RC připojených přes IDC konektor[cite: 3, 64].
* [cite_start]**Napájení:** 3S LiPo akumulátor (11.1V) s připojením přes robustní konektor XT60[cite: 60].
* [cite_start]**Stabilizace napětí:** Spínaný regulátor TSR 1-2450 zajišťující stabilních 5V pro logické obvody bez nadbytečného zahřívání[cite: 22, 62].

### Zapojení pinů (Teensy 4.1):
| Funkce | Pin | Popis |
| :--- | :--- | :--- |
| **Motor L - PWM** | 2 | Rychlost levého motoru |
| **Motor L - DIR** | 3 | Směr levého motoru |
| **Motor R - PWM** | 5 | Rychlost pravého motoru |
| **Motor R - DIR** | 6 | Směr pravého motoru |
| **Senzory čáry** | 14 – 21 | Vstupy z pole QTR-8RC |

## 4. Algoritmus řízení
Software implementuje digitální **PID regulátor**, který vypočítává korekci směru na základě odchylky od středu čáry.

### Konfigurované parametry regulace:
* **P (Proporcionální složka):** $K_p = 0.5$ – určuje sílu reakce na aktuální chybu.
* **I (Integrální složka):** $K_i = 0.001$ – koriguje kumulativní chybu v čase.
* **D (Derivační složka):** $K_d = 0.1$ – tlumí kmitání tím, že reaguje na rychlost změny chyby.

Robot pracuje s normalizovanou pozicí čáry v rozsahu 0 (čára zcela vlevo) až 7000 (čára zcela vpravo). Základní rychlost pohybu je nastavena na hodnotu 150 (PWM duty cycle).

## 5. Bezpečnost a údržba
Vzhledem k použití LiPo akumulátorů jsou dodržovány následující bezpečnostní protokoly:
* Nabíjení probíhá výhradně v protipožárním vaku pod neustálým dohledem.
* Napětí akumulátoru je sledováno, aby nedošlo k podvybití pod 3.3V na článek.
* [cite_start]PCB obsahuje MOSFET IRLZ44N jako ochranný nebo spínací prvek v napájecí větvi[cite: 24, 57].

## 6. Seznam součástek (BOM)
| Označení | Komponenta | Množství | Poznámka |
| :--- | :--- | :--- | :--- |
| **U1** | Teensy 4.1 | 1 ks | [cite_start]Hlavní MCU [cite: 27] |
| **U2, U4** | DRV8871 Breakout | 2 ks | [cite_start]Motor driver [cite: 8, 51] |
| **U3** | TSR 1-2450 | 1 ks | [cite_start]5V DC/DC měnič [cite: 22] |
| **J1** | XT60-M | 1 ks | [cite_start]Konektor baterie [cite: 60] |
| **J4** | IDC-Header 2x12 | 1 ks | [cite_start]Připojení QTR-8RC [cite: 64] |
| **C1, C2** | 100µF / 25V | 2 ks | [cite_start]Filtrační elyt [cite: 52, 62] |
| **R1-R3** | 100 Ohm | 3 ks | [cite_start]Rezistory pro LED [cite: 52, 53, 56] |
| **D2** | LED_RKGB | 1 ks | [cite_start]Indikační RGB LED [cite: 60] |

---

## 7. Přílohy
* **Příloha A:** Technický výkres šasi (export z Fusion 360)
* **Příloha B:** Schéma zapojení (export z KiCad)
* **Příloha C:** Kompletní zdrojový kód (`main.py`)