# pH/ORP Monitor — Specifikácia dosky v1.0

## Popis projektu

Experimentálna riadiaca a meraciu doska pre pH/ORP monitoring s ESP32.
Určené do IP64/IP65 hliníkového boxu (vonkajšie použitie).
Všetko vrátane čerpadla bude v jednom boxe — von trčia len konce hadičiek, BNC konektory a napájací kábel 230V.

---

## Bloková schéma

```
230VAC → Poistka → HLK-30M12 → 12V
                        │
          ┌─────────────┼──────────────┬─────────────────┐
          │             │              │                  │
     LM2596→5V     LM7805→5V(AN)  4×MOSFET(12V)    Relé(12V)→230V
          │             │
     AMS1117→3.3V  TPS60400→-5V(AN)
          │             │
        ESP32       CA3140×2 + TL071×2
          │             │
          └──ADS1115←───┘ (I2C)
          │
          ├── SPI → Display konektor (14-pin)
          ├── 4×GPIO → MOSFETy
          ├── 1×GPIO → Relé (cez PC817 optočlen)
          ├── 1×GPIO → 1-Wire (4×JST-XH konektor)
          ├── BNC×2 → pH + ORP sondy
          └── Ext. pin header (voľné GPIO pre budúce rozšírenia)
```

---

## Napájanie

### Vstup: 230VAC

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| J1 | Šróbovacia svorkovnica 3-pin | L, N, PE | 5mm pitch, 250V rated | 230V vstup |
| F1 | Poistka pomalá (T) | 2A / 250V | 5×20mm + PCB holder | Na PCB |
| U1 | HLK-30M12 | 230VAC → 12V / 2.5A (30W) | PCB modul ~50×36mm | Izolovaný SMPS, CE/UL |
| C1 | Keramický kondenzátor | 100nF | 0805 | Bypass na 12V výstupe U1 |
| R1 | Rezistor | 1kΩ | 0805 | Predradný pre LED D1 |
| D1 | LED modrá | — | 0805 | Indikátor napájania 12V |

### 12V → 5V (digitálna vetva)

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| U2 | LM2596S-5.0 | 12V → 5V / 3A | TO-263-5 | Spínaný buck, pre ESP32/display/logiku |
| L1 | Tlmivka | 33µH / 3A | — | Výkonová tlmivka pre U2 |
| D2 | SS34 | 40V / 3A Schottky | SMA (DO-214AC) | Dióda pre buck U2 |
| C2 | Elektrolytický kondenzátor | 680µF / 25V | Radiálny | Vstupný kondenzátor U2 |
| C3 | Elektrolytický kondenzátor | 220µF / 10V | Radiálny | Výstupný kondenzátor U2 |

### 5V → 3.3V (ESP32)

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| U3 | AMS1117-3.3 | 5V → 3.3V / 1A | SOT-223 | LDO pre ESP32-WROOM |
| C4 | Keramický kondenzátor | 10µF | 0805 | Vstupný bypass U3 |
| C5 | Keramický kondenzátor | 22µF | 1206 | Výstupný bypass U3 |

### 12V → +5V (analógová vetva — ČISTÁ)

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| U4 | LM7805 | 12V → 5V | TO-220 | Lineárny regulátor — žiadny spínací šum |
| C6 | Keramický kondenzátor | 100nF | 0805 | Vstupný filter U4 |
| C7 | Elektrolytický kondenzátor | 10µF / 25V | Radiálny | Vstupný filter U4 |
| C8 | Keramický kondenzátor | 100nF | 0805 | Výstupný filter U4 |
| C9 | Elektrolytický kondenzátor | 10µF / 16V | Radiálny | Výstupný filter U4 |
| FB1 | Feritová perla | 600Ω@100MHz | 0805 | Filter na +5V_AN výstupe |
| L2 | Tlmivka | 10µH | 0805 | LC filter +5V_AN |
| C10 | Elektrolytický kondenzátor | 47µF / 16V | Radiálny | LC filter +5V_AN |

### +5V → -5V (analógová vetva — ČISTÁ)

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| U5 | TPS60400DBVR | 5V → -5V / 60mA | SOT-23-5 | Charge pump |
| C11 | Keramický kondenzátor | 1µF | 0805 | "Flying" kondenzátor (C+ → C-) |
| C12 | Keramický kondenzátor | 10µF | 0805 | Výstupný filter U5 |
| FB2 | Feritová perla | 600Ω@100MHz | 0805 | Filter na -5V_AN výstupe |

---

## pH senzor — analógový front-end

Pôvodná schéma: DFRobot SEN0161 pH Meter V1.0

### Vstupný buffer

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| P1 | BNC konektor | — | Panel mount | pH sonda |
| U6 | CA3140EZ | CMOS op-amp | DIP-8 | Zin >1TΩ, kritický pre pH sondu |
| R2 | Rezistor | 4.7MΩ | 0805 | Vstupný bias |
| C13 | Keramický kondenzátor | 2.2nF | 0805 | VF filter na vstupe |
| C14 | Keramický kondenzátor | 1µF | 0805 | Frekvenčná kompenzácia |
| R3 | Rezistor | 2.2kΩ | 0805 | Feedback |
| R4 | Trimer | 5kΩ | Multi-turn | Kalibrácia pH (offset/gain) |
| R5 | Rezistor | 1kΩ | 0805 | Bias |
| C15 | Keramický kondenzátor | 100nF | 0805 | Bypass +5V_AN na U6 pin 7 |
| C16 | Keramický kondenzátor | 100nF | 0805 | Bypass -5V_AN na U6 pin 4 |

