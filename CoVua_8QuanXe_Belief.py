import tkinter as tk
from collections import deque

N = 8
CELL = 64
PAD = 16
sang = "#f5deb3"
toi = "#8b5a2b"
trang = "#111"
den = "#fff"


vi_tri_xe = [
    [0, 1, 2, 3, 4, 5, 7, 6],   
    [1, 3, 5, 7, 2, 0, 6, 4],   
    [2, 4, 6, 0, 3, 1, 7, 5],  
]

def hop_le(state, r, c):
    for rr in range(r):
        if state[rr] == c:  
            return False
    return True

def next_row(state):
    for r in range(N):
        if state[r] == -1:
            return r
    return None

def actions(state):
    r = next_row(state)
    if r is None: return []
    cols = []
    for c in range(N):
        if hop_le(state, r, c):
            cols.append((r, c))
    return cols

def apply_action(state, action):
    r, c = action
    new_state = list(state)
    new_state[r] = c
    return tuple(new_state)

def belief_search(initial_belief, goals):
    frontier = deque([initial_belief])
    visited = set()
    history = []

    while frontier:
        belief = frontier.popleft()
        history.append(belief)
        if any(state in [tuple(g) for g in goals] for state in belief):
            return history
        key = tuple(sorted(belief))
        if key in visited:
            continue
        visited.add(key)

        new_belief = set()
        for state in belief:
            for act in actions(state):
                succ = apply_action(state, act)
                new_belief.add(succ)

        if new_belief:
            frontier.append(new_belief)

    return history
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
            if c == -1:
                continue
            cx = PAD + c * CELL + CELL // 2
            cy = PAD + r * CELL + CELL // 2
            o_toi = (r + c) % 2 == 1
            color = den if o_toi else trang
            canvas.create_text(
                cx, cy, text="♖", fill=color,
                font=("Segoe UI Symbol", int(CELL*0.75), "bold")
            )

def taoFrame(parent, text, xe=None):
    f = tk.Frame(parent)
    lb = tk.Label(f, text=text, font=("Segoe UI", 12, "bold"))
    lb.pack(pady=(0, 6))
    cv = tk.Canvas(f, highlightthickness=0, bg="white", width=500, height=500)
    cv.pack()
    if xe:
        veBanCo(cv)
        veXe(cv, xe)
    return f, cv

def main():
    root = tk.Tk()
    root.title("Belief-State Search - 8 Xe (tập belief)")
    root.configure(bg="#faefdb")

    wrap = tk.Frame(root, bg="#faefdb")
    wrap.pack(padx=20, pady=20)

    left, cv_left = taoFrame(wrap, "Bàn cờ Belief Search")
    right, cv_right = taoFrame(wrap, "Bàn cờ mục tiêu", xe=vi_tri_xe[0])

    left.grid(row=0, column=0, padx=12, pady=12, sticky="n")
    right.grid(row=0, column=1, padx=12, pady=12, sticky="n")

    init_state = tuple([-1] * N)
    history = belief_search({init_state}, vi_tri_xe)

    final_belief = list(history[-1])   

    def play(idx=0):
        if idx >= len(final_belief):
            return
        state = final_belief[idx]

        veBanCo(cv_left)
        veXe(cv_left, state)

        if any(list(state) == g for g in vi_tri_xe):
            print("Đã đạt một trong các goal!")
            return

        root.after(50, play, idx + 1)

    play(0)

    root.mainloop()

if __name__ == "__main__":
    main()
