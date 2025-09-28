import tkinter as tk

# --- Cấu hình bàn cờ ---
N = 8
CELL = 64
PAD = 16
sang = "#f5deb3"
toi = "#8b5a2b"
trang = "#111"
den = "#fff"

vi_tri_xe = [0, 1, 2, 4, 3, 5, 7, 6]

def goal_test(state, goal):
    return state == tuple(goal)

def actions(state, row):
    N = len(state)
    used_cols = {c for c in state[:row] if c != -1}
    return [c for c in range(N) if c not in used_cols]

def result(state, row, col):
    new_state = list(state)
    new_state[row] = col
    return tuple(new_state)

trace = []

def AND_OR_Graph_Search(initial_state, goal):
    trace.clear()
    return OR_Search(tuple(initial_state), goal, [])

def OR_Search(state, goal, path):
    if goal_test(state, goal):
        return []
    if state in path:
        return None

    if -1 not in state:
        return None

    row = state.index(-1)
    for a in actions(state, row):
        s2 = result(state, row, a)

        trace.append(s2)

        plan = AND_Search([s2], goal, path + [state])
        if plan is not None:
            return [(row, a)] + plan
    return None

def AND_Search(states, goal, path):
    plans = []
    for s in states:
        plan = OR_Search(s, goal, path)
        if plan is None:
            return None
        plans.extend(plan)
    return plans

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
    cv = tk.Canvas(f, highlightthickness=0, bg="white")
    cv.pack()
    veBanCo(cv)
    veXe(cv, xe)
    return f, cv


def main():
    root = tk.Tk()
    root.title("8 quân xe - AND-OR Search")
    root.configure(bg="#faefdb")

    wrap = tk.Frame(root, bg="#faefdb")
    wrap.pack(padx=20, pady=20)

    left, cv_left = taoFrame(wrap, "Bàn cờ (quá trình tìm kiếm)")
    right, cv_right = taoFrame(wrap, "Bàn cờ mục tiêu", xe=vi_tri_xe)

    left.grid(row=0, column=0, padx=12, pady=12, sticky="n")
    right.grid(row=0, column=1, padx=12, pady=12, sticky="n")

    initial = [-1] * N
    plan = AND_OR_Graph_Search(initial, vi_tri_xe)

    def hien_buoc(i=0):
        if i < len(trace):
            veBanCo(cv_left)
            veXe(cv_left, trace[i])
            root.after(600, lambda: hien_buoc(i+1))
        else:
            pass

    hien_buoc()

    root.mainloop()

if __name__ == "__main__":
    main()
