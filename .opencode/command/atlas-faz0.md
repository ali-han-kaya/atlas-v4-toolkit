---
name: atlas-faz0
description: Atlas v5.5 FAZ0 — Kapsam Sozlesmesi
agent: atlas-scoper
---
# /atlas-faz0

1. Kullaniciya sor: "Ne yazacaksin? 7 alan nasil baglaniyor?" (1-2 cümle RQ)
2. `atlas-scoper` ajanini calistir (Claude Sonnet 4)
3. Cikti: `00-FAZ-0-SCOPE-CONTRACT-ve-REGISTER.md`
4. `bash scripts/check_integrity.sh --faz0`
5. `python3 scripts/provenance_check.py`
6. Kullaniciya goster, onay bekle.
