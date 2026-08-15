# Atlas v5.5 — DENETİM RAPORU (AUDIT)

**Tarih:** 2026-08-15
**Denetlenen:** `Atlas-v5-5.zip` (v5.5 "FINAL OPTIMIZE")
**Karşılaştırma tabanı:** ATLAS_v4.0, Atlas-v5, Atlas-v5.1
**Sonuç:** v5.5 "ideal/optimize" DEĞİLDİ — opencode'u başlatamayan kritik bir config
hatası + birkaç davranışsal tutarsızlık + boş template'ler içeriyordu. Bu build
(v5.5.1) bunları giderir.

---

## 1. Yöntem

- 4 sürüm (v4.0, v5, v5.1, v5.5) açıldı ve dosya dosya karşılaştırıldı (`diff -rq`).
- v5.5'in tüm dosyaları (12 agent, 8 command, 5 script, 5 template, config, docs) okundu.
- `opencode.json`, resmî şemaya (`https://opencode.ai/config.json`) karşı doğrulandı.
- Tüm Python script'leri `py_compile`, bash script'i `bash -n` ile sözdizimi testinden geçti (hepsi temiz).

## 2. Bulgular

Şiddet: **KRİTİK** (opencode başlamaz) · **CİDDİ** (pipeline mantık çelişkisi) · **ORTA** · **DÜŞÜK**

| # | Şiddet | Bulgu | Kanıt | Çözüm |
|---|--------|-------|-------|-------|
| F-01 | KRİTİK | `opencode.json` üst düzey şema-dışı anahtarlar: `version`, `description`, `pipeline`. Config şeması `additionalProperties:false` → `ConfigInvalidError`, opencode başlamaz. | opencode.json:4,5,24 | Kaldırıldı; bilgi `docs/PIPELINE.md`'ye taşındı. |
| F-02 | KRİTİK | `provider.openrouter.models.<id>.role` alanı model şemasında yok (`additionalProperties:false`). Ayrıca başlatmayı engeller. | opencode.json:10,13,16,19 | `role` kaldırıldı; model'ler `{}` olarak bırakıldı (geçerli). |
| F-03 | CİDDİ | `[UNVERIFIED]` çelişkisi: orchestrator §8 M1'de DEC-027 ile izin verir; writer CHK-03 ve gate-2a CHK-03 P0→FAIL sayar → geçerli MASTER kapıdan geçemez. | orchestrator.md:22 vs writer.md:41, gate-2a.md:22 | writer + gate-2a'ya DEC-027 §8 M1 istisnası eklendi (CHK-07 kalıbı). |
| F-04 | ORTA | CHK-01 sayı tutarsızlığı: "22 ZORUNLU" (writer/gate/lens/README) vs 24 zorunlu (scoper: 22 sabit + 2 esnek ZORUNLU). | scoper.md:25,49 vs writer.md:33 | "tüm ZORUNLU (≥22)" olarak harmonize; `provenance_check.py` zaten dinamik. |
| F-05 | ORTA | 5 template tek satırlık boş iskelet + yanlış sürüm ("v5.4"). Hiç içerik yok. | templates/*.md | Dokümante edilmiş sütun formatlarıyla gerçek iskeletler yazıldı; v5.5. |
| F-06 | ORTA | Deprecated 3 wrapper (`gate-strong`, `gate-manifest`, `gate_2`) `disable:true` değil → aktif agent olarak yüklenir. | agent/atlas-gate-*.md | `disable: true` eklendi. |
| F-07 | DÜŞÜK | writer-master frontmatter `default: true` — geçersiz alan; varsayılan agent'ı belirlemez. | writer-master.md:4 | Kaldırıldı; `opencode.json` `default_agent` kullanıldı. |
| F-08 | DÜŞÜK | Çalışan agent'larda `mode` yok. | tüm agent'lar | orchestrator=primary, diğerleri=subagent. |
| F-09 | DÜŞÜK | `verify_doi.py` her `[UNVERIFIED]`'da hard-FAIL; DEC-027 §8 M1 istisnasını bilmez (bölüm-farkındasız). | verify_doi.py:36,62 | Davranış korundu; açıklayıcı yorum + gate-2a'nın hakem olduğu notu eklendi. |

## 3. Bilinçli değiştirilmeyenler (tasarım kararı)

- **Girdi taslağı (F-ordering):** Lens'ler (FAZ1) MASTER'ı denetler ama Writer MASTER'ı
  FAZ3'te üretir. Kullanıcı doğrulaması: Atlas bir **denetim aracıdır**, kullanıcı taslak
  MASTER sağlar. Mantık değiştirilmedi; yalnızca README + PIPELINE + HANDOFF'ta belgelendi.
- **DEC-036 hep OPEN → gate FAIL:** Etik onay gelmeden FINAL PASS olmaması kasıtlı güvenlik
  önlemidir. Korundu, belgelendi.

## 4. Doğrulama

- Yeni `opencode.json` resmî şemaya karşı doğrulandı: tüm anahtarlar `Config` izinli
  kümesinde, tüm model anahtarları model şemasında geçerli.
- Tüm script'ler sözdizimi testinden geçti (py_compile / bash -n).
- Artefakt token'ı `-v5.5` korunduğundan script↔agent↔command dosya adı referansları bozulmadı.

## 5. Sürüm sağlık özeti

| Sürüm | opencode başlar mı? | Not |
|-------|--------------------|-----|
| v4.0 | (ayrı yapı, HANDOFF_V3) | Orijinal; 3 lens + gate |
| v5 | HAYIR | `version`+`fixes` şema-dışı |
| v5.1 | HAYIR | v5 ile ~aynı; `version`+`fixes` şema-dışı |
| v5.5 | HAYIR | `version`+`description`+`pipeline`+`role` şema-dışı |
| **v5.5.1 (bu build)** | **EVET** | Şema-geçerli + tutarlı + dolu template |
