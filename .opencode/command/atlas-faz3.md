---
name: atlas-faz3
description: Atlas v5.5 FAZ3 — Writer Master
agent: atlas-writer-master
---
# /atlas-faz3

1. `atlas-writer-master` ajanini calistir (Claude Sonnet 4)
   - Girdi: kullanicinin sagladigi TASLAK MASTER + A/B kaynak paketleri (ham icerik)
     + 00-FAZ-0 + 01-FAZ-1 + 02-FAZ-2
   - Cikti: `03-FAZ-3-MASTER-v5.5.md`
2. PROVENANCE tablosu dolu mu kontrol et
3. `python3 scripts/verify_doi.py --require-master`
4. `python3 scripts/provenance_check.py`
5. `bash scripts/check_integrity.sh --faz3` (≥15KB, verify_doi + provenance_check dahil)
6. Kullaniciya goster, onay bekle.
