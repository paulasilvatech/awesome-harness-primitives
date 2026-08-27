---
name: legacy-circuit-mockups
description: >-
  Generates breadboard circuit mockups and visual electronics diagrams with HTML5 Canvas
  conventions for retro computers, 6502 builds, 555 timer circuits, EEPROM/RAM/VIA wiring,
  7400-series logic, LEDs, resistors, capacitors, switches, and wires. Use this skill when asked
  to create circuit layouts, visualize component placement, draw breadboard diagrams, mock up
  vintage electronics, or design Ben Eater-style projects.
---

<!-- Generated from harness/github-copilot/plugins/iot-embedded-systems/skills/legacy-circuit-mockups/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Legacy circuit mockups

Create breadboard circuit mockups and visual diagrams for retro computing and electronics projects. Translate the requested circuit into component placement, pin-aware wiring, color conventions, and an HTML5 Canvas-style representation that a builder can follow.

## When to invoke

- "Create a breadboard layout for this circuit."
- "Mock up a 6502 computer on a breadboard."
- "Draw a 555 timer LED blinker diagram."
- "Visualize the wire connections between these components."
- "Make an educational electronics diagram for a Ben Eater-style build."

## Prerequisites and context

- Use bundled pinout and build references when exact chip behavior matters.
- Apply breadboard layout conventions: rows, columns, center channel, power rails, and consistent grid spacing.
- Treat diagrams as build aids, not certified electrical designs; preserve component polarity, power, and ground explicitly.

## Supported components

| Component | Pins | Use in mockups |
| --- | ---: | --- |
| `W65C02S` | 40-pin DIP | 8-bit microprocessor with 16-bit address bus. |
| `28C256` | 28-pin DIP | 32KB parallel EEPROM. |
| `W65C22` | 40-pin DIP | Versatile Interface Adapter (`VIA`). |
| `62256` / `6C62256` | 28-pin DIP | 32KB static RAM. |
| `NE555` | 8-pin DIP | Timer IC for timing and oscillation. |
| `7400` | 14-pin DIP | Quad 2-input NAND gate. |
| `7402` | 14-pin DIP | Quad 2-input NOR gate. |
| `7404` | 14-pin DIP | Hex inverter (`NOT`) gate. |
| `7408` | 14-pin DIP | Quad 2-input AND gate. |
| `7432` | 14-pin DIP | Quad 2-input OR gate. |
| LED | 2 leads | Light emitting diode; show anode/cathode. |
| Resistor | 2 leads | Current limiting or timing. |
| Capacitor | 2 leads | Filtering and timing; distinguish ceramic/electrolytic. |
| Crystal | 2 leads | Clock oscillator. |
| Switch | 2+ leads | Latching toggle. |
| Button | 2+ leads | Momentary push button. |
| Potentiometer | 3 leads | Variable resistor. |
| Photoresistor | 2 leads | Light-dependent resistor. |

## Canvas model

Use a deterministic grid and object model so the diagram can be rendered or recreated.

```javascript
// Standard breadboard grid: 20px spacing
const gridSize = 20;
const cellX = Math.floor(x / gridSize) * gridSize;
const cellY = Math.floor(y / gridSize) * gridSize;
```

```javascript
// All components follow this structure:
{
  type: 'component-type',
  x: gridX,
  y: gridY,
  width: componentWidth,
  height: componentHeight,
  rotation: 0,  // 0, 90, 180, 270
  properties: { /* component-specific data */ }
}
```

```javascript
// Wire connection format:
{
  start: { x: startX, y: startY },
  end: { x: endX, y: endY },
  color: '#ff0000'  // Wire color coding
}
```

## Pinout quick reference

