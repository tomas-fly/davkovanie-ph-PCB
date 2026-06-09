# pH/ORP Monitor — Plán tvorby KiCad schémy

## Stav projektu
- **Špecifikácia:** SPECIFIKACIA.md (kompletná, schválená užívateľom)
- **Schéma:** ph-meter-v1.kicad_sch (ešte neexistuje)
- **Formát:** KiCad 8 S-expression (.kicad_sch)
- **Pracovný adresár:** /Users/ing.tomaslaso/Documents/kiCad/ph-verzion-01/

---

## Postup — 10 krokov (menšie bloky = menej chýb)

Každý krok je navrhnutý tak, aby obsahoval max ~5-8 súčiastok a bol
nezávisle testovateľný. Po každom kroku aktualizujem stav na ✅.

---

### Krok 1: Kostra schémy + 230V vstup
**Stav:** ✅ Hotové (2026-06-03)
**Zložitosť:** Nízka (~4 súčiastky)
**Čo:** Vytvorí .kicad_sch súbor, hlavičku, nastaví formát. Pridá 230V vstup.
**Súčiastky:**
- J_AC_IN: Šróbovacia svorkovnica 3-pin (L, N, PE)
- F1: Poistka 2A T, 5×20mm holder
- U_PSU: HLK-30M12 (230VAC → 12V)
  - AC_L, AC_N vstup; +12V, GND výstup
  - C_PSU: 100nF bypass na 12V výstupe
- LED1: Modrá LED + R_LED (1kΩ) na 12V (indikátor)
- PWR_FLAG na +12V a GND

**Nety:** AC_L, AC_N, PE, +12V, GND
**Výstup:** Funkčný .kicad_sch s napájaním 12V

---

### Krok 2: Buck 12V → 5V (digitálna)
**Stav:** ✅ Hotové (2026-06-03)
**Zložitosť:** Stredná (~5 súčiastok)
**Čo:** LM2596 buck konvertor pre digitálnu 5V vetvu.
**Súčiastky:**
- U_BUCK: LM2596S-5.0 (TO-263)
  - Pin 1: IN (+12V)
  - Pin 2: OUT (→ L1 → +5V)
  - Pin 3: GND
  - Pin 4: FB (spojený s OUT pre fixed 5V verziu)
  - Pin 5: ON/OFF (→ GND = always on)
- L1: 33µH tlmivka
- D_BUCK: SS34 (SMA) Schottky
- C_BUCK_IN: 680µF/25V elektrolyt
- C_BUCK_OUT: 220µF/10V elektrolyt

**Nety:** +12V → +5V
**Výstup:** 5V rail pre digitálnu sekciu

---

### Krok 3: LDO 5V → 3.3V
**Stav:** ✅ Hotové (2026-06-03)
**Zložitosť:** Nízka (~3 súčiastky)
**Čo:** AMS1117 LDO pre ESP32.
**Súčiastky:**
- U_LDO: AMS1117-3.3 (SOT-223)
  - Pin 1: GND
  - Pin 2: VOUT (+3V3)
  - Pin 3: VIN (+5V)
- C_LDO_IN: 10µF keramický
- C_LDO_OUT: 22µF keramický

**Nety:** +5V → +3V3
**Výstup:** 3.3V rail pre ESP32

---

### Krok 4: Analógové napájanie (+5V_AN, -5V_AN)
**Stav:** ✅ Hotové (2026-06-03)
**Zložitosť:** Stredná (~8 súčiastok)
**Čo:** Čistá analógová vetva — lineárny regulátor + charge pump.
**Súčiastky:**

LM7805 (12V → +5V_AN):
- U_VREG_AN: LM7805 (TO-220)
  - Pin 1: IN (+12V), Pin 2: GND, Pin 3: OUT (+5V_AN)
- C_AN_IN1: 100nF, C_AN_IN2: 10µF
- C_AN_OUT1: 100nF, C_AN_OUT2: 10µF
- FB1: Feritová perla na +5V_AN výstupe

TPS60400DBVR (+5V_AN → -5V_AN):
- U_CP: TPS60400DBVR (SOT-23-5)
  - Pin 1: IN (+5V_AN)
  - Pin 2: GND
  - Pin 3: C+
  - Pin 4: C-
  - Pin 5: OUT (-5V_AN)
- C_FLY: 1µF keramický (C+ → C-)
- C_CP_OUT: 10µF keramický na OUT
- FB2: Feritová perla na -5V_AN výstupe

**Nety:** +12V → +5V_AN, +5V_AN → -5V_AN
**Výstup:** ±5V_AN rails pre op-ampy

---

### Krok 5: pH front-end (CA3140 + TL081)
**Stav:** ✅ Hotové (2026-06-02)
**Zložitosť:** Stredná (~8 súčiastok + bypass caps)
**Čo:** pH sonda → buffer → zosilňovač → pH_OUT
**Súčiastky:**

BNC vstup:
- P1_pH: BNC konektor (Signal → R1, Shield → AGND)

