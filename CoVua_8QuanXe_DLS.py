import tkinter as tk

N = 8
CELL = 64
PAD = 16
sang = "#f5deb3"
toi = "#8b5a2b"
trang = "#111"
den = "#fff"

vi_tri_xe = [0, 1, 2, 3, 6, 7, 4, 5]

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

def dls(goal, limit, on_visit=None):
    state = []
    cols = set()
    return recursive(state, cols, row=0, limit=limit, goal=goal, on_visit=on_visit)

def recursive(state, used_cols, row, limit, goal, on_visit):
    if on_visit is not None:
        on_visit(state)
    if row == N:
        if goal is None or state == goal:
            return list(state)  
        else:
            return 'failure'
    if limit == 0:
        return 'cutoff'
    cutoff_occurred = False
    for c in range(N):
        if c in used_cols:
            continue
        state.append(c)
        used_cols.add(c)
        result = recursive(state, used_cols, row + 1, limit - 1, goal, on_visit)
        if result == 'cutoff':
            cutoff_occurred = True
        elif result != 'failure':
            return result  
        state.pop()
        used_cols.remove(c)
    return 'cutoff' if cutoff_occurred else 'failure'

def main():
    root = tk.Tk()
    root.title("Cờ vua - 8 quân xe - DFS")
    root.configure(bg="#faefdb")

    wrap = tk.Frame(root, bg="#faefdb")
    wrap.pack(padx=20, pady=20)

    left_frame, cv_left = taoFrame(wrap, "Bàn cờ DFS")
    right_frame, cv_right = taoFrame(wrap, "Bàn cờ theo vi_tri_xe", xe=vi_tri_xe)

    left_frame.grid(row=0, column=0, padx=12, pady=12, sticky="n")
    right_frame.grid(row=0, column=1, padx=12, pady=12, sticky="n")

    def draw_left(state):
        veBanCo(cv_left)
        veXe(cv_left, state)
        cv_left.update_idletasks()

    def draw_right():
        veBanCo(cv_right)
        veXe(cv_right, vi_tri_xe)

    draw_right()
    result = dls(goal=vi_tri_xe, limit=8, on_visit=draw_left)
    steps = [result[:k] for k in range(len(result)+1)]
    def play(step=0):
        veBanCo(cv_left)
        veXe(cv_left, steps[step])
        if step < len(steps)-1:
            root.after(1000, play, step+1)  
    play(0)

    root.mainloop()

if __name__ == "__main__":
    main()