| Chip | Pin | Name | Function |
| --- | ---: | --- | --- |
| `NE555` | 1 | `GND` | Ground (`0V`). |
| `NE555` | 2 | `TRIG` | Trigger; `< 1/3 Vcc` starts timing. |
| `NE555` | 3 | `OUT` | Output; source/sink up to `200mA`. |
| `NE555` | 4 | `RESET` | Active-low reset. |
| `NE555` | 5 | `CTRL` | Control voltage; bypass with `10nF`. |
| `NE555` | 6 | `THR` | Threshold; `> 2/3 Vcc` resets. |
| `NE555` | 7 | `DIS` | Discharge, open collector. |
| `NE555` | 8 | `Vcc` | Supply, `+4.5V` to `+16V`. |
| `W65C02S` | 8 | `VDD` | Power supply. |
| `W65C02S` | 21 | `VSS` | Ground. |
| `W65C02S` | 37 | `PHI2` | System clock input. |
| `W65C02S` | 40 | `RESB` | Active-low reset. |
| `W65C02S` | 34 | `RWB` | Read/Write signal. |
| `W65C02S` | 9-25 | `A0-A15` | Address bus. |
| `W65C02S` | 26-33 | `D0-D7` | Data bus. |
| `28C256` | 14 | `GND` | Ground. |
| `28C256` | 28 | `VCC` | Power supply. |
| `28C256` | 20 | `CE` | Chip enable, active-low. |
| `28C256` | 22 | `OE` | Output enable, active-low. |
| `28C256` | 27 | `WE` | Write enable, active-low. |
| `28C256` | 1-10, 21-26 | `A0-A14` | Address inputs. |
| `28C256` | 11-19 | `I/O0-I/O7` | Data bus. |

## Build patterns

| Circuit | Placement and wiring sequence |
| --- | --- |
| Basic LED | Use step-by-step placement. Define breadboard dimensions and grid; connect `+5V` and `GND`; place LED with anode/cathode orientation; place current-limiting resistor; draw wires and labels. |
| Single LED build | Components: red LED, `220Ω` resistor, jumper wires, power source. Insert black jumper from power `GND` to row `A5`; red jumper from `+5V` to row `J5`; align LED cathode with ground; place `220Ω` resistor between power and LED anode. |
| 555 astable blinker | Place `NE555` straddling the center channel; connect pin `1` to `GND`, pin `8` to `+5V`, pin `4` to pin `8`; wire `10kΩ` between pin `7` and `+5V`; wire `100kΩ` between pins `6` and `7`; wire `10µF` between pin `6` and `GND`; connect pin `3` to LED circuit. |
| 6502 microprocessor layout | Center `W65C02S`; add `28C256` EEPROM, `W65C22` VIA, `7400-series` address decoding, address bus `A0-A15`, data bus `D0-D7`, control signals `R/W`, `PHI2`, `RESB`, reset button, and clock crystal. |

## Formulas and conventions

| Topic | Formula or convention |
| --- | --- |
| Ohm's Law | `V = I × R` |
| LED current resistor | `R = (Vcc - Vled) / Iled` |
| Power | `P = V × I = I² × R` |
| 555 astable frequency | `f = 1.44 / ((R1 + 2×R2) × C)` |
| 555 high time | `t₁ = 0.693 × (R1 + R2) × C` |
| 555 low time | `t₂ = 0.693 × R2 × C` |
| 555 duty cycle | `D = (R1 + R2) / (R1 + 2×R2) × 100%` |
| 555 monostable pulse | `T = 1.1 × R × C` |
| Capacitive reactance | `Xc = 1 / (2πfC)` |
| Capacitor energy | `E = ½ × C × V²` |

| Wire color | Purpose |
| --- | --- |
| Red | `+5V` / power. |
| Black | Ground. |
| Yellow | Clock / timing. |
| Blue | Address bus. |
| Green | Data bus. |
| Orange | Control signals. |
| White | General purpose. |

| LED color | Forward voltage |
| --- | --- |
| Red | `1.8V - 2.2V` |
| Green | `2.0V - 2.2V` |
| Yellow | `2.0V - 2.2V` |
| Blue | `3.0V - 3.5V` |
| White | `3.0V - 3.5V` |

## Gotchas

