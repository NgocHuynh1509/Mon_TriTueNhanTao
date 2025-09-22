import tkinter as tk
import random

N = 8
CELL = 64  # pixel
PAD = 16   # pixel
sang = "#f5deb3"
toi = "#8b5a2b"
trang = "#111"
den = "#fff"

vi_tri_xe = [0, 1, 2, 3, 4, 7, 6, 5]

def heuristic(vt, goal):
    return sum(abs(c - gc) for (_, c), (_, gc) in zip(vt, goal))

def random_start():
    return [(r, random.randint(0, 7)) for r in range(8)]


def hill_climbing(start, goal):
    current = start
    steps = [(current[:], heuristic(current, goal))]
    h_curr = heuristic(current, goal)

    improved = True
    while improved:
        improved = False
        neighbors = []

        # thử di chuyển từng quân trong hàng sang cột khác
        for r in range(8):
            c_now = current[r][1]
            for c in range(8):
                if c != c_now:
                    new_state = current[:]
                    new_state[r] = (r, c)
                    h_new = heuristic(new_state, goal)
                    neighbors.append((h_new, new_state))

        if not neighbors:
            break

        best_h, best_state = min(neighbors, key=lambda x: x[0])

        if best_h < h_curr:
            current, h_curr = best_state, best_h
            steps.append((current[:], h_curr))
            improved = True

        if current == goal:
            print("Đạt mục tiêu!")
            break

    return steps


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
    veBanCo(canvas)
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
    root.title("8 xe - Hill Climbing (dừng & tiếp tục)")
    root.configure(bg="#faefdb")

    wrap = tk.Frame(root, bg="#faefdb")
    wrap.pack(padx=20, pady=20)

    left, cv_left = taoFrame(wrap, "Bàn cờ Hill Climbing")
    right, cv_right = taoFrame(wrap, "Bàn cờ mục tiêu", xe=vi_tri_xe)

    left.grid(row=0, column=0, padx=12, pady=12, sticky="n")
    right.grid(row=0, column=1, padx=12, pady=12, sticky="n")

    veXe(cv_right, vi_tri_xe)

    info_label = tk.Label(root, text="", font=("Segoe UI", 12), bg="#faefdb", fg="#333")
    info_label.pack(pady=10)

    SPEED_MS = 1000

    # === Chuẩn bị start/goal và chạy hill_climbing để lấy danh sách bước ===
    start = random_start()  # list[(r,c)]
    goal = [(r, vi_tri_xe[r]) for r in range(N)]  # list[(r,c)] tương ứng bảng mục tiêu
    steps = hill_climbing(start, goal)  # list[(state(list[(r,c)]), h)]

    # Hàm phụ đổi state dạng [(r,c)] -> list[c] để vẽ
    def to_cols(state_rc):
        cols = [0] * N
        for r, c in state_rc:
            cols[r] = c
        return cols

    # Vẽ trạng thái đầu tiên nếu có
    if steps:
        veXe(cv_left, to_cols(steps[0][0]))
        info_label.config(text=f"Bắt đầu: h={steps[0][1]}")

    idx = 0  # chỉ số bước

    def step():
        nonlocal idx
        if idx >= len(steps):
            return
        state_rc, h = steps[idx]
        veXe(cv_left, to_cols(state_rc))
        info_label.config(text=f"Bước {idx}/{len(steps)-1} – h={h}")
        idx += 1
        if idx < len(steps):
            root.after(SPEED_MS, step)
        else:
            info_label.config(text=f"Hoàn thành – h={h}")

    root.after(SPEED_MS, step)
    root.mainloop()



if __name__ == "__main__":
    main()
