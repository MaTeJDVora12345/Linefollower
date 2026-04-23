# Technical Documentation: Linefollower 3.0 2026

**Team:** Jakub Lukšík & Matěj Dvořák  
**School:** Secondary School of Informatics and Financial Services (INFIS)  
**Competition:** ROBO2026  
**Version:** 3.0  
**Date:** March 16, 2026

---

## 1. Introduction and Project Objectives
The "Linefollower 3.0 2026" project was developed as a competitive robot for autonomous black line following on a light background for the ROBO2026 competition. The primary objective was to construct a robot with high dynamics and precise control, achieved by combining a powerful Teensy 4.1 microcontroller with a lightweight 3D-printed chassis.

## 2. Mechanical Construction
The robot's design focuses on a low center of gravity and rigidity, which are crucial for stability during high-speed cornering.
* **Design:** The chassis was completely designed in the **Autodesk Fusion 360** CAD environment.
* **Manufacturing:** Main parts are 3D printed from PLA for easy and low-cost production. PETG supports were used during printing for easy removal.
* **Surface Finish:** To achieve a high aesthetic standard, the surface was treated with metallic spray paint, giving the robot a professional appearance and distinguishing it from common prototypes.
* **Drive:** The robot utilizes two Pololu 25D series gearmotors with integrated magnetic encoders for distance estimation and sector-based drive control.

* **Total Weight:** 600 g
* **Wheelbase:** _______
* **Wheel Diameter:** _______

[//]: # (* TODO: Fill in wheelbase and wheel diameter values)

## 3. Hardware and Electronics
The electronic system is built on a custom-designed and assembled PCB created in KiCad, emphasizing signal integrity and efficient power management.

### Key Components:
* **Control Unit:** Teensy 4.1 (ARM Cortex-M7, 600 MHz). Selected for its superior processing power, allowing for a high sampling frequency of the PID loop.
* **Motor Drivers:** 2× breakout boards with DRV8871 chips (U2, U4). These feature integrated overcurrent protection and are controlled by a 1 kHz PWM signal. The input power rail of each driver is decoupled by electrolytic capacitors C1 and C2 (100 µF / 25 V) to suppress voltage spikes from motor commutation.
* **Sensor Array:** 8 infrared QTR-8RC sensors, optimized for fast response to contrast changes. The sensor bar is connected via an IDC cable to connector J4.
* **Status RGB LED:** Component D2 (LED_RKGB, 5 mm, 4 pins) visually indicates the robot's status. Each of the three color channels is protected by series resistors R1, R2, and R3 (100 Ω), limiting the current to approximately 30 mA at 5 V.
* **Power Supply:** 3S LiPo battery (11.1 V nominal, 12.6 V fully charged, critical threshold 9.9 V = 3.3 V/cell). Connected via an XT60 connector (J1). The entire power supply is switched by a high-power N-channel MOSFET IRLZ44N (Q1, 47 A / 55 V), with its gate controlled via a protective resistor R5 (1 kΩ) from the main switch. This solution allows for safe disconnection of the entire power circuit without mechanical cable interruption.
* **Voltage Stabilization:** A TSR 1-2450 switching regulator (U3) provides a stable 5 V for logic circuits with up to 94% efficiency. Ceramic decoupling capacitors C3 and C4 (100 nF) are placed on its output rail to suppress high-frequency noise.

### Pinout (Teensy 4.1):
| Function | Pin | Direction | Description |
| :--- | :--- | :--- | :--- |
| **Encoder** | D1 | IN | Magnetic encoder input (IRQ_RISING interrupt) |
| **Motor L - PWM** | D3 | OUT | Left motor speed (PWM, 1 kHz, 16-bit) |
| **Motor L - DIR** | D4 | OUT | Left motor direction |
| **Line Sensor 1** | D5 | IN/OUT | QTR-8RC - far left sensor |
| **Line Sensor 2** | D6 | IN/OUT | QTR-8RC |
| **Line Sensor 3** | D7 | IN/OUT | QTR-8RC |
| **Line Sensor 4** | D8 | IN/OUT | QTR-8RC |
| **Line Sensor 5** | D9 | IN/OUT | QTR-8RC |
| **Line Sensor 6** | D10 | IN/OUT | QTR-8RC |
| **Line Sensor 7** | D11 | IN/OUT | QTR-8RC |
| **Line Sensor 8** | D12 | IN/OUT | QTR-8RC - far right sensor |
| **LED RGB - B** | D13 | OUT | Status LED (Blue) |
| **LED RGB - R** | D14 | OUT | Status LED (Red) |
| **LED RGB - G** | D15 | OUT | Status LED (Green) |
| **Motor R - PWM** | D28 | OUT | Right motor speed (PWM, 1 kHz, 16-bit) |
| **Motor R - DIR** | D29 | OUT | Right motor direction |

## 4. Control Algorithm
The software implements a digital **PID controller**, which calculates steering corrections based on a weighted average of values from the sensor array.

### Configured Control Parameters:
* **P (Proportional):** $K_p = ___________$ – determines immediate reaction to current deviation from the center.
* **I (Integral):** $K_i = ____________$ – corrects small systematic errors over longer sections.
* **D (Derivative):** $K_d = ____________$ – predicts future error and dampens overshooting during rapid direction changes.

The robot operates with a normalized line position ranging from 0 to 3000. The base speed (`BASE_SPEED`) is set to 30,000 to achieve an optimal balance between stability and lap time.
To optimize driving smoothness, the track is divided into imaginary sectors. The robot tracks its location via encoder counts and uses optimized speed and sensitivity settings specifically for each sector.

## 5. Safety and Maintenance
Due to the use of LiPo batteries, the following safety guidelines are followed:
* Charging takes place exclusively in a fireproof bag (LiPo Safe Bag).
* Battery voltage is monitored via a voltage divider on the Teensy 4.1 analog input. The critical lower limit is **9.9 V** (3.3 V/cell) – falling below this value risks irreversible cell damage. A fully charged battery reaches 12.6 V.
* Mechanical connections and cable conditions are inspected before every run.

## 6. Bill of Materials (BOM)
| Reference | Component | Quantity | Note |
| :--- | :--- | :--- | :--- |
| **U1** | Teensy 4.1 | 1 pc | Main microcontroller |
| **U2, U4** | DRV8871 Breakout | 2 pcs | H-Bridge for motors |
| **U3** | TSR 1-2450 | 1 pc | DC/DC converter (5 V) |
| **J1** | XT60-M | 1 pc | Power connector |
| **J4** | IDC-Header 2x12 | 1 pc | QTR-8RC sensor bar connector |
| **D2** | LED_RKGB (5 mm) | 1 pc | Status RGB LED |
| **C1, C2** | 100 µF / 25 V | 2 pcs | Electrolytic supply filters for motor drivers |
| **C3, C4** | 100 nF | 2 pcs | Ceramic decoupling capacitors for TSR regulator |
| **R1-R3** | 100 Ω | 3 pcs | RGB LED series resistors (D2) |
| **R5** | 1 kΩ | 1 pc | MOSFET Q1 gate protection resistor |
| **Q1** | IRLZ44N | 1 pc | N-MOSFET, main power switch (47 A / 55 V) |

---

## 7. Appendices
* **Appendix A:** Technical drawing of the chassis
* **Appendix B:** Circuit diagram (Schematic)
* **Appendix C:** Complete source code