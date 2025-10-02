import tkinter as tk
import random

N = 8
CELL = 64
PAD = 16
sang = "#f5deb3"
toi = "#8b5a2b"
trang = "#111"
den = "#fff"

# =================== BACKTRACKING SINH THEO BƯỚC ===================

def is_safe(position, row, col):
    for (r, c) in position:
        if r == row or c == col:
            return False
    return True

def backtracking_rooks_steps(n=N):
    """Generator: yield ra từng bước đặt quân xe"""
    def backtrack(i, position):
        if i == n:
            yield position[:]
            return
        cells = [(r, c) for r in range(n) for c in range(n)]
        random.shuffle(cells)
        for (row, col) in cells:
            if is_safe(position, row, col):
                position.append((row, col))
                yield ("place", i, (row, col), position[:])
                yield from backtrack(i + 1, position)
                position.pop()
                yield ("remove", i, (row, col), position[:])
    yield from backtrack(0, [])

def veBanCo(canvas):
    canvas.delete("all")
    W = PAD * 2 + N * CELL
    canvas.config(width=W, height=W)
    for r in range(N):
        for c in range(N):
            x0 = PAD + c * CELL
            y0 = PAD + r * CELL
            x1 = x0 + CELL
            y1 = y0 + CELL
            fill = sang if (r + c) % 2 == 0 else toi
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=0)

def veXe(canvas, xe=None): 
    if xe: 
        for r, c in xe: 
            cx = PAD + c * CELL + CELL//2 
            cy = PAD + r * CELL + CELL//2 
            o_toi = (r + c) % 2 == 1 
            color = den if o_toi else trang 
            canvas.create_text(cx, cy, text="♖", fill=color, font=("Segoe UI Symbol", int(CELL*0.75), "bold"))

def main():
    root = tk.Tk()
    root.title("8 quân xe - Backtracking")
    root.configure(bg="#faefdb")

    label = tk.Label(root, text="Nhấn Start để bắt đầu đặt quân xe",
                     font=("Segoe UI", 12), bg="#faefdb")
    label.pack(pady=10)

    canvas = tk.Canvas(root, highlightthickness=0, bg="white")
    canvas.pack(padx=20, pady=20)
    veBanCo(canvas)

    steps_gen = None  # sẽ giữ generator các bước

    def next_step():
        nonlocal steps_gen
        try:
            step = next(steps_gen)
            if isinstance(step, list):
                # Hoàn thành
                label.config(text="Hoàn thành đặt đủ 8 quân xe!")
                veBanCo(canvas)
                veXe(canvas, step)
                return

            action, i, (r, c), position = step
            if action == "place":
                label.config(text=f"Đặt quân xe {i+1} tại ({r}, {c})")
            elif action == "remove":
                label.config(text=f"Backtrack bỏ quân xe {i+1} khỏi ({r}, {c})")

            veBanCo(canvas)
            veXe(canvas, position)
            root.after(500, next_step)
        except StopIteration:
            pass

    def start():
        nonlocal steps_gen
        steps_gen = backtracking_rooks_steps()
        next_step()

    btn = tk.Button(root, text="Start", command=start)
    btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()