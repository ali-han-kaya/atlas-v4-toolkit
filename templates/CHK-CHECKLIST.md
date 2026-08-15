# CHK-CHECKLIST — Atlas v5.5

> Lens (FAZ1) ve Gate (FAZ4) ajanlarının uyguladığı 7 kontrol. Severity: P0 kritik
> (yayın/karar bloklayıcı), P1 düzeltilmeli (bloklamaz), P2 kozmetik/kabul.

| CHK | Açıklama | Severity | Karar |
|-----|----------|----------|-------|
| CHK-01 | Tüm ZORUNLU SCOPE-ID (≥22) MASTER'da bölüm olarak var mı? | P1 | eksikse FAIL |
| CHK-02 | Tüm ZORUNLU SCOPE-ID PROVENANCE tablosunda "kapsıyor" mu? | P1 | eksikse FAIL |
| CHK-03 | `[DOĞRULANMADI]` / `[DOGRULANAMADI]` / `[UNVERIFIED]` etiketi var mı? | P0 | varsa FAIL (İSTİSNA: DEC-027 §8 M1 kasıtlı) |
| CHK-04 | Etik kurallar + DEC-036 atfı + DPIA belgesi mevcut mu? | P1 | eksikse FAIL |
| CHK-05 | `##` / `###` başlıkları benzersiz mi? | P2 | tekrar varsa belgele, PASS |
| CHK-06 | Chi-square p-değeri tek tutarlı değer mi? Bilinen çelişkiler çözülmüş mü? | P0 | tutarsızsa FAIL |
| CHK-07 | `SC-006 [YENİ]` notu var, yanında `[DOĞRULANMADI]` yok — kasıtlı istisna | PASS | her zaman PASS |

**Verdict kuralı (gate):** P0 ≥ 1 → FAIL; P1 ≥ 1 → FAIL; yalnız P2 → PASS (belgelenir).
