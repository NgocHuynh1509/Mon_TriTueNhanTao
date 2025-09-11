''' Tên: Huỳnh Gia Diễm Ngọc
MSSV: 23110132'''

import tkinter as tk
from collections import deque

N = 8
CELL = 64
PAD = 16
sang = "#f5deb3"
toi = "#8b5a2b"
trang = "#111"
den = "#fff"

vi_tri_xe = [0, 1, 2, 3, 6, 7, 4, 5]

def dfs(n=8):
    start = tuple()
    stack = [start]
    yield ("visit", start)
    while stack:
        state = stack.pop()
        row = len(state)
        if row == n:
            yield ("done", state)
            continue
        used = set(state)
        for col in reversed(range(n)):
            if col not in used:
                child = state + (col,)
                stack.append(child)
                yield ("visit", child)
    yield ("fail", ())


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
    if xe is not None:
        for r in range(len(xe)):
            c = xe[r]
            cx = PAD + c * CELL + CELL // 2
            cy = PAD + r * CELL + CELL // 2
            o_toi = (r + c) % 2 == 1
            color = den if o_toi else trang
            canvas.create_text(
                cx, cy, text="♖", fill=color,
                font=("Segoe UI Symbol", int(CELL * 0.75), "bold")
            )

def taoFrame(parent, text, xe=None):
    f = tk.Frame(parent, bg="#faefdb")
    lb = tk.Label(f, text=text, font=("Segoe UI", 12, "bold"), bg="#faefdb")
    lb.pack(pady=(0, 6))
    cv = tk.Canvas(f, highlightthickness=0, bg="white")
    cv.pack()
    veBanCo(cv)
    veXe(cv, xe)
    return f, cv

def main():
    root = tk.Tk()
    root.title("Cờ vua - 8 quân xe -DFS")
    root.configure(bg="#faefdb")

    wrap = tk.Frame(root, bg="#faefdb")
    wrap.pack(padx=20, pady=20)

    left, cv_left = taoFrame(wrap, "Bàn cờ DFS")
    right, cv_right = taoFrame(wrap, "Bàn cờ theo vi_tri_xe", xe=vi_tri_xe)

    left.grid(row=0, column=0, padx=12, pady=12, sticky="n")
    right.grid(row=0, column=1, padx=12, pady=12, sticky="n")

    SPEED_MS = 25
    gen = dfs(N)

    def left(state):
        veBanCo(cv_left)
        veXe(cv_left, state)
        cv_left.update_idletasks()

    def right():
        veBanCo(cv_right)
        veXe(cv_right, vi_tri_xe)

    def step():
        try:
            kind, state = next(gen)
            left(state)
            if len(state) == N and tuple(vi_tri_xe) == state:
                return
            root.after(SPEED_MS, step)
        except StopIteration:
            pass

    root.after(SPEED_MS, step)
    root.mainloop()

if __name__ == "__main__":
    main()
