<img src="https://github.com/air-cbr/sphero_unsw/blob/main/sphero_bolt_plus.jpg?raw=true" alt="Sphero BOLT+" width="500" height="500"/>

# sphero_unsw

**sphero_unsw** is a fork of the [spherov2](https://github.com/artificial-intelligence-class/spherov2.py) Python library, extended to support the Sphero BOLT+ robot.

## About Us

This extension was developed by:
- [**Kathryn Kasmarik**](https://www.unsw.edu.au/staff/kathryn-kasmarik) (kathryn.kasmarik@unsw.edu.au)  
- [**Reda Ghanem**](https://redaghanem.github.io/) (reda.ghanem@unsw.edu.au)

From the School of Systems and Computing, UNSW Canberra, to support the Sphero BOLT+ robot.

This extension is intended for educational purposes, developed for students in **ZEIT1102: Introduction to Programming** at the University of New South Wales Canberra (UNSW Canberra), where Sphero BOLT+ robots are used to teach programming fundamentals and basic robotics.

## Features

- All features from the original `spherov2` library.
- Extended functionality for Sphero BOLT+.
- Compatible with Python 3.7+.

## Installation

```bash
pip install sphero_unsw
```

## Usage
Usage Example: Sphero BOLT+ Demo with sphero_unsw

This script demonstrates how to:
- Connect to first available Sphero BOLT+ via Bluetooth.
- Light up the LED in UNSW blue.
- Roll forward and then backward.
- Stop movement safely.
- Display the character 'A' in blue on the LED matrix.
- Scroll the word "UNSW" across the LED matrix.

```python
import time
from sphero_unsw import scanner
from sphero_unsw.sphero_edu import SpheroEduAPI
from sphero_unsw.types import Color

# Scan and connect to the first available BOLT+
toy = scanner.find_toy()
if not toy:
    print("No Sphero BOLT+ found. Please ensure Bluetooth is enabled and the robot is awake.")
    exit()

# Use the SpheroEduAPI context manager
with SpheroEduAPI(toy) as api:
    print(f"Connected to {toy.name}!")

    # Set LED to blue (UNSW color)
    api.set_main_led(Color(0, 0, 255))
    time.sleep(0.5)

    # Roll forward for 2 seconds at heading 0°
    print("Rolling forward...")
    api.roll(0, 100, 2)
    time.sleep(2)

    # Roll backward by using 180° heading
    print("Rolling backward...")
    api.roll(180, 100, 2)
    time.sleep(2)

    # Stop movement
    api.stop_roll()

    # Change LED to yellow before displaying text
    print("Changing LED to yellow...")
    api.set_main_led(Color(255, 255, 0))
    time.sleep(0.5)

    # Display text on the matrix
    print("Testing matrix character...")
    api.set_matrix_character("A", Color(0, 0, 255))
    time.sleep(1)

    # Scroll "UNSW" on the matrix display
    print("Displaying 'UNSW'...")
    api.scroll_matrix_text("UNSW", Color(255, 0, 0), fps=5, wait=True)
    time.sleep(8)

    print("Demo complete.")
```

## Acknowledgments

We gratefully acknowledge the original authors of the `spherov2` library:

- **Hanbang Wang** – https://www.cis.upenn.edu/~hanbangw/
- **Elionardo Feliciano**

This library [`spherov2`](https://github.com/artificial-intelligence-class/spherov2.py) was originally created for educational use in **CIS 521: Artificial Intelligence** at the University of Pennsylvania, where Sphero robots are used to help teach the foundations of AI.

## License

MIT License. See the [LICENSE](https://github.com/air-cbr/sphero_unsw/blob/main/LICENSE) file.

This library is based on the original [`spherov2`](https://github.com/artificial-intelligence-class/spherov2.py) library developed by the University of Pennsylvania.
