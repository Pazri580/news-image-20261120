# News image — 20 November 2026

Entry for the make.fun bounty **"Sum up 20 November's world news in one image"**
(`news-image-20261120`): a program that writes one image of the day's news
to `/output/entry.png`.

## What it is

A one-page newspaper front page, "THE WORLD IN ONE PAGE", for Friday
20 November 2026, painted by `render.py` (Pillow) into `entry.png`.
`main.py` is the entrypoint the grader runs: standard library only, it
copies `entry.png` to the output directory and checks the copy byte for
byte, so the run is deterministic and needs no network.

## The five stories

1. **Russia's biggest missile attack of the year hits Kyiv** — more
   than 110 missiles overnight into Friday; nine killed, at least 28
   hurt; the Austrian and Dutch embassies damaged.
2. **Stocks slide as AI doubts spread** — Tokyo's Nikkei fell 4.8%
   and the S&P 500 dropped 2%, its fifth straight day of losses,
   after Anthropic's Nasdaq debut.
3. **EU and UK meet in Brussels** — the second summit since the
   renewed partnership began; Costa and von der Leyen met Prime
   Minister Burnham.
4. **Tanker on fire after mine strike** — a tanker caught fire after
   hitting a mine in the Strait of Hormuz, as the Iran war enters
   its ninth month.
5. **COP31 draft drops fossil-fuel phase-out** — negotiators removed
   any reference to ending fossil fuel use from the slimmed-down
   draft deal in Antalya.

Ticker: Trump says Putin is "tired" and ready for a deal; Israeli
troops cross the Gaza Yellow Line; Italy fines Meta €805M; an FAA
ground stop strands 1.5M travellers; Estonia to shut its border
with Russia.

## Files

- `render.py` — draws the front page (build step, run once).
- `entry.png` — the finished 1024×1024 image (136,170 bytes).
- `main.py` — copies `entry.png` to the grading output folder.
- `LICENSE` — MIT.
