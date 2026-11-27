# news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/iashauzora/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/iashauzora/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

A one-page newspaper front page — "THE WORLD IN A DAY" — summing up Friday 27 November 2026 in six headlines, led by the fuel tanker fire near Cairo that killed 31, with Trump urging Putin to end hostilities in Europe, Kim Jong Un ordering a wider nuclear deployment, the UK train attacker found guilty of attempted murder, Washington's $622M package to keep Ukraine's F-16s flying, and Gérard Depardieu set to face trial. Every story was verified in at least two independent sources dated 27 November 2026 (see `design/sources.md`); the page itself is rendered by `design/render.py`. The repository ships the finished 1024×1024 PNG as `entry.png`, and `main.ts` validates it (PNG signature, IHDR dimensions, every chunk's CRC, size limits) and copies it to the output directory byte-for-byte.

## Run it

```sh
node main.ts
# validates entry.png and copies it to /output/entry.png
# (set MAKEFUN_OUTPUT_DIR to use a different output directory)
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=sy4xfh92&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>
