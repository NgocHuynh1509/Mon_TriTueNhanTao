import tkinter as tk
import random

N = 8
CELL = 64
PAD = 16
sang = "#f5deb3"
toi = "#8b5a2b"
trang = "#111"
den = "#fff"

def forward_checking_steps(n=N):
    # Domain ban đầu: mỗi biến có tất cả các ô
    domains = {i: [(r, c) for r in range(n) for c in range(n)] for i in range(n)}
    assignment = {}

    def forward(i, domains, assignment):
        if i == n:
            yield ("done", assignment.copy())
            return

        values = domains[i][:]
        random.shuffle(values)

        for (row, col) in values:
            assignment[i] = (row, col)
            # yield bước đặt
            yield ("place", i, (row, col), assignment.copy())
            # Cập nhật domain
            new_domains = {j: list(domains[j]) for j in range(n)}
            ok = True
            for j in range(i + 1, n):
                new_domains[j] = [(r, c) for (r, c) in new_domains[j] if r != row and c != col]
                if not new_domains[j]:
                    ok = False
                    break
            if ok:
                yield from forward(i + 1, new_domains, assignment)
            # backtrack
            assignment.pop(i, None)
            yield ("remove", i, (row, col), assignment.copy())

    yield from forward(0, domains, assignment)


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
            cx = PAD + c * CELL + CELL // 2
            cy = PAD + r * CELL + CELL // 2
            o_toi = (r + c) % 2 == 1
            color = den if o_toi else trang
            canvas.create_text(cx, cy, text="♖", fill=color, font=("Segoe UI Symbol", int(CELL * 0.75), "bold"))

def main():
    root = tk.Tk()
    root.title("8 quân xe - Forward Checking")
    root.configure(bg="#faefdb")

    label = tk.Label(root, text="Nhấn Start để bắt đầu đặt quân xe",
                     font=("Segoe UI", 12), bg="#faefdb")
    label.pack(pady=10)

    canvas = tk.Canvas(root, highlightthickness=0, bg="white")
    canvas.pack(padx=20, pady=20)
    veBanCo(canvas)

    steps_gen = None  # giữ generator các bước

    def next_step():
        nonlocal steps_gen
        try:
            step = next(steps_gen)
            action = step[0]

            if action == "place":
                _, i, (r, c), assignment = step
                label.config(text=f"Đặt quân xe x{i+1} tại ({r}, {c})")
                veBanCo(canvas)
                veXe(canvas, assignment.values())

            elif action == "remove":
                _, i, (r, c), assignment = step
                label.config(text=f"Backtrack bỏ quân xe x{i+1} khỏi ({r}, {c})")
                veBanCo(canvas)
                veXe(canvas, assignment.values())

            elif action == "done":
                _, assignment = step
                label.config(text="Hoàn thành đặt đủ 8 quân xe!")
                veBanCo(canvas)
                veXe(canvas, assignment.values())
                return  # dừng lại, không lên lịch bước tiếp theo

            root.after(500, next_step)

        except StopIteration:
            pass

    def start():
        nonlocal steps_gen
        steps_gen = forward_checking_steps()
        next_step()

    btn = tk.Button(root, text="Start", command=start)
    btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
