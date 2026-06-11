# KiCad Routing Tips

## Klávesové skratky

| Klávesa | Funkcia |
|---------|---------|
| X | Prepne routovací režim (push&shove) |
| / | Zobrazí/skryje ratsnest (modré čiary nespojených netov) |
| W | Prepína šírku trasy počas routingu |
| +/- | Prepínanie vrstiev (F.Cu / B.Cu) |
| V | Vloží via (prechod medzi vrstvami) |
| ` (backtick) | Prepne vrstvu počas routingu + automaticky pridá via |
| D | Prepína medzi 45° a oblúkovým ohýbaním |
| Backspace | Zmaže posledný segment (krok späť) |
| Esc | Zruší aktuálnu trasu |
| U | Vyberie celú trasu |
| B | Aktualizuje copper zones |
| I | Routovanie diferenciálnych párov |
| Ctrl+klik na net | Zvýrazní celý net |

## Šírky trás

| Typ | Šírka |
|-----|-------|
| 230V AC | min. 1mm, clearance min. 2mm od signálov |
| Power (12V, 5V, 3.3V) | 0.5 - 1mm |
| Signály | 0.25mm |

## Postup routingu

### 1. GND zóna na B.Cu (spodná vrstva)

Celú spodnú vrstvu dosky pokryješ medenou zónou pripojenou na GND. Tým sa automaticky prepoja
všetky GND piny cez vias — nemusíš routovať stovky GND spojov ručne.

**Ako na to:**
- Umiestniť → Zóna (alebo klikni na ikonu zóny v pravom paneli)
- Vyber vrstvu **B.Cu**
- V dialógu vyber net **GND**
- Nakresli obdĺžnik okolo celej dosky (po Edge.Cuts okraji)
- Stlač **B** na aktualizáciu — zóna sa vyplní meďou a automaticky sa pripojí ku všetkým GND padom

Potom pri routingu stačí ku GND padu pridať via (V) a je pripojený cez spodný GND plane.

### 2. Power trasy na F.Cu (vrchná vrstva)

Napájacie trasy (+12V, +5V, +3.3V, ±5V_ANALOG) routuj na vrchnej vrstve, hrubšie (0.5-1mm).
Tieto vedú viac prúdu ako signály, preto musia byť širšie.

**Ako na to:**
- Stlač **X** (začni routovanie)
- Klikni na pad napájacieho pinu
- Stlač **W** na prepnutie šírky na 0.5mm alebo 1mm
- Ťahaj trasu k ďalšiemu padu rovnakého netu
- Napájacie trasy veď ako "strom" — hlavná línia a z nej odbočky ku komponentom

**Poradie:** najprv +12V (od U1 k MOSFETom, J12), potom +5V (od U2/U4), potom +3.3V (od U3 k ESP32, ADS1115), nakoniec ±5V (od U4/U5 k op-ampom).

### 3. Signálové trasy

Všetky ostatné spoje — I2C (SDA, SCL), GPIO, 1-Wire, UART, atď. Tenšie trasy (0.25mm).

**Ako na to:**
- Stlač **X**, klikni na pad
- Šírku nastav na 0.25mm (W)
- Routuj po najkratšej ceste, ohýbaj pod 45° (nie 90° — D prepína režim)
- Ak nemôžeš prejsť na F.Cu, stlač **` (backtick)** — automaticky vloží via a pokračuješ na B.Cu
- Na B.Cu pozor — nepretínaj GND zónu zbytočne veľkými trasami

### 4. 230V AC trasy

Tieto spoja J1 → F1 → U1 (vstup) a RLY1 → J11 (výstup). Musia byť široké a ďaleko od všetkého.

**Pravidlá:**
- Šírka min. **1mm** (lepšie 1.5-2mm)
- Medzera min. **2mm** od akýchkoľvek iných trás/komponentov
- Veď ich len po ľavom okraji dosky — tam kde sú 230V komponenty
- Nikdy neprechádzaj cez digitálnu alebo analógovú časť
- Medzi L (fáza) a N (neutrál) tiež dodržuj 2mm medzeru

### 5. Analógové signály — čo najkratšie

pH_OUT, ORP_OUT (z op-ampov do ADS1115) a BNC signály (z konektorov do CA3140) sú najcitlivejšie.
Každý mm navyše = viac šumu.

**Pravidlá:**
- Trasy čo najkratšie a najpriamejšie
- Neveď ich paralelne s napájacími trasami (indukuje sa šum)
- Ak musíš ísť cez via, použi len jedno — každé via pridáva odpor a kapacitu
- BNC signál (vysoká impedancia) obzvlášť krátky — preto je BNC na okraji pri op-ampoch
- Okolo analógových trás nechaj guard ring (GND trasa po oboch stranách) ak je priestor

## Pravidlá

- **230V ďaleko od signálov** — min. 2mm, ideálne viac. Ak sa niekde priblížia, je to bezpečnostné riziko
- **GND plane ako štít** — spodná GND zóna tvorí elektromagnetický štít medzi trasami na vrchu. Preto je dôležité mať ju celistvú (nerozrezanú veľkými trasami na B.Cu)
- **Buck converter (L1, D2, U2) krátke trasy** — spínací obvod vytvára ostré hrany prúdu. Čím dlhšia trasa medzi L1↔D2↔U2, tým väčšia anténa pre EMI. Tieto 3 spoj čo najkratšie, ideálne pod 10mm
- **Bypass kondenzátory blízko IC** — každý kondenzátor (C25 pri U10, C26/C27 pri ESP32, C13-C17 pri op-ampoch) musí byť max 3-5mm od napájacích pinov IC. Filtrujú šum z napájania — ak sú ďaleko, nefungujú
- **BNC signály krátke** — BNC vstup je vysokoimpedančný (>10MΩ pre pH). Dlhá trasa zachytáva rušenie ako anténa. Preto sú BNC konektory na okraji pri op-ampoch