### Výstupný stupeň

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| U7 | TL081CDT | JFET op-amp | SOIC-8 | Invertujúci zosilňovač, gain=-1 |
| R6 | Rezistor | 30kΩ | 0805 | Feedback (U7 pin 6 → pin 2) |
| R7 | Rezistor | 30kΩ | 0805 | Vstupný rezistor (U6 out → U7 pin 2) |
| R8 | Rezistor | 75kΩ | 0805 | Offset kompenzácia (U7 pin 3) |
| C17 | Keramický kondenzátor | 100nF | 0805 | Bypass +5V_AN na U7 pin 7 |
| C18 | Keramický kondenzátor | 100nF | 0805 | Bypass -5V_AN na U7 pin 4 |

**Výstupný net:** pH_OUT → ADS1115 AIN0

---

## ORP senzor — analógový front-end

Rovnaká topológia ako pH senzor.

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| P2 | BNC konektor | — | Panel mount | ORP sonda |
| U8 | CA3140EZ | CMOS op-amp | DIP-8 | Vstupný buffer ORP |
| R9 | Rezistor | 4.7MΩ | 0805 | Vstupný bias |
| C19 | Keramický kondenzátor | 2.2nF | 0805 | VF filter |
| C20 | Keramický kondenzátor | 1µF | 0805 | Frekvenčná kompenzácia |
| R10 | Rezistor | 2.2kΩ | 0805 | Feedback |
| R11 | Trimer | 5kΩ | Multi-turn | Kalibrácia ORP |
| R12 | Rezistor | 1kΩ | 0805 | Bias |
| C21 | Keramický kondenzátor | 100nF | 0805 | Bypass +5V_AN na U8 pin 7 |
| C22 | Keramický kondenzátor | 100nF | 0805 | Bypass -5V_AN na U8 pin 4 |
| U9 | TL081CDT | JFET op-amp | SOIC-8 | Invertujúci zosilňovač ORP |
| R13 | Rezistor | 30kΩ | 0805 | Feedback |
| R14 | Rezistor | 30kΩ | 0805 | Vstupný rezistor |
| R15 | Rezistor | 75kΩ | 0805 | Offset kompenzácia |
| C23 | Keramický kondenzátor | 100nF | 0805 | Bypass +5V_AN na U9 pin 7 |
| C24 | Keramický kondenzátor | 100nF | 0805 | Bypass -5V_AN na U9 pin 4 |

**Výstupný net:** ORP_OUT → ADS1115 AIN1

---

## ADC — ADS1115

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| U10 | ADS1115IDGSR | 16-bit ADC, I2C, 4ch | MSOP-10 | PGA, napájanie 3.3V |
| C25 | Keramický kondenzátor | 100nF | 0805 | Bypass na VDD |
| R16 | Rezistor | 4.7kΩ | 0805 | I2C pull-up SDA → +3V3 |
| R17 | Rezistor | 4.7kΩ | 0805 | I2C pull-up SCL → +3V3 |

### Mapovanie kanálov ADS1115

| Kanál | Signál | Zdroj |
|-------|--------|-------|
| AIN0 | pH_OUT | U7 pin 6 |
| AIN1 | ORP_OUT | U9 pin 6 |
| AIN2 | voľný | vyvedený na pad |
| AIN3 | voľný | vyvedený na pad |

ADDR pin → GND = I2C adresa **0x48**

---

## ESP32

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| U11 | ESP32-WROOM-32E-N4 | MCU modul | Modul 38-pin | 4MB flash, WiFi + BT |
| C26 | Keramický kondenzátor | 100nF | 0805 | Bypass na 3V3 |
| C27 | Keramický kondenzátor | 10µF | 0805 | Bypass na 3V3 |
| R18 | Rezistor | 10kΩ | 0805 | Pull-up na EN pin |
| C28 | Keramický kondenzátor | 100nF | 0805 | RC filter na EN |
| R19 | Rezistor | 10kΩ | 0805 | Pull-up na GPIO0 (boot) |

### GPIO alokácia

