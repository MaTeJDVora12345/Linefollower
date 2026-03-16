# Technická dokumentace: Linefollower 3.0 2026 

**Tým:** Jakub Lukšík & Matěj Dvořák  
**Škola:** Střední škola informatiky a finančních služeb (INFIS)  
**Soutěž:** ROBO2026  
**Verze:** 3.0

---

## 1. Úvod a cíle projektu
Projekt "Linefollower 3.0 2026" byl vyvinut jako soutěžní robot pro autonomní sledování černé čáry na světlém podkladu v rámci soutěže ROBO2026. Hlavním cílem byla konstrukce robota s vysokou dynamikou a precizním řízením, čehož bylo dosaženo kombinací výkonného mikrokontroléru Teensy 4.1 a lehkého 3D tištěného šasi.

## 2. Mechanická konstrukce
Konstrukce robota se zaměřuje na nízké těžiště a tuhost, což je klíčové pro stabilitu v zatáčkách při vysokých rychlostech.
* **Návrh:** Šasi bylo kompletně navrženo v CAD prostředí **Autodesk Fusion 360**.
* **Výroba:** Hlavní díly jsou vyrobeny 3D tiskem z materiálu PLA.
* **Povrchová úprava:** Pro dosažení vysokého estetického standardu byl povrch ošetřen metalickým sprejem Primalex, což robotovi dodává profesionální vzhled a odlišuje jej od běžných prototypů.
* **Pohon:** Robot využívá dva převodové motory řady Pololu 25D s integrovanými magnetickými enkodéry pro získání aktuální pozice vozidla na dráze.

## 3. Hardware a elektronika
Elektronický systém je postaven na manuálně vyrobeném PCB navrženém v programu KiCad, s důrazem na čistotu signálů a efektivní napájení.

### Klíčové komponenty:
* **Řídicí jednotka:** Teensy 4.1 (ARM Cortex-M7, 600 MHz). Zvolena pro nadstandardní výpočetní výkon umožňující vysokou vzorkovací frekvenci PID smyčky.
* **Motorové budiče:** 2× breakout board s čipy DRV8871. Tyto budiče disponují integrovanou proudovou ochranou a jsou řízeny pomocí PWM.
* **Senzorové pole:** 8 infračervených senzorů QTR-8RC, které jsou optimalizovány pro rychlou odezvu na změnu kontrastu podkladu.
* **Napájení:** 3S LiPo akumulátor (11.1V). Připojení je realizováno přes robustní konektor XT60, který minimalizuje přechodový odpor.
* **Stabilizace napětí:** Spínaný regulátor TSR 1-2450 zajišťující stabilních 5V pro logické obvody s účinností až 94 %.

### Zapojení pinů (Teensy 4.1):
| Funkce | Pin | Popis |
| :--- | :--- | :--- |
| **Motor L - PWM** | 2 | Rychlost levého motoru |
| **Motor L - DIR** | 3 | Směr levého motoru |
| **Motor R - PWM** | 5 | Rychlost pravého motoru |
| **Motor R - DIR** | 6 | Směr pravého motoru |
| **Senzory čáry** | 14 – 21 | Vstupy z pole QTR-8RC |

## 4. Algoritmus řízení
Software implementuje digitální **PID regulátor**, který vypočítává korekci směru na základě váženého průměru hodnot ze senzorového pole.

### Konfigurované parametry regulace:
* **P (Proporcionální složka):** $K_p = 0.5$ – určuje okamžitou reakci na aktuální odchylku od středu.
* **I (Integrální složka):** $K_i = 0.001$ – koriguje drobnou systematickou chybu v delších úsecích.
* **D (Derivační složka):** $K_d = 0.1$ – predikuje budoucí chybu a tlumí překmity při rychlých změnách směru.

Robot pracuje s normalizovanou pozicí čáry v rozsahu 0 až 7000. Základní rychlost pohybu (BASE_SPEED) je nastavena na hodnotu 150 pro dosažení optimálního poměru mezi stabilitou a časem průjezdu.

## 5. Bezpečnost a údržba
Vzhledem k použití LiPo akumulátorů jsou dodržovány tyto bezpečnostní zásady:
* Nabíjení probíhá výhradně v protipožárním vaku (LiPo Safe Bag).
* Napětí akumulátoru je monitorováno, aby nedošlo k podvybití článků pod kritickou mez.
* Mechanické spoje a stav kabeláže jsou kontrolovány před každou jízdou.

## 6. Seznam součástek (BOM)
| Označení | Komponenta | Množství | Poznámka |
| :--- | :--- | :--- | :--- |
| **U1** | Teensy 4.1 | 1 ks | Řídicí mikrokontrolér |
| **U2, U4** | DRV8871 Breakout | 2 ks | H-Můstek pro motory |
| **U3** | TSR 1-2450 | 1 ks | DC/DC měnič (5V) |
| **J1** | XT60-M | 1 ks | Napájecí konektor |
| **J4** | IDC-Header 2x12 | 1 ks | Konektor pro senzory |
| **C1, C2** | 100µF / 25V | 2 ks | Filtrační kondenzátory |
| **R1-R3** | 100 Ohm | 3 ks | Předřadné rezistory LED |
| **Q1** | IRLZ44N | 1 ks | Spínací Power MOSFET |

---

## 7. Přílohy
* **Příloha A:** Technický výkres šasi (export z Fusion 360)
* **Příloha B:** Schéma zapojení (export z KiCad)
* **Příloha C:** Kompletní zdrojový kód (soubor `main.py`)
* **Příloha D:** Seznam součástek (BOM)