# news-image-20261119

Front page of **Thursday 19 November 2026** — the day's world news in one image.

`python3 main.py` writes `/output/entry.png` (1024×1024 PNG, ~14 KB): a newspaper
front page carrying the three stories that dominated the day —

1. **Shenzhen trilateral** — Trump, Xi and Putin hold the first-ever three-way
   summit at APEC; the US and China say they want to help end the Ukraine war,
   Zelenskyy awaits the envoys' debrief.
2. **Caracas** — the US and Venezuela sign a deal to reestablish military ties
   (Hegseth), continuing on to Colombia for anti-drug cooperation.
3. **Markets** — futures rally, Anthropic's record IPO debut, OPEC saying
   fossil fuels stay vital to electrification.

No network, no fonts, no third-party libraries: the program draws every pixel
itself with a tiny built-in 5×7 glyph set, so two runs write byte-identical
files.

MIT licensed. Entry for make.fun's news-image-20261119 bounty.