| GPIO | Funkcia | Smer | Ref cieľa | Poznámka |
|------|---------|------|-----------|----------|
| 18 | SPI SCK | OUT | J2 pin 7 | Display + Touch (zdieľané) |
| 23 | SPI MOSI | OUT | J2 pin 6 | Display + Touch (zdieľané) |
| 19 | SPI MISO | IN | J2 pin 9 | Display + Touch (zdieľané) |
| 15 | Display CS | OUT | J2 pin 3 | ILI9488 chip select |
| 2 | Display DC | OUT | J2 pin 5 | Data/Command |
| 4 | Display RST | OUT | J2 pin 4 | Reset |
| 32 | Display BL | OUT | J2 pin 8 | Backlight (PWM capable) |
| 21 | Touch CS | OUT | J2 pin 11 | XPT2046 chip select |
| 39 | Touch IRQ | IN | J2 pin 14 | Input only, interrupt |
| 26 | I2C SDA | I/O | U10 pin SDA | ADS1115 |
| 27 | I2C SCL | OUT | U10 pin SCL | ADS1115 |
| 33 | MOSFET 1 | OUT | Q1 gate | Čerpadlo |
| 25 | MOSFET 2 | OUT | U12 pin 1 | Relé (cez PC817) |
| 13 | MOSFET 3 | OUT | Q3 gate | Voľný výstup |
| 14 | MOSFET 4 | OUT | Q4 gate | Voľný výstup |
| 5 | 1-Wire | I/O | J3-J6 pin 2 | DS18B20 senzory |
| 1 | UART TX | OUT | J8 pin 2 | Debug |
| 3 | UART RX | IN | J8 pin 3 | Debug |

### Voľné GPIO vyvedené na pin header (J7)

| GPIO | Typ | Pin na J7 | Poznámka |
|------|-----|-----------|----------|
| 12 | I/O | 1 | Boot strapping pin (musí byť LOW pri boote) |
| 16 | I/O | 2 | Voľný |
| 17 | I/O | 3 | Voľný |
| 22 | I/O | 4 | Voľný |
| 34 | Input only | 5 | ADC1_CH6 |
| 35 | Input only | 6 | ADC1_CH7 |
| 36 (SVP) | Input only | 7 | ADC1_CH0 |
| +3V3 | Power | 8-10 | Napájanie |
| +5V | Power | 11-13 | Napájanie |
| GND | Power | 14-20 | Zem (pod každým signálom) |

Pin header J7: **2×10 kolíkov 2.54mm**

---

## Display konektor

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| J2 | Pin header | 1×14 | 2.54mm | Pre ILI9488 + XPT2046 modul |

### Pinout J2

| Pin | Signál | GPIO |
|-----|--------|------|
| 1 | VCC (3.3V) | — |
| 2 | GND | — |
| 3 | CS | GPIO15 |
| 4 | RESET | GPIO4 |
| 5 | DC | GPIO2 |
| 6 | MOSI | GPIO23 |
| 7 | SCK | GPIO18 |
| 8 | LED (BL) | GPIO32 |
| 9 | MISO | GPIO19 |
| 10 | T_CLK | GPIO18 (zdieľaný) |
| 11 | T_CS | GPIO21 |
| 12 | T_DIN | GPIO23 (zdieľaný) |
| 13 | T_DO | GPIO19 (zdieľaný) |
| 14 | T_IRQ | GPIO39 |

---

## MOSFET výstupy (4×)

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| Q1 | IRLZ44NPBF | N-ch MOSFET 55V/47A | TO-220 | Čerpadlo NKP-DCL-B10D |
| Q2 | IRLZ44NPBF | N-ch MOSFET 55V/47A | TO-220 | Relé cievka (cez PC817) |
| Q3 | IRLZ44NPBF | N-ch MOSFET 55V/47A | TO-220 | Voľný výstup |
| Q4 | IRLZ44NPBF | N-ch MOSFET 55V/47A | TO-220 | Voľný výstup |
| R20 | Rezistor | 100Ω | 0805 | Gate rezistor Q1 |
| R21 | Rezistor | 100Ω | 0805 | Gate rezistor Q2 |
| R22 | Rezistor | 100Ω | 0805 | Gate rezistor Q3 |
| R23 | Rezistor | 100Ω | 0805 | Gate rezistor Q4 |
| R24 | Rezistor | 10kΩ | 0805 | Pull-down Q1 gate → GND |
| R25 | Rezistor | 10kΩ | 0805 | Pull-down Q2 gate → GND |
| R26 | Rezistor | 10kΩ | 0805 | Pull-down Q3 gate → GND |
| R27 | Rezistor | 10kΩ | 0805 | Pull-down Q4 gate → GND |
| D3 | SS14 | 40V/1A Schottky | SOD-123 | Flyback dióda Q1 (čerpadlo) |
| D4 | SS14 | 40V/1A Schottky | SOD-123 | Flyback dióda Q2 (relé cievka) |
| D5 | SS14 | 40V/1A Schottky | SOD-123 | Flyback dióda Q3 |
| D6 | SS14 | 40V/1A Schottky | SOD-123 | Flyback dióda Q4 |

### Konektory MOSFET výstupov

| Ref | Záťaž | Typ konektora |
|-----|-------|---------------|
| — | Q1: Čerpadlo NKP-DCL-B10D (12V/5W) | Interný vodič (v boxe) |
| — | Q2: Relé cievka | Interný vodič |
| J9 | Q3: Voľný výstup | Šróbovacia svorkovnica 2-pin (+12V + drain) |
| J10 | Q4: Voľný výstup | Šróbovacia svorkovnica 2-pin (+12V + drain) |

---

