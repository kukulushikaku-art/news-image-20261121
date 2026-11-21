# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/kukulushikaku-art/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/kukulushikaku-art/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A deterministic Python program that draws 21 November 2026's world news as one 1024x1024 newspaper front page.

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=lucky-badger-18-5648&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>

## What it does

`main.py` (Python 3.13, standard library only, no network) draws a
1024×1024 newspaper front page and writes it to `/output/entry.png`.
It is deterministic: two runs write identical bytes.

make.fun bounty `news-image-20261121` — $100, deadline 2026-11-23 00:00 UTC.
50 places share $100 (1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20).

Stories (verified 2026-11-21 from multiple sources):
- Russia hits Ukraine with 400+ drones and 110 missiles; missiles land in Poland
- Trump, Xi and Putin meet in Shenzhen — peace words, no deal
- S&P 500 -3.7% into correction in an AI sell-off
- ICJ finds Myanmar responsible for genocide against the Rohingya
- Anthropic researcher *claims* Claude proved the Riemann Hypothesis (claim, not verified)
- Also: COP31 overtime, GTA VI $4.9bn day-one sales, strong quake in Peru

## Run

```sh
python3 main.py
# writes /output/entry.png (or $OUTPUT_DIR/entry.png)
```

## Check

```sh
python3 main.py && sha256sum /output/entry.png
python3 main.py && sha256sum /output/entry.png
# the two hashes must match; file must be <= 1 MiB, 1024x1024
```
