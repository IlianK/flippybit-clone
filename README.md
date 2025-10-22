# FlippyBit Clone

A GTK4/Python clone of ["Flippy Bit and the Attack of the Hexadecimals From Base 16"](https://flippybitandtheattackofthehexadecimalsfrombase16.com/)
an educational game to learn binary-to-hexadecimal conversion through fast-paced tower defense gameplay.

Defend against descending hexadecimal enemies by converting them to binary! 
Enemies display hex values (like 0x1F, 0xA3, 0xFF) that you must convert to binary.
Input the converted value to destroy them before they reach the bottom.

---

![image](/images/sample.png)


## How to Play
### Core Gameplay
- **Start Game**: Click "Start Game" button
- **Binary**: Use mouse or keyboard (1-8 keys) to set binary bits
- **Fire**: When your binary matches an enemy's hex value, it automatically fires
- **Enemies**: Projectile hits destroy matching enemies and increase score
- **Game Over**: If any enemy reaches the bottom, game ends and you can "Restart Game"

### Controls
- **Mouse**: Click on bit buttons to flip between 0 and 1
- **Keyboard/ Numpad**: Press keys 1-8 to flip corresponding bits (1=MSB, 8=LSB)

---

## Game Mechanics
### Binary-Hexadecimal Conversion
The game reinforces understanding of:
- 8-bit binary ranges (0000 0000 to 1111 1111)
- Hexadecimal representation (0x00 to 0xFF)

### Difficulty Curve
- **Start**: 3s between enemies, 1.0x speed
- **Progress**: -100ms spawn time per point, +0.1 speed per point
- **Maximum**: 1.5s between enemies, unlimited speed scaling

### Auto-Fire System
- **Matching**: Compares current binary input against all active enemies
- **Target Selection**: Always targets the lowest (most urgent) matching enemy
- **Visual Feedback**: Projectile shows which enemy is being targeted
- **Auto-Reset**: Bits reset after successful hit

---

## Build & Run
### Prerequisites
- GTK4
- Python 3
- Meson build system

```
meson setup build
meson compile -C build
./build/src/flippybit
```