- **LED polarity matters**: anode goes toward positive supply through a resistor; cathode goes toward ground.
- **IC orientation matters**: pin 1 and the notch/dot determine all subsequent pin positions.
- **Power rails may be split**: show jumpers that bridge rail breaks when the mockup assumes continuous `+5V` or `GND`.
- **6502 buses get unreadable fast**: bundle address, data, and control wires by color and label bus ranges instead of drawing ambiguous spaghetti.

## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| LED does not light | Polarity or missing current path | Check anode to positive, cathode to negative, and resistor placement. |
| Circuit does not power | Rail or jumper omission | Verify `VCC`, `VDD`, `VSS`, `GND`, and rail continuity. |
| Threshold/trigger wiring is unclear | 555 timing node is ambiguous | Label `threshold/trigger` connections and mark `HIGH` reset state when pin 4 is tied to Vcc. |
| IC not working | Power pins or orientation wrong | Check notch/dot, pin 1, `VCC`, and `GND`. |
| 555 not oscillating | Trigger/threshold capacitor wiring wrong | Verify `TRIG`, `THR`, `DIS`, timing resistors, and capacitor polarity. |
| Microprocessor stuck | Reset or clock invalid | Check `RESB` is high after reset pulse and `PHI2` is present. |

## Progressive disclosure and bundled resources

Load bundled references only when the component, emulator, or build step is relevant.

- `references/555.md`: complete 555 timer IC specification.
- `references/6502.md`: MOS 6502 microprocessor details.
- `references/6522.md`: `W65C22` VIA interface adapter.
- `references/28256-eeprom.md`: `AT28C256` EEPROM specification.
- `references/6C62256.md`: `62256` SRAM details.
- `references/7400-series.md`: TTL logic gate pinouts.
- `references/assembly-compiler.md`: assembly compiler specification.
- `references/assembly-language.md`: assembly language specification.
- `references/basic-electronic-components.md`: resistors, capacitors, switches.
- `references/breadboard.md`: breadboard specifications.
- `references/common-breadboard-components.md`: comprehensive component reference.
- `references/connecting-electronic-components.md`: step-by-step (`by-step`) build guides with `ceramic/electrolytic` capacitor notes.
- `references/emulator-28256-eeprom.md`: emulating `28256-eeprom` specification.
- `references/emulator-6502.md`: emulating `6502` specification.
- `references/emulator-6522.md`: emulating `6522` specification.
- `references/emulator-6C62256.md`: emulating `6C62256` specification.
- `references/emulator-lcd.md`: emulating a `LCD` specification.
- `references/lcd.md`: LCD display interfacing.
- `references/minipro.md`: EEPROM programmer usage.
- `references/t48eeprom-programmer.md`: T48 programmer reference.

## Output template

````markdown
## Circuit mockup — <circuit name>

**Status:** ready | needs clarification | blocked
**Format:** HTML5 Canvas plan | breadboard layout | wiring table
**Assumptions:** <supply voltage, breadboard type, component variants>

### Components
| Ref | Component | Value/model | Placement | Notes |
| --- | --- | --- | --- | --- |
| U1 | NE555 | timer IC | center channel, rows <range> | notch points left |

### Wiring
| Wire | From | To | Color | Purpose |
| --- | --- | --- | --- | --- |
| W1 | +5V rail | U1 pin 8 Vcc | Red | power |

### Canvas model
```javascript
<component and wire objects>
```

### Build notes
- <polarity, pinout, formula, or troubleshooting note>
````

## Quality gate

- [ ] Every IC has model, package, orientation, power pins, and ground pins shown.
- [ ] LED, electrolytic capacitor, diode, and power polarity are explicit.
- [ ] Current-limiting resistors are present for LED loads.
- [ ] Wires use the color convention for power, ground, clock, buses, and controls.
- [ ] Bus labels such as `A0-A15`, `D0-D7`, `R/W`, `PHI2`, and `RESB` match the pinout.
- [ ] Formulas used for timing or resistors are shown with the chosen component values.
- [ ] Any referenced bundled file exists under `references/` and was loaded only when needed.
