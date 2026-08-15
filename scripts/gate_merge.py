#!/usr/bin/env python3
"""Atlas v5.5.2 Gate Merge — 2-of-2 Voting (guvenlik-sikilastirilmis)

Kullanim: python3 scripts/gate_merge.py gate/STRONG-gate-2a-v5.5.json gate/STRONG-gate-2b-v5.5.json

GUVENLIK ILKESI (P0-01 duzeltmesi):
Bu script agent'in kendi beyan ettigi `verdict` veya `metadata.p0_count/p1_count`
alanlarina GUVENMEZ. P0/P1 sayilari HER ZAMAN ham `findings`, `checks` ve
`manifest_reconciliation` dizilerinden yeniden hesaplanir. Agent beyani ile
yeniden hesaplanan deger celisirse bu celiskinin kendisi FAIL nedenidir
(metadata_mismatch).
"""
import json, sys, pathlib
from datetime import datetime, timezone


def load(p):
    try:
        raw = pathlib.Path(p).read_text()
    except Exception as e:
        return None, f"okunamadi: {e}"
    try:
        data = json.loads(raw)
    except Exception as e:
        return None, f"JSON gecersiz: {e}"
    if not isinstance(data, dict):
        return None, "JSON kok nesnesi dict degil"
    return data, None


def recompute_counts(gate):
    """P0/P1 sayilarini SADECE ham dizilerden hesapla. Metadata'ya bakma."""
    p0 = 0
    p1 = 0
    findings = gate.get("findings", [])
    if not isinstance(findings, list):
        findings = []
    for f in findings:
        if not isinstance(f, dict):
            continue
        pr = str(f.get("priority", "")).upper()
        if pr == "P0":
            p0 += 1
        elif pr == "P1":
            p1 += 1

    # checks dizisindeki FAIL durumlari da P1 muadili sayilir (2A CHK tablosu)
    checks = gate.get("checks", [])
    if isinstance(checks, list):
        for c in checks:
            if isinstance(c, dict) and str(c.get("status", "")).upper() == "FAIL":
                p1 += 1

    # manifest_reconciliation icindeki KANITSIZ / UYGULANMAMIS-ama-UYGULANMIS-denen
    # durumlar P0 sayilir (2B)
    manifest = gate.get("manifest_reconciliation", [])
    if isinstance(manifest, list):
        for m in manifest:
            if not isinstance(m, dict):
                continue
            status = str(m.get("status", "")).upper()
            if "KANITSIZ" in status:
                p0 += 1

    return p0, p1


def declared_counts(gate):
    """Agent'in kendi beyan ettigi sayilar (sadece karsilastirma/seffaflik icin)."""
    meta = gate.get("metadata", {})
    if not isinstance(meta, dict):
        return None, None
    dp0 = meta.get("p0_count")
    dp1 = meta.get("p1_count")
    return dp0, dp1


def evaluate(gate, label):
    """Bir gate JSON'u icin gercek verdict'i BAGIMSIZ hesapla."""
    p0, p1 = recompute_counts(gate)
    declared_verdict = str(gate.get("verdict", "")).upper()
    dp0, dp1 = declared_counts(gate)

    # Gercek verdict SADECE yeniden hesaplanan sayilardan turetilir.
    real_verdict = "PASS" if (p0 == 0 and p1 == 0) else "FAIL"

    mismatch = False
    mismatch_notes = []
    if declared_verdict and declared_verdict != real_verdict:
        mismatch = True
        mismatch_notes.append(
            f"{label}: agent verdict='{declared_verdict}' ama yeniden hesaplanan='{real_verdict}'"
        )
    if dp0 is not None and int(dp0) != p0:
        mismatch = True
        mismatch_notes.append(f"{label}: agent p0_count={dp0} ama gercek={p0}")
    if dp1 is not None and int(dp1) != p1:
        mismatch = True
        mismatch_notes.append(f"{label}: agent p1_count={dp1} ama gercek={p1}")

    return {
        "label": label,
        "real_verdict": real_verdict,
        "declared_verdict": declared_verdict or None,
        "p0": p0,
        "p1": p1,
        "declared_p0": dp0,
        "declared_p1": dp1,
        "mismatch": mismatch,
        "mismatch_notes": mismatch_notes,
        "findings": gate.get("findings", []) if isinstance(gate.get("findings", []), list) else [],
    }


