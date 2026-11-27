# news-image-20261127

[![news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/iashauzora/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127?utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/iashauzora/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_campaign=news-image-20261127)

**The World in a Day — Friday 27 November 2026.** One front page,
six headlines, one 1024×1024 image. The lead story is the fuel
tanker fire near Cairo that killed 31 people, with prosecutors
arresting a man accused of sparking the blaze. Around it: Trump
urging Putin to end hostilities in Europe, Kim Jong Un ordering a
wider nuclear deployment, a UK train attacker found guilty of
attempted murder, a $622M US deal to keep Ukraine's F-16s flying,
and Gérard Depardieu set to face trial in Paris. Every headline is
backed by at least two reports dated 27 November 2026; the
citations are in `design/sources.md`, and the page itself is drawn
by `design/render.py`.

## Run it

```sh
node main.ts
```

`main.ts` validates the committed `entry.png` (size, PNG signature,
dimensions, and a full chunk-by-chunk integrity walk) and copies it
byte-for-byte to `$MAKEFUN_OUTPUT_DIR` (default `/output`).

---

Built for [make.fun](https://make.fun/?ref=sy4xfh92).