## Relé — 230V/16A výstup

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| U12 | PC817 | Optočlen | DIP-4 | Galvanická izolácia ESP32 od relé |
| R28 | Rezistor | 330Ω | 0805 | LED strana U12 (3.3V → ~10mA) |
| R29 | Rezistor | 1kΩ | 0805 | Kolektorová strana U12 → gate Q2 |
| RLY1 | Finder 40.52.9.012.0000 | 12V cievka, 16A/250VAC | PCB relay | 2×prepínací kontakt |
| D7 | 1N4007 | 1000V/1A | DO-41 | Flyback dióda na cievke RLY1 |
| R30 | Rezistor | 100Ω | 0805 alebo THT | RC snubber na kontaktoch RLY1 |
| C29 | Kondenzátor X2 | 100nF / 275VAC | X2 safety | RC snubber na kontaktoch RLY1 |
| MOV1 | Varistor | 275V | Disc | Ochrana na kontaktoch RLY1 |

### 230V konektory

| Ref | Komponent | Poznámka |
|-----|-----------|----------|
| J1 | (zdieľaný) | 230V vstup — L, N, PE |
| J11 | Šróbovacia svorkovnica 3-pin, 250V rated | 230V výstup — L_out (cez RLY1 NO), N_out, PE |

**Bezpečnostné vzdialenosti: min 6mm creepage** medzi 230V a LV sekciou (IPC-2221).

---

## 1-Wire senzory (DS18B20)

| Ref | Komponent | Hodnota | Puzdro | Poznámka |
|-----|-----------|---------|--------|----------|
| J3 | JST-XH 3-pin | VCC/DATA/GND | 2.54mm | 1-Wire slot 1 |
| J4 | JST-XH 3-pin | VCC/DATA/GND | 2.54mm | 1-Wire slot 2 |
| J5 | JST-XH 3-pin | VCC/DATA/GND | 2.54mm | 1-Wire slot 3 |
| J6 | JST-XH 3-pin | VCC/DATA/GND | 2.54mm | 1-Wire slot 4 |
| R31 | Rezistor | 4.7kΩ | 0805 | Pull-up DATA → +3V3 |

Všetky J3-J6 paralelne: VCC=+3V3, DATA=GPIO5, GND=GND

---

## Voľný GPIO header + Debug

| Ref | Komponent | Puzdro | Poznámka |
|-----|-----------|--------|----------|
| J7 | Pin header 2×10 | 2.54mm | Voľné GPIO + napájanie |
| J8 | Pin header 1×4 | 2.54mm | Debug UART (3V3, TX, RX, GND) |

---

## Ochrana proti EMI / šumu

### Analógová sekcia

- Samostatný lineárny regulátor U4 (LM7805) pre +5V_AN
- U5 (TPS60400) pre -5V_AN
- FB1, FB2: Feritové perly na ±5V_AN pred op-ampami
- L2 + C10: LC filter na +5V_AN (10µH + 47µF, cutoff ~7kHz)
- AGND oddelené od DGND, spojené v jedinom star-point
- Guard ring okolo vysokoimpedančných vstupov U6, U8 (CA3140)

### Čerpadlo (DC motor)

- C_motor: 100nF keramický kondenzátor priamo na svorky motora (nie na PCB)
- FB_motor: Feritová perla na každom vodiči (nie na PCB)
- D3 (SS14): Flyback dióda na Q1

### Relé

- U12 (PC817) optočlen — galvanická izolácia
- R30 + C29: RC snubber na kontaktoch RLY1
- MOV1: Varistor na kontaktoch RLY1
- D7: Flyback dióda na cievke RLY1
- Fyzická separácia od analógovej sekcie na PCB

### PCB layout pravidlá

```
[230V + RLY1]  ←6mm→  [U1 + U2 + U11(ESP32)]  ←GND pour→  [U4 + U6-U9 (Analóg)]
  (roh 1)                    (stred)                          (roh 2, opačný)
```

---

## Tepelný manažment

| Ref | Zdroj | Pdiss |
|-----|-------|-------|
| U1 | HLK-30M12 | ~2.5W |
| U2 | LM2596 | ~1.2W |
| U3 | AMS1117 | ~0.85W |
| U4 | LM7805 | ~0.7W |
| RLY1 | Relé cievka | ~1W |
| — | Čerpadlo (motor) | ~2.5W |
| | **Celkom** | **~8.7W** |

**Riešenie:** Hliníkový IP65 box (napr. Hammond 1554 séria, ~150×100×80mm).
Teplé komponenty (U1, U2, U4) priložené termálnou podložkou k stene boxu.

---

## Kompletný BOM — nákupný zoznam

