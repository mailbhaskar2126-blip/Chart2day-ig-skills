# Chart2day Instagram skills

Instagram agent skills for the Chart2day page (@chart2day), one financial or economic chart a day.

Based on [postzen-dev/instagram-agent-skill](https://github.com/postzen-dev/instagram-agent-skill) (MIT), itself a fork of Jake Schincariol's instagram-agent-skill. DM and comment skills are left out.

- `skills/`: 12 Claude skills (`ig-caption`, `ig-carousel`, `ig-plan`, `ig-publish`, and others)
- `2026-10-30-chart2day-voice.md`: draft voice profile, copy to `~/.instagram-agent/voice.md`
- Publishing goes through PostZen. Put the key in `.env` as `POSTZEN_API_KEY`; it is gitignored.
