---
name: atlas-gate-2b
description: Atlas v5.5 Gate 2B — Manifest Dogrulama GPT-OSS
agent: atlas-gate-2b
---
# /atlas-gate-2b

1. `atlas-gate-2b` ajanini calistir (GPT-OSS 20B)
   - Girdi: FIX-MANIFEST + MASTER + SCOPE-CONTRACT
   - Cikti: `gate/STRONG-gate-2b-v5.5.json`
2. `ls -la gate/STRONG-gate-2b-v5.5.json`
3. `python3 -c "import json; json.load(open('gate/STRONG-gate-2b-v5.5.json'))"`
4. Voting (gate_merge.py FINAL-GATE + rapor dosyasini burada uretir):
   `python3 scripts/gate_merge.py gate/STRONG-gate-2a-v5.5.json gate/STRONG-gate-2b-v5.5.json`
5. Merge SONRASI butunluk kontrolu (rapor artik mevcut):
   `bash scripts/check_integrity.sh --gate`
