#!/bin/bash
# Atlas v5.5.2 Integrity Check (sikilastirilmis)
set -e

FAZ=${1:-"--full"}
BASEDIR="."
echo "=== ATLAS v5.5.2 Integrity $FAZ ==="

check_exists(){ [ -f "$1" ] || { echo "FAIL $1 yok"; exit 1; }; }
check_size(){
  S=$(wc -c < "$1")
  [ "$S" -ge "$2" ] || { echo "FAIL $1 kucuk $S < $2"; exit 1; }
  echo "OK $1 ${S}B"
}
check_contains(){
  grep -q "$2" "$1" || { echo "FAIL $1 icinde '$2' yok"; exit 1; }
  echo "OK $1 icinde '$2' var"
}
check_json(){
  python3 -c "import json; json.load(open('$1'))" 2>/dev/null && echo "OK JSON $1" || { echo "FAIL JSON $1 gecersiz"; exit 1; }
}
check_json_verdict_pass(){
  V=$(python3 -c "import json; print(json.load(open('$1')).get('verdict','?'))" 2>/dev/null) || { echo "FAIL $1 okunamadi"; exit 1; }
  [ "$V" = "PASS" ] || { echo "FAIL $1 verdict=$V (PASS bekleniyor)"; exit 1; }
  echo "OK $1 verdict=PASS"
}

MASTER="03-FAZ-3-MASTER-v5.5.md"

case $FAZ in
  --faz0)
    check_exists "00-FAZ-0-SCOPE-CONTRACT-ve-REGISTER.md"
    check_size "00-FAZ-0-SCOPE-CONTRACT-ve-REGISTER.md" 1000
    check_contains "00-FAZ-0-SCOPE-CONTRACT-ve-REGISTER.md" "SC-"
    check_contains "00-FAZ-0-SCOPE-CONTRACT-ve-REGISTER.md" "DEC-"
    ;;
  --faz1)
    check_exists "01-FAZ-1-LENS-SWARM-DENETIM.md"
    check_size "01-FAZ-1-LENS-SWARM-DENETIM.md" 5000
    check_contains "01-FAZ-1-LENS-SWARM-DENETIM.md" "CHK-"
    check_contains "01-FAZ-1-LENS-SWARM-DENETIM.md" "P0"
    ;;
  --faz2)
    check_exists "02-FAZ-2-FIXER-SWARM.md"
    check_size "02-FAZ-2-FIXER-SWARM.md" 1000
    check_contains "02-FAZ-2-FIXER-SWARM.md" "FIX-"
    ;;
  --faz3)
    check_exists "$MASTER"
    check_size "$MASTER" 15000
    check_contains "$MASTER" "PROVENANCE"
    echo "-- verify_doi.py (DEC-027 bolum-farkindali, sert kontrol) --"
    python3 scripts/verify_doi.py --require-master
    echo "-- provenance_check.py (CHK-01/02/05) --"
    python3 scripts/provenance_check.py
    ;;
  --gate)
    check_exists "gate/STRONG-gate-2a-v5.5.json"
    check_json "gate/STRONG-gate-2a-v5.5.json"
    check_exists "gate/STRONG-gate-2b-v5.5.json"
    check_json "gate/STRONG-gate-2b-v5.5.json"
    check_exists "gate/FINAL-GATE-v5.5.json"
    check_json "gate/FINAL-GATE-v5.5.json"
    check_exists "04-FAZ-4-STRONG-GATE-RAPORU-v5.5.md"
    ;;
  --full)
    echo "-- FAZ0 --"; $0 --faz0
    echo "-- FAZ1 --"; $0 --faz1
    echo "-- FAZ2 --"; $0 --faz2
    echo "-- FAZ3 (verify_doi + provenance_check dahil) --"; $0 --faz3
    echo "-- GATE --"; $0 --gate
    echo "-- FINAL VERDICT --"
    check_json_verdict_pass "gate/FINAL-GATE-v5.5.json"
    echo "FULL PASS v5.5.2 — tum fazlar + gate dogrulandi"
    ;;
  *)
    echo "Kullanim: $0 --faz0|--faz1|--faz2|--faz3|--gate|--full"
    exit 1
    ;;
esac
