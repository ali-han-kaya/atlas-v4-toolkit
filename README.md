# Atlas Akademik v5.5

Cok-ajanli akademik makale yazim pipeline. Sinirbilim, felsefe, teoloji, bilissel bilim alanlari icin optimize edilmistir.

## Kurulum

**Tüm paketi** hedef proje köküne kopyala (yalnızca `.opencode` + `opencode.json`
YETERLİ DEĞİLDİR — komutlar `scripts/`'i çağırır, config `AGENTS.md`'yi yükler):

```bash
cp -r .opencode opencode.json AGENTS.md scripts templates docs proje/
chmod +x proje/scripts/*.sh proje/scripts/*.py
cd proje/
opencode   # veya: opencode .
```

Doğrulama (kopya sonrası hepsi mevcut olmalı):
```bash
test -f AGENTS.md && test -d scripts && test -d templates && echo "OK: kurulum tam"
```

## Pipeline Akisi

```
FAZ0 (Scoper) → FAZ1 (3 Lens Paralel) → FAZ2 (Fixer) → FAZ3 (Writer) → FAZ4 (Gate 2-of-2)
```

**Girdi:** Atlas bir denetim + sertlestirme aracidir. FAZ1 lens'leri MASTER'i denetler;
bu nedenle pipeline'a girmeden once bir **taslak MASTER** (elindeki A/B kaynak
paketlerinden) saglanir. FAZ3 (Writer) duzeltmeleri isleyip MASTER'i finalize eder.
Detay: `docs/PIPELINE.md`, `docs/HANDOFF-CONTEXT.md`.

Her FAZ sonrasi kullanici onayi zorunludur. `/atlas-full` komutunu KULLANMA.

## Dogrulama

```bash
bash scripts/check_integrity.sh --full
python3 scripts/verify_doi.py --require-master
python3 scripts/provenance_check.py
python3 scripts/budget_guard.py --report
```
`/atlas-verify` komutu bu dorttunu calistirip `05-VERIFICATION-REPORT-v5.5.md`
uretir.

## CHK-01..07

| CHK | Aciklama | Severity |
|-----|---------|----------|
| CHK-01 | Tüm ZORUNLU SCOPE-ID (≥22) MASTER'da | P1 |
| CHK-02 | PROVENANCE coverage | P1 |
| CHK-03 | [DOGRULANMADI] etiketi yok | P0 |
| CHK-04 | Etik + DEC-036 + DPIA | P1 |
| CHK-05 | Baslik benzersiz | P2 |
| CHK-06 | Chi-square tutarlilik | P0 |
| CHK-07 | SC-006 kasitli istisna | PASS |
