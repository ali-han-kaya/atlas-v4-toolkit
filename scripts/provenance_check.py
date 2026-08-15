#!/usr/bin/env python3
"""Atlas v5.5.2 Provenance Check — CHK-01, CHK-02, CHK-05 (sikilastirilmis)

ZORUNLU SCOPE-ID'lerin MASTER'da GERCEK BOLUM (baslik) olarak olup olmadigini,
PROVENANCE tablosunda "kapsiyor" durumuyla yer alip almadigini ve baslik
benzersizligini kontrol eder.

Onceki surumden farklar:
- CHK-01: ID'nin metnin herhangi bir yerinde gecmesi YETMEZ; bir markdown
  basligina (# / ## / ###) dahil olmasi gerekir.
- ZORUNLU satirlari SADECE tablo-sutunu formatinda (| ... | ZORUNLU | ...)
  eslesir; "degil ZORUNLU" gibi serbest metin yanlis pozitif URETMEZ.
- CHK-02: PROVENANCE tablosu satir satir ayristirilir; her ZORUNLU ID icin
  tabloda bir satir VE durumun "kapsiyor" (veya DEC-027 kapsaminda
  [UNVERIFIED]) olmasi gerekir. Sadece "PROVENANCE" kelimesinin varligi
  YETMEZ.
"""
import re, pathlib, sys

MASTER_CANDS = [
    "03-FAZ-3-MASTER-v5.5.md",
    "03-FAZ-3-MASTER-v5.4.md",
    "03-FAZ-3-MASTER-v5.2.md",
    "MASTER.md",
]
SCOPE = pathlib.Path("00-FAZ-0-SCOPE-CONTRACT-ve-REGISTER.md")

if not SCOPE.exists():
    print("FAIL: SCOPE-CONTRACT yok")
    sys.exit(1)

master = None
for c in MASTER_CANDS:
    if pathlib.Path(c).exists():
        master = pathlib.Path(c)
        break

if not master:
    print("FAIL: MASTER yok")
    sys.exit(1)

st = SCOPE.read_text(errors="ignore")
mt = master.read_text(errors="ignore")

overall_fail = False

# --- ZORUNLU SC-ID'leri SADECE tablo-sutunu formatinda cikar ---
# Beklenen format: | SC-XXX | Baslik | ZORUNLU | Kaynak | Gerekce |
zor = []
for line in st.splitlines():
    if not line.strip().startswith("|"):
        continue
    cols = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cols) < 3:
        continue
    id_match = re.match(r"SC-\d{3}", cols[0])
    if not id_match:
        continue
    # ZORUNLU herhangi bir sutunda TAM esdeger olarak geciyor mu?
    if any(c.upper() == "ZORUNLU" for c in cols):
        zor.append(id_match.group(0))

if not zor:
    print("WARN: SCOPE-CONTRACT'ta tablo-sutunu formatinda ZORUNLU SC-ID bulunamadi (format kontrolu)")

# --- CHK-01: her ZORUNLU ID bir MARKDOWN BASLIGINDA var mi? ---
heading_lines = [l for l in mt.splitlines() if re.match(r"^#{1,6}\s", l)]
headings_text = "\n".join(heading_lines)
missing_headings = [s for s in zor if s not in headings_text]
if missing_headings:
    print(f"FAIL CHK-01: {len(zor)} zorunlu, {len(missing_headings)} basliksiz {missing_headings}")
    overall_fail = True
else:
    print(f"PASS CHK-01: {len(zor)} zorunlu SCOPE-ID MASTER'da baslik olarak var")

# --- PROVENANCE tablosunu ayristir: | SC-ID | Bolum | Kaynak | Satir | Durum | ---
prov_rows = {}
for line in mt.splitlines():
    if not line.strip().startswith("|"):
        continue
    cols = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cols) < 2:
        continue
    m = re.match(r"SC-\d{3}", cols[0])
    if not m:
        continue
    sid = m.group(0)
    durum = cols[-1] if cols else ""
    prov_rows[sid] = durum

# --- CHK-02: her ZORUNLU ID provenance tablosunda "kapsiyor" (veya DEC-027
#     kapsaminda [UNVERIFIED]) durumunda mi? ---
missing_prov = []
bad_status = []
for sid in zor:
    if sid not in prov_rows:
        missing_prov.append(sid)
        continue
    durum = prov_rows[sid].lower()
    if "kapsiyor" in durum or "kaps\u0131yor" in durum or "unverified" in durum:
        continue
    bad_status.append((sid, prov_rows[sid]))

if missing_prov or bad_status:
    print(f"FAIL CHK-02: PROVENANCE eksik {missing_prov} / gecersiz-durum {bad_status}")
    overall_fail = True
else:
    print(f"PASS CHK-02: {len(zor)} zorunlu ID PROVENANCE tablosunda 'kapsiyor' durumunda")

# --- CHK-05: Baslik benzersizligi ---
titles = re.findall(r"^#+\s+(.+)$", mt, re.M)
seen = set()
dup = []
for t in titles:
    tn = t.strip().lower()
    if tn in seen:
        dup.append(t)
    seen.add(tn)
if dup:
    print(f"WARN CHK-05: {len(dup)} tekrar baslik {dup}")
else:
    print(f"PASS CHK-05: {len(titles)} benzersiz baslik")

sys.exit(1 if overall_fail else 0)
