#!/usr/bin/env python3
"""k2animated.py – **full‑math Kryptos K2 crib alignment demo**

Slides a 13‑letter crib ("ALLYINVISIBLE") across the Kryptos K2 cipher
and shows, for *every* offset 1→10, the complete Vigenère arithmetic in
an 8‑row Tkinter grid:

    • Row 0  Cipher letter 𝐶
    • Row 1  Index of 𝐶 in the ‘KRYPTOS’ keyed alphabet (00‑25)
    • Row 2  Crib letter 𝑃
    • Row 3  Index of 𝑃
    • Row 4  Δ = (C‑P) mod 26
    • Row 5  Key index (same as Δ)
    • Row 6  Derived key letter (green if it matches pattern, red if not)
    • Row 7  Expected key pattern “ABSCISSA…”

Numbers are now **two‑digit strings** ("14", "07", …) so nothing is
missing.  Colours update live as the offset advances at ~3 fps.

Standard‑library only – no external deps.
"""
from tkinter import Tk, Frame, Label, Button, StringVar
from itertools import cycle
from textwrap import dedent

CIPHERTEXT = dedent("""
VFPJUDEEHZWETZYVGWHKKQETGFQJNCEGGWHKK?DQMCPFQZDQMMIAGPFXHQRLG
TIMVMZJANQLVKQEDAGDVFRPJUNGEUNAQZGZLECGYUXUEENJTBJLBQCRTBJDFHRR
YIZETKZEMVDUFKSJHKFWHKUWQLSZFTIHHDDDUVH?DWKBFUFPWNTDFIYCUQZERE
EVLDKFEZMOQQJLTTUGSYQPFEUNLAVIDXFLGGTEZ?FKZBSFDQVGOGIPUFXHHDRKF
FHQNTGPUAECNUVPDJMQCLQUMUNEDFQELZZVRRGKFFVOEEXBDMVPNFQXEZLGREDN
QFMPNZGLFLPMRJQYALMGNUVPDXVKPDQUMEBEDMHDAFMJGZNUPLGEWJLLAETG""").replace("\n", "")

CRIB = "ALLYINVISIBLE"
KEY_PATTERN = "ABSCISSA"  # repeats

# ‘KRYPTOS’ keyed alphabet (duplicates removed, then rest of A‑Z)
KEYWORD = "KRYPTOS"
KEYED_ALPHA = "".join(dict.fromkeys(KEYWORD + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
ALPHA_IDX = {ch: i for i, ch in enumerate(KEYED_ALPHA)}

FPS = 3.0      # frames per second
MAX_OFFSET = 10  # show offsets 0‑9 inclusive (=1‑10 for humans)

# ────────────────────────── GUI ──────────────────────────
class Visualizer:
    def __init__(self, root: Tk):
        self.root = root
        self.offset = 0
        self.running = False

        self.vars = [[StringVar() for _ in CRIB] for _ in range(8)]  # 8 rows x len(crib)

        grid = Frame(root, padx=10, pady=10)
        grid.pack()

        for r, row_vars in enumerate(self.vars):
            for c, var in enumerate(row_vars):
                lbl = Label(grid, textvariable=var, font=("Consolas", 14, "bold" if r in (0,2,6,7) else "normal"))
                lbl.grid(row=r, column=c, padx=2, pady=1)
                # save label widget reference for colouring derived key row (r==6)
                if r == 6:
                    row_vars[c] = (var, lbl)  # store tuple

        # buttons
        btn_frame = Frame(root)
        btn_frame.pack(pady=5)
        Button(btn_frame, text="Start", command=self.start).pack(side="left", padx=5)
        Button(btn_frame, text="Pause", command=self.pause).pack(side="left", padx=5)
        Button(btn_frame, text="Reset", command=self.reset).pack(side="left", padx=5)

        # initial draw
        self.draw()

    # ───────── animation control ─────────
    def start(self):
        if not self.running:
            self.running = True
            self.tick()

    def pause(self):
        self.running = False

    def reset(self):
        self.pause()
        self.offset = 0
        self.draw()

    def tick(self):
        if not self.running:
            return
        self.offset = (self.offset + 1) % MAX_OFFSET
        self.draw()
        self.root.after(int(10000/FPS), self.tick)

    # ───────── core draw routine ─────────
    def draw(self):
        off = self.offset
        expected_cycle = cycle(KEY_PATTERN)

        for i, crib_ch in enumerate(CRIB):
            ct_ch = CIPHERTEXT[off + i]
            ct_idx = ALPHA_IDX[ct_ch]
            pt_idx = ALPHA_IDX[crib_ch]
            delta  = (ct_idx - pt_idx) % 26
            k_idx  = delta
            k_ch   = KEYED_ALPHA[k_idx]
            exp_ch = next(expected_cycle)

            # row 0 – cipher letter
            self.vars[0][i].set(ct_ch)
            # row 1 – cipher index (two digits)
            self.vars[1][i].set(f"{ct_idx:02}")
            # row 2 – crib letter
            self.vars[2][i].set(crib_ch)
            # row 3 – crib index
            self.vars[3][i].set(f"{pt_idx:02}")
            # row 4 – delta
            self.vars[4][i].set(f"{delta:02}")
            # row 5 – key index (same as delta)
            self.vars[5][i].set(f"{k_idx:02}")
            # row 6 – derived key letter (colour highlight)
            var, lbl = self.vars[6][i]
            var.set(k_ch)
            lbl.config(fg="green" if k_ch == exp_ch else "red")
            # row 7 – expected pattern letter
            self.vars[7][i].set(exp_ch)

# ────────────────────────── run ──────────────────────────
if __name__ == "__main__":
    root = Tk()
    root.title("Kryptos K2 Crib Visualiser – full math mode")
    Visualizer(root)
    root.mainloop()
