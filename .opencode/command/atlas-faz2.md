---
name: atlas-faz2
description: Atlas v5.5 FAZ2 — Fixer
agent: atlas-orchestrator
---
# /atlas-faz2

1. `01-FAZ-1-LENS-SWARM-DENETIM.md` oku
2. Her P0/P1 bulgu icin FIX-XXX (ardisik, benzersiz) olustur
3. Kullaniciya sor: "Hangi FIX'ler uygulansin?" (evet/hayir)
4. Uygulanan her FIX icin: MASTER'da once→sonra alinti kaniti
5. `02-FAZ-2-FIXER-SWARM.md` yaz:
   | FIX-ID | CHK-Kaynak | Aciklama | Severity | Durum | Kanit |
6. `bash scripts/check_integrity.sh --faz2`
7. Kullaniciya goster, onay bekle.
