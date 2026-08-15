#!/usr/bin/env python3
"""Atlas v5.5.2 Budget Guard — $30/ay/proje limit (sikilastirilmis)

Onceki surumden farklar:
- Aylik donem takibi: farkli ay basladiginda spent/articles/history sifirlanir.
- Bozuk/eksik-alanli .atlas_budget.json artik crash etmez (setdefault ile
  guvenli varsayilanlar).
- Kullanilmayan 'master' degiskeni kaldirildi.
"""
import pathlib, json, sys
from datetime import datetime, timezone

FILES = [
    "00-FAZ-0-SCOPE-CONTRACT-ve-REGISTER.md",
    "01-FAZ-1-LENS-SWARM-DENETIM.md",
    "03-FAZ-3-MASTER-v5.5.md",
]
LIMIT = 30.0


def tokens(p):
    try:
        return pathlib.Path(p).stat().st_size // 4
    except Exception:
        return 0


def current_period():
    return datetime.now(timezone.utc).strftime("%Y-%m")


def load_budget(path):
    default = {"period": current_period(), "spent": 0.0, "articles": 0, "history": [], "last_mode": None, "last_date": None}
    if not path.exists():
        return default
    try:
        raw = json.loads(path.read_text())
    except Exception:
        print("WARN: .atlas_budget.json bozuk, sifirdan baslatiliyor")
        return default
    if not isinstance(raw, dict):
        print("WARN: .atlas_budget.json gecersiz sekil, sifirdan baslatiliyor")
        return default
    # Guvenli varsayilanlarla eksik alanlari tamamla
    for k, v in default.items():
        raw.setdefault(k, v)
    if not isinstance(raw.get("history"), list):
        raw["history"] = []
    if not isinstance(raw.get("spent"), (int, float)):
        raw["spent"] = 0.0
    if not isinstance(raw.get("articles"), int):
        raw["articles"] = 0
    return raw


all_files = [f for f in FILES if pathlib.Path(f).exists()]
total = sum(tokens(f) for f in all_files)
mode = "SINGLE" if total <= 50000 else "PAIRWISE"
cost = 0.25 if mode == "SINGLE" else 0.60
total_cost = cost + 0.20 + 0.35  # lens + gate

bf = pathlib.Path(".atlas_budget.json")
data = load_budget(bf)

period = current_period()
if data.get("period") != period:
    print(f"NOT: yeni donem ({period}), bir onceki donemin ({data.get('period')}) harcamasi sifirlaniyor")
    data = {"period": period, "spent": 0.0, "articles": 0, "history": [], "last_mode": None, "last_date": None}

if "--report" not in sys.argv:
    now = datetime.now(timezone.utc).isoformat()
    data["spent"] += total_cost
    data["articles"] += 1
    data["last_mode"] = mode
    data["last_date"] = now
    data["history"].append({"date": now, "cost": round(total_cost, 2), "tokens": total, "mode": mode})
    data["history"] = data["history"][-100:]
    bf.write_text(json.dumps(data, indent=2))

print(f"Token: {total} | Mod: {mode} | Maliyet: ${total_cost:.2f}")
print(f"Donem {data['period']}: ${data['spent']:.2f}/${LIMIT} | Makale: {data['articles']}")

if data["spent"] > LIMIT:
    print("FAIL: budget asildi")
    sys.exit(1)
else:
    print("OK: budget icinde")
