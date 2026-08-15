---
name: atlas-gate-2a
description: Atlas v5.5 Gate 2A — Kor Denetim Claude
agent: atlas-gate-2a
---
# /atlas-gate-2a

1. `atlas-gate-2a` ajanini calistir (Claude Sonnet 4)
   - Girdi: MASTER + SCOPE-CONTRACT + PROVENANCE (FIX-MANIFEST ASLA okuma)
   - Cikti: `gate/STRONG-gate-2a-v5.5.json`
2. `ls -la gate/STRONG-gate-2a-v5.5.json`
3. `python3 -c "import json; json.load(open('gate/STRONG-gate-2a-v5.5.json'))"`
4. Verdict PASS ise 2B'ye gec, FAIL ise bulgulari goster FAZ2'ye don.