if len(sys.argv) < 3:
    print("Kullanim: gate_merge.py 2a.json 2b.json")
    sys.exit(1)

a, err_a = load(sys.argv[1])
b, err_b = load(sys.argv[2])

if a is None or b is None:
    print(f"FAIL: JSON okunamadi. 2A: {err_a or 'ok'} | 2B: {err_b or 'ok'}")
    sys.exit(1)

res_a = evaluate(a, "2A")
res_b = evaluate(b, "2B")

any_mismatch = res_a["mismatch"] or res_b["mismatch"]
# 2-of-2: HER IKI gate'in GERCEK (yeniden hesaplanan) verdict'i PASS olmali.
# Metadata/agent-beyan celiskisi VARSA guven kirilmistir -> FAIL.
verdict = "PASS" if (res_a["real_verdict"] == "PASS" and res_b["real_verdict"] == "PASS" and not any_mismatch) else "FAIL"

reason_parts = [
    f"2A={res_a['real_verdict']}(P0:{res_a['p0']},P1:{res_a['p1']})",
    f"2B={res_b['real_verdict']}(P0:{res_b['p0']},P1:{res_b['p1']})",
]
if any_mismatch:
    reason_parts.append("METADATA_MISMATCH")
reason = " ".join(reason_parts) + f" -> {verdict}"

all_findings = []
for res in (res_a, res_b):
    for f in res["findings"]:
        if isinstance(f, dict):
            entry = dict(f)
            entry["_source"] = res["label"]
            all_findings.append(entry)

out = {
    "atlas_version": "v5.5",
    "build": "v5.5.2",
    "gate_type": "FINAL-2-of-2",
    "verdict": verdict,
    "reason": reason,
    "gate_2a": res_a["real_verdict"],
    "gate_2b": res_b["real_verdict"],
    "counts": {
        "p0_2a": res_a["p0"], "p1_2a": res_a["p1"],
        "p0_2b": res_b["p0"], "p1_2b": res_b["p1"],
    },
    "metadata_integrity": {
        "mismatch_detected": any_mismatch,
        "mismatch_notes": res_a["mismatch_notes"] + res_b["mismatch_notes"],
    },
    "findings": all_findings,
    "metadata": {"gate_date": datetime.now(timezone.utc).isoformat(), "voting": "2-of-2"},
}

pathlib.Path("gate").mkdir(exist_ok=True)
pathlib.Path("gate/FINAL-GATE-v5.5.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))

findings_md = "\n".join(
    f"- [{f.get('_source','?')}] {f.get('priority','?')} — {f.get('finding') or f.get('evidence') or f.get('issue') or '(detay yok)'} "
    f"(konum: {f.get('location','?')})"
    for f in all_findings
) or "(bulgu yok)"

mismatch_md = "\n".join(f"- {n}" for n in out["metadata_integrity"]["mismatch_notes"]) or "(yok)"

report = f"""# FINAL GATE RAPORU — v5.5.2

## Verdict: {verdict}
{reason}

## Gate 2A (Claude Sonnet 4 — Kor Denetim)
- Gercek verdict (yeniden hesaplanan): {res_a['real_verdict']}
- Agent beyani: {res_a['declared_verdict']}
- P0: {res_a['p0']}, P1: {res_a['p1']}

## Gate 2B (GPT-OSS 20B — Manifest Dogrulama)
- Gercek verdict (yeniden hesaplanan): {res_b['real_verdict']}
- Agent beyani: {res_b['declared_verdict']}
- P0: {res_b['p0']}, P1: {res_b['p1']}

## Metadata Butunluk Kontrolu
Mismatch tespit edildi mi: {any_mismatch}
{mismatch_md}

## Bulgu Detaylari
{findings_md}

Tarih: {datetime.now(timezone.utc).isoformat()}
"""

pathlib.Path("04-FAZ-4-STRONG-GATE-RAPORU-v5.5.md").write_text(report)

print(f"FINAL {verdict} {reason}")
sys.exit(0 if verdict == "PASS" else 1)