CA3140AMZ buffer (U1):
- Pin 3 (+): ← R1 (4.7MΩ) ← BNC signal
- Pin 3 (+): C1 (2.2nF) → AGND (VF filter)
- Pin 2 (-): ← feedback sieť (C2 1µF, R4 2.2kΩ, R5 5kΩ trimer, R6 1kΩ)
- Pin 7: +5V_AN, Pin 4: -5V_AN
- Pin 6: výstup (pH_BUFFERED)
- Bypass: C_U1+ (100nF), C_U1- (100nF) na napájacie piny

TL081CDT zosilňovač (U2):
- Pin 2 (-): ← R8 (30kΩ) ← pH_BUFFERED; R7 (30kΩ) feedback z pin 6
- Pin 3 (+): ← R9 (75kΩ) → referencia/offset
- Pin 7: +5V_AN, Pin 4: -5V_AN
- Pin 6: výstup (pH_OUT → ADS1115 AIN0)
- Bypass: C_U2+ (100nF), C_U2- (100nF)

**Nety:** pH_SIGNAL, pH_BUFFERED, pH_OUT

---

### Krok 6: ORP front-end (kópia pH)
**Stav:** ✅ Hotové (2026-06-03)
**Zložitosť:** Stredná (identické ako krok 5)
**Čo:** ORP sonda → buffer → zosilňovač → ORP_OUT
**Súčiastky:** Rovnaké ako krok 5, s prefixom ORP:
- P2_ORP: BNC konektor
- U3: CA3140AMZ (buffer)
- U4: TL081CDT (zosilňovač)
- R11-R19: rovnaké hodnoty ako R1-R9
- C11-C18: rovnaké hodnoty
- Výstup: ORP_OUT → ADS1115 AIN1

**Nety:** ORP_SIGNAL, ORP_BUFFERED, ORP_OUT

---

### Krok 7: ADS1115 ADC
**Stav:** ✅ Hotové (2026-06-03)
**Zložitosť:** Nízka (~4 súčiastky)
**Čo:** 16-bit ADC, I2C, prijíma pH_OUT a ORP_OUT
**Súčiastky:**
- U_ADC: ADS1115IDGSR (MSOP-10)
  - VDD: +3V3
  - GND: GND
  - SDA: → net SDA (GPIO26)
  - SCL: → net SCL (GPIO27)
  - ADDR: → GND (I2C 0x48)
  - ALRT/RDY: NC
  - AIN0: ← pH_OUT
  - AIN1: ← ORP_OUT
  - AIN2: voľný (vyvedený na pad)
  - AIN3: voľný (vyvedený na pad)
- C_ADC: 100nF bypass na VDD
- R_SDA: 4.7kΩ pull-up → +3V3
- R_SCL: 4.7kΩ pull-up → +3V3

**Nety:** SDA, SCL, pH_OUT, ORP_OUT

---

### Krok 8: ESP32-WROOM-32E
**Stav:** ✅ Hotové (2026-06-03)
**Zložitosť:** Stredná (~5 súčiastok + veľa net labels)
**Čo:** MCU modul s boot obvodom a GPIO net labels
**Súčiastky:**
- U_MCU: ESP32-WROOM-32E-N4
  - 3V3 (pin 2) ← +3V3
  - GND (pin 1, 15, 38) → GND
  - EN (pin 3) ← R_EN (10kΩ → +3V3) + C_EN (100nF → GND)
  - IO0 (pin 25) ← R_IO0 (10kΩ → +3V3)
- C_MCU1: 100nF bypass na 3V3
- C_MCU2: 10µF bypass na 3V3

GPIO net labels (len labels, pripojenia sú v iných krokoch):
- GPIO26 → SDA
- GPIO27 → SCL
- GPIO18 → SPI_SCK
- GPIO23 → SPI_MOSI
- GPIO19 → SPI_MISO
- GPIO15 → TFT_CS
- GPIO2 → TFT_DC
- GPIO4 → TFT_RST
- GPIO32 → TFT_BL
- GPIO21 → TOUCH_CS
- GPIO39 → TOUCH_IRQ
- GPIO33 → MOSFET1_GATE
- GPIO25 → RELAY_CTRL
- GPIO13 → MOSFET3_GATE
- GPIO14 → MOSFET4_GATE
- GPIO5 → ONEWIRE_DATA
- GPIO1 → UART_TX
- GPIO3 → UART_RX

**Nety:** Všetky vyššie uvedené

---

### Krok 9: Výstupy (4× MOSFET + relé)
**Stav:** ✅ Hotové (2026-06-03)
**Zložitosť:** Stredná (~15 súčiastok, ale opakujúce sa vzory)
**Čo:** 4 MOSFET kanály + PC817 + relé + 230V výstup

4× MOSFET kanál (Q1-Q4, identické):
- Qn: IRLZ44NPBF (TO-220) — Gate, Drain, Source
  - Gate ← R_gate_n (100Ω) ← net label (MOSFET1_GATE atď.)
  - Gate ← R_pd_n (10kΩ) → GND
  - Source → GND
  - Drain → konektor + D_n (SS14, katóda→+12V, anóda→drain)
