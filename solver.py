import tkinter as tk
from tkinter import messagebox
import sys
from collections import defaultdict

# Increase recursion limit for deep backtracking
sys.setrecursionlimit(10000)

# --- 1. Build the board shape as a set of (x,y) coords ---
def build_board():
    board = set()
    # Months area: rows 1-2, cols 1-6
    for y in (1, 2):
        for x in range(1, 7):
            board.add((x, y))
    # Days area: rows 3-6, cols 1-7
    for y in range(3, 7):
        for x in range(1, 8):
            board.add((x, y))
    # row 7, cols 1-3
    for x in range(1, 4):
        board.add((x, 7))
    return board

# --- 2. Map month/day to the two holes ---
def month_coord(month):
    if not 1 <= month <= 12:
        raise ValueError("Month must be 1–12")
    idx = month - 1
    y = 1 if idx < 6 else 2
    x = (idx % 6) + 1
    return (x, y)

def day_coord(day):
    if not 1 <= day <= 31:
        raise ValueError("Day must be 1–31")
    idx = day - 1
    y = 3 + (idx // 7)
    x = 1 + (idx % 7)
    return (x, y)

# --- 3. Define the eight pieces ---
raw_pieces = {
    1: [(1,1), (2,1), (3,1), (1,2), (3,2)],
    2: [(1,1), (2,1), (3,1), (3,2), (4,2)],
    3: [(1,1), (2,1), (3,1), (1,2), (2,2), (3,2)],
    4: [(1,1), (2,1), (3,1), (4,1), (2,2)],
    5: [(1,1), (2,1), (3,1), (1,2), (1,3)],
    6: [(1,1), (2,1), (2,2), (2,3), (3,3)],
    7: [(1,1), (2,1), (3,1), (4,1), (1,2)],
    8: [(1,1), (2,1), (1,2), (2,2), (3,1)],
}

def generate_orientations(coords):
    result = set()
    pts = coords
    for flip in (False, True):
        flipped = [(-x, y) if flip else (x, y) for x, y in pts]
        for rot in range(4):
            if rot == 0:
                rot_pts = flipped
            elif rot == 1:
                rot_pts = [(-y, x) for x, y in flipped]
            elif rot == 2:
                rot_pts = [(-x, -y) for x, y in flipped]
            else:
                rot_pts = [(y, -x) for x, y in flipped]
            minx = min(x for x, y in rot_pts)
            miny = min(y for x, y in rot_pts)
            norm = frozenset((x - minx, y - miny) for x, y in rot_pts)
            result.add(norm)
    return result

# Precompute all piece orientations
piece_orients = {pid: list(generate_orientations(shape)) for pid, shape in raw_pieces.items()}

# --- 4. Precompute valid placements ---
def all_placements(board, hole1, hole2):
    max_x = max(x for x, y in board)
    max_y = max(y for x, y in board)
    placements = defaultdict(list)
    board_noholes = board - {hole1, hole2}

    for pid, orients in piece_orients.items():
        for shape in orients:
            width = max(x for x, y in shape) + 1
            height = max(y for x, y in shape) + 1
            for ox in range(1, max_x - width + 2):
                for oy in range(1, max_y - height + 2):
                    placed = {(ox + x, oy + y) for x, y in shape}
                    if placed & {hole1, hole2}:
                        continue
                    if placed <= board_noholes:
                        placements[pid].append(frozenset(placed))
    return placements, board_noholes

# --- 5. Solve via backtracking ---
def solve(placements, board_noholes):
    piece_order = sorted(placements.keys(), key=lambda pid: len(placements[pid]))
    used = set()
    solution = {}

    def backtrack(idx):
        if idx >= len(piece_order):
            return used == board_noholes
        pid = piece_order[idx]
        for shape in placements[pid]:
            if shape & used:
                continue
            prev_used = set(used)
            used.update(shape)
            solution[pid] = shape
            if backtrack(idx+1):
                return True
            used.clear()
            used.update(prev_used)
            del solution[pid]
        return False

    return solution if backtrack(0) else None

# --- Display constants ---
CELL_SIZE = 40
MARGIN = 20
COLORS = {1:'#d32f2f', 2:'#e57373', 3:'#1976d2', 4:'#64b5f6', 5:'#388e3c', 6:'#81c784', 7:'#fbc02d', 8:'#ffeb3b'}

# --- 6. GUI Application ---
class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        master.title("Month-Day Puzzle")
        frame = tk.Frame(master)
        frame.pack(pady=10)
        tk.Label(frame, text="Month (1-12):").grid(row=0, column=0)
        self.month_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.month_var, width=5).grid(row=0, column=1)
        tk.Label(frame, text="Day (1-31):").grid(row=0, column=2)
        self.day_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.day_var, width=5).grid(row=0, column=3)
        tk.Button(frame, text="Solve", command=self.on_solve).grid(row=0, column=4, padx=5)

        self.board = build_board()
        max_x = max(x for x,y in self.board)
        max_y = max(y for x,y in self.board)
        width = MARGIN*2 + CELL_SIZE*max_x
        height = MARGIN*2 + CELL_SIZE*max_y
        self.canvas = tk.Canvas(master, width=width, height=height, bg='white')
        self.canvas.pack()

    def on_solve(self):
        try:
            m = int(self.month_var.get())
            d = int(self.day_var.get())
            holeM = month_coord(m)
            holeD = day_coord(d)
        except Exception as e:
            messagebox.showerror("Input Error", str(e))
            return
        placements, board_noholes = all_placements(self.board, holeM, holeD)
        sol = solve(placements, board_noholes)
        if sol is None:
            messagebox.showinfo("No Solution", f"No solution for {m}/{d}")
            return
        self.draw_solution(sol, holeM, holeD)

    def draw_solution(self, sol, holeM, holeD):
        self.canvas.delete("all")
        # Draw grid and holes
        for x,y in self.board:
            x1 = MARGIN + (x-1)*CELL_SIZE
            y1 = MARGIN + (y-1)*CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            if (x,y) in (holeM, holeD):
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='black')
            else:
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='gray')
        # Draw pieces with labels
        for pid, cells in sol.items():
            color = COLORS.get(pid, 'gray')
            for x,y in cells:
                x1 = MARGIN + (x-1)*CELL_SIZE + 2
                y1 = MARGIN + (y-1)*CELL_SIZE + 2
                x2 = x1 + CELL_SIZE - 4
                y2 = y1 + CELL_SIZE - 4
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                # Label each cell with piece ID
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                self.canvas.create_text(cx, cy, text=str(pid), fill='white', font=('Helvetica', 12, 'bold'))

if __name__ == '__main__':
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
