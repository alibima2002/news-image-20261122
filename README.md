# 22 November 2026 — World News in One Image

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/alibima2002/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/alibima2002/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-image summary of the world's news of **Sunday 22 November 2026**, drawn
programmatically with Python/PIL (`draw_entry.py`, DejaVu Sans) and shipped as
`entry.png` (1024×1024). The program `main.ts` (Node 22, stdlib only) copies
that image to `$MAKEFUN_OUTPUT_DIR/entry.png`, byte for byte, with a full
byte-equality self-check.

## The day, ranked by significance

1. **COP31 collapses with no deal** — after two days in overtime, the UN
   climate summit in Antalya ends with no agreement, the first such failure
   since Copenhagen in 2009.
2. **Democrats clinch 258 House seats** — a North Carolina win gives them
   their biggest House majority since 1992, a 44-seat gain.
3. **Houthis claim Saudi refinery hit** — Yemen's Houthis say they struck the
   Rabigh oil refinery; the claim is unverified and Riyadh is silent.
4. **S&P 500 slides into correction** — the index falls 11.6% from its record
   high, down seven straight sessions on AI-spending doubts.
5. **Drone flattens flats near Kyiv** — a Russian drone collapses part of a
   block in Dymer; two killed and about 14 people missing.
6. **Factory fire: 3 dead, 36 missing** — rescuers search a burned candy
   factory in Cikande, Indonesia, a day after the blaze.

Also today: South Korea's education minister quits over AI cheating chaos;
the Russian ship Sparta II is towed out of Finnish waters; Bahrain says two
people were hurt in Saturday's Iran attack.

Every story was verified against Reuters, AP and AFP reporting of
22 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Bounty

[news-image-20261122 on make.fun](https://make.fun/bounty/news-image-20261122) —
"Sum up 22 November's world news in one image" ($100).

## License

MIT — see [LICENSE](LICENSE).