- Konektory Q3, Q4: Šróbovacia svorkovnica 2-pin (+12V + drain)
- Q1: interný (čerpadlo), Q2: interný (relé cievka)

Relé obvod:
- U_OPTO: PC817
  - Pin 1 (A) ← R_opto_in (330Ω) ← RELAY_CTRL (GPIO25)
  - Pin 2 (K) → GND
  - Pin 4 (C) ← +12V cez R_opto_out (1kΩ)
  - Pin 3 (E) → GND
  - Collector → MOSFET2_GATE (namiesto priameho GPIO)
- RLY1: Finder 40.52.9.012
  - Cievka: +12V → drain Q2
  - D_RLY: 1N4007 cez cievku
- Kontakty relé:
  - COM → J_AC_OUT pin L_out
  - NO → AC_L (zo vstupu cez poistku)
- RC snubber: R_snub (100Ω) + C_snub (100nF X2) na kontaktoch
- MOV1: 275V varistor na kontaktoch

230V výstup:
- J_AC_OUT: Šróbovacia svorkovnica 3-pin (L_out, N_out, PE)
  - N_out: priamo z J_AC_IN N
  - PE: priamo z J_AC_IN PE

**Nety:** MOSFET1_GATE..4, RELAY_CTRL, PUMP_OUT, RELAY_COIL+/-

---

### Krok 10: Periférie (display, 1-Wire, GPIO header, UART)
**Stav:** ❌ Nehotové
**Zložitosť:** Nízka (~5 konektorov + 1 rezistor)
**Čo:** Všetky externé konektory a rozšírenia

Display konektor:
- J_DISP: Pin header 1×14 (2.54mm)
  - Pin 1: +3V3
  - Pin 2: GND
  - Pin 3: TFT_CS (GPIO15)
  - Pin 4: TFT_RST (GPIO4)
  - Pin 5: TFT_DC (GPIO2)
  - Pin 6: SPI_MOSI (GPIO23)
  - Pin 7: SPI_SCK (GPIO18)
  - Pin 8: TFT_BL (GPIO32)
  - Pin 9: SPI_MISO (GPIO19)
  - Pin 10: SPI_SCK (GPIO18, zdieľaný)
  - Pin 11: TOUCH_CS (GPIO21)
  - Pin 12: SPI_MOSI (GPIO23, zdieľaný)
  - Pin 13: SPI_MISO (GPIO19, zdieľaný)
  - Pin 14: TOUCH_IRQ (GPIO39)

1-Wire:
- J_1W_1 až J_1W_4: JST-XH 3-pin
  - Pin 1: +3V3
  - Pin 2: ONEWIRE_DATA (GPIO5) — všetky paralelne
  - Pin 3: GND
- R_1W: 4.7kΩ pull-up (ONEWIRE_DATA → +3V3)

Voľný GPIO header:
- J_EXT: Pin header 2×10 (2.54mm)
  - Riadok 1: GPIO12, GPIO16, GPIO17, GPIO22, GPIO34, GPIO35, GPIO36, +3V3, +5V, GND
  - Riadok 2: GND pod každým GPIO (pre jednoduché pripojenie)

Debug UART:
- J_UART: Pin header 1×4 (2.54mm)
  - Pin 1: +3V3
  - Pin 2: UART_TX (GPIO1)
  - Pin 3: UART_RX (GPIO3)
  - Pin 4: GND

---

## KiCad technické poznámky

- **Verzia:** KiCad 8 formát
- **Knižnice symbolov:** Použiť štandardné KiCad 8 knižnice kde možné
  - Symboly ktoré neexistujú: HLK-30M12 (generický modul), TPS60400 (generický SOT-23-5)
  - Pre tieto vytvoriť jednoduché custom symboly priamo v schéme
- **Power symbols:** +12V, +5V, +3V3, +5V_AN, -5V_AN, GND, AGND — štandardné KiCad power symboly
- **Net labels:** Konzistentné pomenovanie, rovnaký label = rovnaký net
- **Poznámky v schéme:** Textové bloky pri každom bloku (napr. "POWER SUPPLY", "pH FRONT-END")

---

## Dôležité pravidlá

1. **AGND vs GND:** Analógová zem (AGND) oddelená od digitálnej (GND), star-point
2. **+5V_AN vs +5V:** Analógová 5V (LM7805) oddelená od digitálnej (LM2596)
3. **Creepage 230V:** Min 6mm medzi HV a LV
4. **Guard ring:** Okolo vstupov CA3140
5. **Bypass caps:** Každý IC vlastné, čo najbližšie

---

## Ako pokračovať po reštarte

1. Prečítaj tento PLAN.md — nájdi prvý krok so stavom ❌
2. Prečítaj SPECIFIKACIA.md pre detaily
3. Otvor/vytvor ph-meter-v1.kicad_sch a pridaj ďalší blok
4. Po dokončení kroku zmeň stav na ✅ v tomto súbore
5. Pokračuj ďalším krokom
