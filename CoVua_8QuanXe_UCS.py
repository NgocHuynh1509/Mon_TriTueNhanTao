import tkinter as tk
from collections import deque
import heapq


N = 8
CELL = 64  # pixel
PAD = 16   # pixel
sang = "#f5deb3"
toi = "#8b5a2b"
trang = "#111"
den = "#fff"

vi_tri_xe = [0, 1, 2, 3, 4, 7, 6, 5]

def bfs(n=8):
    start = tuple()
    queue = deque([start])
    while queue:
        state = queue.popleft()
        row = len(state)
        if row == n:
            yield ("done", state)
            continue
        used = set(state)
        for col in range(n):
            if col not in used:
                child = state + (col,)
                queue.append(child)

def ucs(n=8):
    start = tuple()
    frontier = [(0, start)]
    while frontier:
        cost, state = heapq.heappop(frontier)
        row = len(state)
        if row == n:
            yield ("done", state, cost)
            continue
        used = set(state)
        prev_state = {r: state[r] for r in range(len(state))}
        for i in range(n):
            if i not in used:
                new_blocked = 0
                for k, v in prev_state.items():
                    if v == i or k == row: 
                        new_blocked += n - 1
                step_cost = new_blocked
                heapq.heappush(frontier, (cost + step_cost, state + (i,)))

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
    f = tk.Frame(parent)
    lb = tk.Label(f, text=text, font=("Segoe UI", 12, "bold"))
    lb.pack(pady=(0, 6))
    cv = tk.Canvas(f, highlightthickness=0, bg="white")
    cv.pack()
    veBanCo(cv)
    veXe(cv, xe)
    return f, cv

def main():
    root = tk.Tk()
    root.title("8 xe ")
    root.configure(bg="#faefdb")

    wrap = tk.Frame(root, bg="#faefdb")
    wrap.pack(padx=20, pady=20)
    
    left, cv_left = taoFrame(wrap, "Bàn cờ trống")
    right, cv_right = taoFrame(wrap, "Bàn cờ mục tiêu", xe=vi_tri_xe)

    left.grid(row=0, column=0, padx=12, pady=12, sticky="n")
    right.grid(row=0, column=1, padx=12, pady=12, sticky="n")

    
    veBanCo(cv_right)
    veXe(cv_right, vi_tri_xe)

    root.mainloop()

if __name__ == "__main__":
    main()
