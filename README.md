# Month‑Day Puzzle Solver

A simple Python application with a Tkinter GUI that solves the “month‑day” tiling puzzle. You enter a month and day, and the program removes those two cells as holes and then fits the eight puzzle pieces (which can flip and rotate) into the remaining board. The solution is displayed graphically, with each piece in its color and the holes in black.

## Features

* **GUI input** for month (1–12) and day (1–31)
* **Backtracking solver** that considers all flips and rotations of each piece
* **Graphical display** using Tkinter:

  * Board grid
  * Black squares for the two holes
  * Colored squares for each placed piece

## Requirements

* Python 3.x
* Tkinter (usually included with standard Python installs)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/QuellaMC/PuzzleSolver.git
   cd PuzzleSolver
   ```
2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # on Windows use `venv\Scripts\activate`
   ```

## Usage

```bash
python solver.py
```

1. Enter a month (1–12) and a day (1–31) in the GUI fields.
2. Click **Solve**.
3. View the solution on the canvas: holes in black, pieces in color.

## File Structure

* `solver.py` – Main application script.
* `README.md` – This file.

## License

This project is released under the MIT License. Feel free to use and modify!