| # | Ref | Komponent | Hodnota / Typ | Ks | Poznámka |
|---|-----|-----------|--------------|-----|----------|
| 1 | U1 | HLK-30M12 | 230VAC→12V/2.5A | 1 | SMPS modul |
| 2 | U2 | LM2596S-5.0 | 12V→5V/3A | 1 | Buck konvertor, TO-263 |
| 3 | U3 | LD1117AS33TR | 5V→3.3V/1A | 1 | LDO, SOT-223 |
| 4 | U4 | L7805ABD2T-TR | 12V→5V (lineárny) | 1 | D2PAK, čistá analóg 5V |
| 5 | U5 | TPS60400DBVR | 5V→-5V/60mA | 1 | Charge pump, SOT-23-5 |
| 6 | U6, U8 | CA3140EZ | CMOS op-amp | 2 | DIP-8, pH+ORP buffer |
| 7 | U7, U9 | TL071IP | JFET op-amp | 2 | DIP-8, pH+ORP výstup |
| 8 | U10 | ADS1115IDGSR | 16-bit ADC, I2C | 1 | VSSOP-10 |
| 9 | U11 | ESP32-WROOM-32E-N4 | MCU modul | 1 | WiFi + BT, 4MB flash |
| 10 | U12 | LTV-356T | Optočlen | 1 | SOP-4, izolácia relé |
| 11 | Q1-Q4 | IRLR2905TRPBF | N-MOSFET 55V/30A | 4 | DPAK, logic-level |
| 12 | RLY1 | Finder 40.52.9.012 | Relé 12V, 16A/250VAC | 1 | 2×prepínací kontakt |
| 13 | D1 | LED modrá | — | 1 | 0805 |
| 14 | D2 | SS34 (ONSEMI) | 40V/3A Schottky | 1 | SMC (DO-214AB), buck dióda |
| 15 | D3-D6 | SS14 | 40V/1A Schottky | 4 | SMA, flyback MOSFET |
| 16 | D7 | M7 | 1000V/1A | 1 | SMA, flyback relé |
| 17 | R1 | Rezistor | 1kΩ | 1 | 0805, LED predradný |
| 18 | R2, R9 | Rezistor | 4.7MΩ | 2 | 0805, vstupný bias sonda |
| 19 | R3, R10 | Rezistor | 2.2kΩ | 2 | 0805, feedback |
| 20 | R4, R11 | Trimer | 5kΩ | 2 | Multi-turn, kalibrácia |
| 21 | R5, R12 | Rezistor | 1kΩ | 2 | 0805, bias |
| 22 | R6, R7, R13, R14 | Rezistor | 30kΩ | 4 | 0805, zosilňovač |
| 23 | R8, R15 | Rezistor | 75kΩ | 2 | 0805, offset |
| 24 | R16, R17 | Rezistor | 4.7kΩ | 2 | 0805, I2C pull-up |
| 25 | R18, R19 | Rezistor | 10kΩ | 2 | 0805, ESP32 EN+IO0 |
| 26 | R20-R23 | Rezistor | 100Ω | 4 | 0805, gate MOSFET |
| 27 | R24-R27 | Rezistor | 10kΩ | 4 | 0805, pull-down gate |
| 28 | R28 | Rezistor | 330Ω | 1 | 0805, optočlen LED |
| 29 | R29 | Rezistor | 1kΩ | 1 | 0805, optočlen kolektor |
| 30 | R30 | Rezistor | 100Ω | 1 | 0805/THT, RC snubber |
| 31 | R31 | Rezistor | 4.7kΩ | 1 | 0805, 1-Wire pull-up |
| 32 | C1 | Keramický | 100nF | 1 | 0805, bypass U1 |
| 33 | C2 | Elektrolytický | 680µF/25V | 1 | Radiálny, buck vstup |
| 34 | C3 | Elektrolytický | 220µF/10V | 1 | Radiálny, buck výstup |
| 35 | C4 | Keramický | 10µF | 1 | 0805, LDO vstup |
| 36 | C5 | Keramický | 22µF | 1 | 1206, LDO výstup |
| 37 | C6, C8 | Keramický | 100nF | 2 | 0805, LM7805 filter |
| 38 | C7, C9 | Elektrolytický | 10µF | 2 | Radiálny, LM7805 filter |
| 39 | C10 | Elektrolytický | 47µF/16V | 1 | Radiálny, LC filter |
| 40 | C11 | Keramický | 1µF | 1 | 0805, flying cap TPS60400 |
| 41 | C12 | Keramický | 10µF | 1 | 0805, TPS60400 výstup |
| 42 | C13, C19 | Keramický | 2.2nF | 2 | 0805, VF filter sonda |
| 43 | C14, C20 | Keramický | 1µF | 2 | 0805, freq. kompenzácia |
| 44 | C15-C18, C21-C24 | Keramický | 100nF | 8 | 0805, bypass op-amp |
| 45 | C25-C28 | Keramický | 100nF + 10µF | 4 | 0805, bypass ADC+ESP32 |
| 46 | C29 | Kondenzátor X2 | 100nF/275VAC | 1 | X2, RC snubber relé |
| 47 | L1 | Tlmivka | 33µH/3A | 1 | Výkonová, buck |
| 48 | L2 | Tlmivka | 10µH | 1 | 0805, LC filter analóg |
| 49 | FB1, FB2 | Feritová perla | 600Ω@100MHz | 2 | 0805, EMI filter analóg |
| 50 | MOV1 | Varistor | 275V | 1 | Disc, ochrana relé |
| 51 | F1 | Poistka + holder | 2A T, 5×20mm | 1 | Na PCB |
| 52 | P1, P2 | BNC konektor | Amphenol B6252HA-NPP3G-50 | 2 | 50Ω, right-angle PCB, [TME](https://www.tme.eu/sk/details/b6252ha-npp3g-50/konektory-bnc/amphenol-rf/) |
| 53 | J1 | Šróbovacia svorkovnica 3-pin | 250V rated | 1 | 230V vstup |
| 54 | J2 | Pin header 1×14 | 2.54mm | 1 | Display konektor |
| 55 | J3-J6 | JST-XH 3-pin | 2.54mm | 4 | 1-Wire senzory |
| 56 | J7 | Pin header 2×10 | 2.54mm | 1 | Voľné GPIO |
| 57 | J8 | Pin header 1×4 | 2.54mm | 1 | Debug UART |
| 58 | J9, J10 | Šróbovacia svorkovnica 2-pin | 5mm pitch | 2 | MOSFET výstupy Q3, Q4 |
| 59 | J11 | Šróbovacia svorkovnica 3-pin | 250V rated | 1 | 230V výstup cez relé |

---

## Celkový počet súčiastok

| Typ | Počet |
|-----|-------|
| IC / moduly (U1-U12) | 12 |
| MOSFETy (Q1-Q4) | 4 |
| Relé (RLY1) | 1 |
| Diódy (D1-D7) | 7 |
| Rezistory (R1-R31) | 31 |
| Kondenzátory (C1-C29) | 29 |
| Tlmivky (L1-L2) | 2 |
| Feritové perly (FB1-FB2) | 2 |
| Varistor (MOV1) | 1 |
| Poistka (F1) | 1 |
| Konektory (J1-J11, P1-P2) | 13 |
| **Celkom** | **~103 súčiastok** |

---

## Linky na TME.eu — objednávka IC a kľúčových komponentov

Všetky aktívne komponenty vybrané v **SMD** prevedení (okrem U1 modulu a RLY1 relé).

| # | Ref | Komponent | TME link | Puzdro | Poznámka |
|---|-----|-----------|----------|--------|----------|
| 1 | U1 | HLK-30M12 | ❌ Nie je na TME | Modul | AliExpress/eBay (Hi-Link originál) |
| 2 | U2 | LM2596S-5.0/NOPB | [TME](https://www.tme.eu/en/details/lm2596s-5.0_nopb/voltage-regulators-dc-dc-circuits/texas-instruments/) | TO-263-5 (SMD) | Texas Instruments |
| 3 | U3 | LD1117AS33TR | [TME SK](https://www.tme.eu/sk/details/ld1117as33tr/stabilizatory-napatia-neregulovane-ldo/stmicroelectronics/) | SOT-223 | STMicro, 3.3V/1A, náhrada AMS1117 |
| 3b | U3 alt. | LDL1117S33R | [TME](https://www.tme.eu/en/details/ldl1117s33r/ldo-fixed-voltage-regulators/stmicroelectronics/) | SOT-223 | STMicro, 3.3V/**1.2A**, novší, nižší dropout |
| 4 | U4 | L7805ABD2T-TR | [TME](https://www.tme.eu/en/details/l7805abd2t-tr/fixed-voltage-regulators/stmicroelectronics/) | **D2PAK** (SMD) | STMicro, 5V/1.5A, ±2%, ✅ na sklade |
| 5 | U5 | TPS60400DBVR | [TME](https://www.tme.eu/en/details/tps60400dbvr/voltage-regulators-dc-dc-circuits/texas-instruments/) | SOT-23-5 | TI, charge pump 5V→-5V |
| 6 | U6, U8 | CA3140EZ | [TME](https://www.tme.eu/en/details/ca3140ez/tht-operational-amplifiers/renesas-intersil/) | **DIP-8** | Renesas, MOSFET input, Zin>1TΩ, ✅ 542 ks na sklade |
| 7 | U7, U9 | TL071IP | [TME](https://www.tme.eu/en/details/tl071ip/tht-operational-amplifiers/texas-instruments/) | **DIP-8** | TI, JFET op-amp, nižší šum, ✅ 928 ks na sklade |
| 8 | U10 | ADS1115IDGSR | [TME](https://www.tme.eu/en/details/ads1115idgsr/a-d-converters-integrated-circuits/texas-instruments/) | VSSOP-10 | TI, 16-bit ADC |
| 9 | U11 | ESP32-WROOM-32E-N4 | [TME](https://www.tme.eu/en/details/esp32-wroom-32e/iot-wifi-bluetooth-modules/espressif/esp32-wroom-32e-n4/) | Modul SMD | Espressif, 4MB flash |
| 10 | U12 | LTV-356T | [TME](https://www.tme.eu/en/details/ltv-356t/optocouplers-analog-output/liteon/) | **SMD SOP-4** | Lite-On, náhrada PC817, 3.75kV izol. |
| 11 | Q1-Q4 | IRLR2905TRPBF | [TME](https://www.tme.eu/en/details/irlr2905trpbf/smd-n-channel-transistors/infineon-technologies/) | **DPAK** (SMD) | Infineon, 55V/30A, logic-level (Vgs_th 1-2V), Rds 27mΩ (over. dostupnosť!) |
| 12 | RLY1 | Finder 40.52.9.012.0000 | [TME](https://www.tme.eu/en/details/40.52.9.012.000/miniature-electromagnetic-relays/finder/40-52-9-012-0000/) | THT (relé) | DPDT, 12VDC, 15A |
| 13 | D2 | SS34 (ONSEMI) | [TME](https://www.tme.eu/en/details/ss34-ons/smd-schottky-diodes/onsemi/ss34/) | **SMC** (DO-214AB) | 40V/3A Schottky, buck, ✅ 1006 ks |
| 14 | D3-D6 | SS14 (Taiwan Semi) | [TME](https://www.tme.eu/en/details/ss14-tsc/smd-schottky-diodes/taiwan-semiconductor/ss14/) | **SMA** | 40V/1A Schottky, flyback (over. dostupnosť!) |
| 14b | D3-D6 alt. | SS14-E3/61T (Vishay) | [TME](https://www.tme.eu/en/details/ss14-e3_61t/smd-schottky-diodes/vishay/) | **SMA** | 40V/1A, Vishay kvalita |
| 15 | D7 | M7 | [TME](https://www.tme.eu/en/details/m7-dc/smd-universal-diodes/dc-components/m7/) | **SMA** | 1kV/1A, SMD ekvivalent 1N4007 |

### Upozornenia pri objednávke

- **U1 (HLK-30M12):** Nie je na TME. Objednať Hi-Link originál (AliExpress, eBay). Pozor na podvrhy.
- **U3 (AMS1117 náhrada):** TME nemá AMS1117. Dve možnosti:
  - **LD1117AS33TR** — overená klasika, 3.3V/1A, SOT-223 ([TME SK link](https://www.tme.eu/sk/details/ld1117as33tr/stabilizatory-napatia-neregulovane-ldo/stmicroelectronics/))
  - **LDL1117S33R** — novší, 3.3V/**1.2A**, nižší dropout (350mV vs 1.1V), odporúčam ak je na sklade
- **U4 (LM7805):** Použiť SMD verziu **L7805ABD2T-TR** v D2PAK puzdre (±2% tolerancia, 7042 ks na sklade). Pôvodný L7805CD2T-TR má nefunkčný link (404).
- **U6, U8 (CA3140EZ):** DIP-8 verzia, ✅ 542 ks na sklade TME. SMD verzia (CA3140AMZ) mala 0 ks, preto prechod na THT DIP-8.
- **U12 (PC817 → LTV-356T):** SMD náhrada optočlena. LTV-356T (Lite-On) je SMD SOP-4, 3.75kV izolácia, kompatibilný pinout. Puzdro sa zmení z DIP-4 na SOP-4.
- **Q1-Q4 (IRLZ44N):** IRLZ44NSPBF aj IRLZ44ZSPBF vyradené, IRLZ44NSTRLPBF má min. 800 ks. Náhrada: **IRLR2905TRPBF** (DPAK, 55V/30A, logic-level Vgs_th 1-2V, Rds_on 27mΩ). Pre naše záťaže (čerpadlo ~2A, relé ~44mA, externé max ~10A) je 30A viac ako dosť. DPAK je menšie ako D2PAK — treba prispôsobiť footprint!
- **U7, U9 (TL071IP):** DIP-8 verzia, ✅ 928 ks na sklade TME. TL071IDT (SOIC-8) mala 0 ks, preto prechod na THT DIP-8. TL071 je nižší šum ako TL081.
- **D3-D6 (SS14):** SS14-DC (DC Components) má 0 ks. Skúsiť **SS14-TSC** (Taiwan Semiconductor) alebo **SS14-E3/61T** (Vishay) — obe SMA puzdro, overiť dostupnosť na TME.
- **D2 (SS34):** Pôvodný SS34-CDI mal 0 ks. Nahradený **SS34-ONS** (ONSEMI) v SMC puzdre — ✅ 1006 ks na sklade. Pozor: SMC (DO-214AB) je väčší ako SMA, treba prispôsobiť footprint!
- **D7 (1N4007 → M7):** Použiť **M7** — SMD ekvivalent 1N4007 v SMA puzdre (1kV/1A). Rovnaké parametre.
- **Rezistory, kondenzátory, ferity** — bežné 0805 súčiastky, TME má stovky možností. Vybrať podľa ceny/dostupnosti.

---

## Kompletný nákupný zoznam — pasívne súčiastky a konektory

Toto dopĺňa TME tabuľku vyššie (IC a polovodiče). Všetky rezistory a keramické kondenzátory sú **0805 SMD** (okrem kde uvedené inak).

### Rezistory (0805, 1%, 0.125W)

| Hodnota | Počet | Ref | Použitie |
|---------|-------|-----|----------|
| 100Ω | 5 | R20-R23, R30 | Gate MOSFET (4×), RC snubber (1×) |
| 330Ω | 1 | R28 | Optočlen LED |
| 1kΩ | 4 | R1, R5, R12, R29 | LED predradný, bias (2×), optočlen kolektor |
| 2.2kΩ | 2 | R3, R10 | Feedback op-amp |
| 4.7kΩ | 3 | R16, R17, R31 | I2C pull-up (2×), 1-Wire pull-up (1×) |
| 10kΩ | 6 | R18, R19, R24-R27 | ESP32 EN+IO0 (2×), gate pull-down (4×) |
| 30kΩ | 4 | R6, R7, R13, R14 | Zosilňovač gain |
| 75kΩ | 2 | R8, R15 | Offset referencia |
| 4.7MΩ | 2 | R2, R9 | Vstupný bias sonda |
| **Celkom rezistory** | **29** | | |

### Trimre

| Hodnota | Počet | Ref | Použitie |
|---------|-------|-----|----------|
| 5kΩ multi-turn | 2 | R4, R11 | Kalibrácia pH/ORP offset |

### Keramické kondenzátory (0805, 50V, X7R/X5R)

| Hodnota | Počet | Ref | Použitie |
|---------|-------|-----|----------|
| 2.2nF | 2 | C13, C19 | VF filter sonda |
| 100nF | 11 | C1, C6, C8, C15-C18, C21-C24 | Bypass (PSU 1×, LM7805 2×, op-amp 8×) |
| 100nF | 2 | C25, C27 | Bypass ADC + ESP32 (100nF časť) |
| 1µF | 3 | C11, C14, C20 | Flying cap TPS60400 (1×), freq. komp. (2×) |
| 10µF | 4 | C4, C7, C9, C12 | LDO vstup (1×), LM7805 filter (2×), TPS60400 výstup (1×) |
| 10µF | 2 | C26, C28 | Bypass ADC + ESP32 (10µF časť) |
| 22µF (1206) | 1 | C5 | LDO výstup — **puzdro 1206!** |
| **Celkom keramické** | **25** | | |

### Elektrolytické kondenzátory (radiálne SMD alebo THT)

| Hodnota | Počet | Ref | Použitie |
|---------|-------|-----|----------|
| 47µF/16V | 1 | C10 | LC filter analóg |
| 220µF/10V | 1 | C3 | Buck výstup |
| 680µF/25V | 1 | C2 | Buck vstup |
| **Celkom elektrolytické** | **3** | | |

### Špeciálne kondenzátory

| Hodnota | Počet | Ref | Použitie |
|---------|-------|-----|----------|
| 100nF/275VAC X2 | 1 | C29 | RC snubber relé — **safety rated!** |

### Tlmivky a ferity

| Komponent | Hodnota | Počet | Ref | Puzdro |
|-----------|---------|-------|-----|--------|
| Výkonová tlmivka | 33µH / 3A | 1 | L1 | SMD výkonová (napr. 12×12mm) |
| Tlmivka | 10µH | 1 | L2 | 0805 |
| Feritová perla | 600Ω@100MHz | 2 | FB1, FB2 | 0805 |

### Diódy (už v TME tabuľke vyššie)

| Komponent | Počet | Ref | Puzdro |
|-----------|-------|-----|--------|
| LED modrá | 1 | D1 | 0805 |
| SS34 (Schottky 40V/3A) | 1 | D2 | SMC |
| SS14 (Schottky 40V/1A) | 4 | D3-D6 | SMA |
| M7 (1kV/1A) | 1 | D7 | SMA |

### Varistor a poistka

| Komponent | Hodnota | Počet | Ref | Poznámka |
|-----------|---------|-------|-----|----------|
| Varistor | 275V | 1 | MOV1 | Disc, ochrana relé kontaktov |
| Poistka + holder | 2A T, 5×20mm | 1 | F1 | Na PCB, pomalá |

### Konektory

| Komponent | Počet | Ref | Rozteč | Poznámka |
|-----------|-------|-----|--------|----------|
| BNC right-angle PCB mount | 2 | P1, P2 | — | pH + ORP sonda, 50Ω, Amphenol B6252HA-NPP3G-50 [TME](https://www.tme.eu/sk/details/b6252ha-npp3g-50/konektory-bnc/amphenol-rf/) |
| Šróbovacia svorkovnica 3-pin (250V) | 2 | J1, J11 | 7.5mm (alebo 7.62mm) | 230V vstup + výstup, min. 16A |
| Šróbovacia svorkovnica 2-pin | 2 | J9, J10 | 5.0mm (alebo 5.08mm) | MOSFET výstupy Q3, Q4, 12V |
| Pin header 1×14 | 1 | J2 | 2.54mm | Display konektor |
| JST-XH 3-pin | 4 | J3-J6 | 2.50mm | 1-Wire senzory (DS18B20) |
| Pin header 2×10 | 1 | J7 | 2.54mm | Voľné GPIO |
| Pin header 1×4 | 1 | J8 | 2.54mm | Debug UART |
| **Celkom konektory** | **13** | | | |

### Súhrn na objednanie

| Kategória | Počet kusov |
|-----------|-------------|
| Rezistory 0805 | 29 |
| Trimre | 2 |
| Keramické kondenzátory | 25 |
| Elektrolytické kondenzátory | 3 |
| Kondenzátor X2 | 1 |
| Tlmivky | 2 |
| Feritové perly | 2 |
| LED | 1 |
| Diódy (SS34+SS14+M7) | 6 |
| Varistor | 1 |
| Poistka + holder | 1 |
| Konektory | 13 |
| IC a moduly (viď TME tabuľka) | 12 |
| MOSFETy | 4 |
| Relé | 1 |
| **Celkom** | **~103 súčiastok** |

---

## Poznámky

- Toto je experimentálna doska — voľné GPIO sú vyvedené na J7 pin header
- Display nie je na doske — pripojený cez J2 (14-pin konektor)
- Čerpadlo NKP-DCL-B10D je v boxe, priamo pripojené na Q1
- ORP front-end je rovnaký ako pH, len iná sonda a kalibrácia
- V budúcej verzii sa doplnia funkcie podľa experimentov
