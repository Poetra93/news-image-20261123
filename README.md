# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Poetra93/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Poetra93/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper front page summing up the world news of **Monday 23 November 2026** in a single 1024×1024 image — built for make.fun's "Sum up 23 November's world news in one image" bounty ($100 in USDC).

The image leads with Ukraine saying it sank the Russian corvette Merkury off Libya, then covers the collapse of COP31 in Antalya, the EU's proposed 22nd Russia sanctions package, NATO's answer to the missiles that fell in Poland, Iran's vow to counter the US blockade of Hormuz, and the Russian strikes that killed at least 15 people around Kyiv — plus 21 more stories from the day in brief, across every region and beat: war and diplomacy, climate, markets, science, health, justice and sport. All 27 stories happened or were first reported on 23 November 2026, checked against dated reporting (Reuters, France 24, RFE/RL, CNBC, the NHS and others). Nothing is invented; claims still being checked are worded as claims.

## How to run it

```sh
python3 compose.py            # redraws front-page.png (build-time only)
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` is Python 3.13, standard library only. It validates `front-page.png` (PNG signature, 1024×1024, ≤ 1 MiB, every chunk CRC) and copies it byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png`. It needs no network.

## The day, in brief

- **Lead — Libya:** Zelenskyy confirms Ukraine's naval drones sank the Russian corvette Merkury at Benghazi and hit the cargo ship MV Angara; satellite images show the capsized hull.
- **Climate:** COP31 in Antalya ends with no deal after a record two days in overtime; the EU and 130+ countries reject a text with no fossil-fuel phase-out.
- **Europe:** the EU Commission proposes its 22nd Russia sanctions package — about 60 banks off SWIFT, a crypto crackdown, 70 more shadow-fleet ships.
- **NATO:** after three Russian missiles fell in south-east Poland, the alliance meets in Brussels and sends an AWACS early-warning aircraft; Poland does not invoke Article 4.
- **The Gulf:** Iran vows to use every means against a US naval blockade of the Strait of Hormuz; Iran also says it hit US bases in Bahrain.
- **Ukraine:** Russian strikes kill at least 15 around Kyiv, 11 of them in Dymer; Ukraine hits refineries deep in Russia, in Perm and Rostov.
- **Asia and the world:** an Indonesian factory fire toll of 24 dead is confirmed; drones damage a UN building in Khartoum; the NHS starts the world's largest AI breast-screening trial; the Riemann proof author says the 250,000-page claim was a joke.

## Stories and sources

- Ukraine sinks Russian corvette Merkury at Benghazi — confirmed by Zelenskyy, 23 Nov (France 24 liveblog; RFE/RL, 23 Nov 2026).
- COP31 ends without a deal — reported 23 Nov (CNBC Africa, 23 Nov 2026; Reuters Breakingviews, 23 Nov 2026).
- EU proposes 22nd Russia sanctions package — von der Leyen in Strasbourg, 23 Nov (European Commission via EuropeSays, 23 Nov 2026).
- NATO meets and sends AWACS to Poland — 23 Nov (Live From Europe, 23 Nov 2026; Magna Bureau, 23 Nov 2026).
- Iran vows to counter US Hormuz blockade — 23 Nov (Daily Summary of World, 23 Nov 2026).
- Russian strikes kill at least 15 around Kyiv; Dymer toll 11 — 23 Nov (Principia, 23 Nov 2026; Just Security Early Edition, 23 Nov 2026).
- Indonesia confirms 24 killed in Cikande factory fire, about 30 missing — Reuters, 23 Nov 2026.
- Drones hit Khartoum, damage UN building, four killed — UN OCHA statement, 23 Nov 2026.
- Eisenkot calls West Bank settler arson "Jewish terrorism" — Reuters via Just Security, 23 Nov 2026.
- Singer Parastoo Ahmadi flogged in Qom — lawyers, first reported 23 Nov (Daily Summary of World).
- Finland summons Russian ambassador; Russia warns Estonia — 23 Nov (Daily Summary of World).
- Asian tech shares fall as AI sell-off deepens; euro inflation 4.0% — 23 Nov (Principia).
- US lead over China in Asia narrows to record low — Lowy Institute Asia Power Index, 23 Nov (10 Things Global News).
- Riemann proof: 250,000-page figure was a joke — Alpöge on X, 23 Nov 2026 (Wikipedia, citing the 23 Nov post).
- NHS launches EDITH, the world's largest AI breast-screening trial — NHS England, 23 Nov 2026.
- Bangladesh will arrest and jail Hasina if she returns — Reuters via Just Security, 23 Nov 2026.
- India offers €1.4bn to Nepal for flood rebuilding — 23 Nov (Daily Summary of World).
- Oklahoma beats Ole Miss 24-17 — 23 Nov (Daily Fox News).
- Hungary's PM Magyar plans Transcarpathia visit — 23 Nov (Daily Summary of World).
- Nigeria's Tinubu: presidential villa hit by water and power cuts — 23 Nov (Daily Summary of World).
- Gaza: UNRWA worker killed in Jabalia; Oxfam finds 99% of Gaza contaminated — 23 Nov (War Briefing, 23 Nov 2026; Medium global brief).
- Houthis say Saudi strike on Hodeidah killed 17 (unverified claim) — Houthi telecom ministry via AFP, 23 Nov.
- 49ers beat Vikings 35-10 in Mexico City; Cowboys beat Tennessee 51-30 — NFL Week 11, 23 Nov (ProCappers).
- Brentford beat Everton 4-0; Michigan stun UCLA in triple overtime — 23 Nov (SportsCafe; ProCappers).
- Amtrak train derails in Louisiana after hitting a tractor-trailer — 23 Nov (Daily Summary of World).
- US presses Nvidia over China chip sales — 23 Nov (10 Things Global News).
- JinkoSolar claims perovskite-silicon cell at 35.24% efficiency — 23 Nov (Beyond2C Climate Pulse).

## Files

- `front-page.png` — the entry image (1024×1024, PNG)
- `compose.py` — draws `front-page.png` with Pillow (build-time only)
- `main.py` — the entrypoint: validates and copies the image to the output directory
- `LICENSE` — MIT

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=darmo-susanto&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
