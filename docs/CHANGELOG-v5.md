# Atlas CHANGELOG

## v5.5.2 — GÜVENLİK + TUTARLILIK SIKILAŞTIRMA (bu build)

v5.5.1 teslim edildikten sonra iki bağımsız subagent denetimi (mimari/statik +
gerçek opencode CLI/runtime) yapıldı. 1 P0 (kritik güvenlik) + 13 P1 + 6 P2 +
3 P3 bulgu tespit edildi; kullanıcı onayı sonrası TÜMÜ giderildi. Tam liste ve
kanıtlar: `docs/AUDIT-v5.5.2.md`.

**En kritik düzeltme (P0):** `gate_merge.py` artık agent'ın kendi beyan ettiği
`verdict`/`p0_count`/`p1_count`'a güvenmiyor; P0/P1 sayılarını HER ZAMAN ham
`findings`/`checks`/`manifest_reconciliation` dizilerinden bağımsız olarak
yeniden hesaplıyor. Beyan ile gerçek durum çelişirse (`metadata_mismatch`) bu
tek başına FAIL nedenidir. Önceden: yalancı/hatalı metadata ile gerçek P0
bulgusu varken FINAL PASS üretilebiliyordu.

Diğer önemli düzeltmeler: `verify_doi.py` artık DEC-027 (§8 M1) istisnasını
bölüm-farkındalığıyla doğru uyguluyor ve gerçek DOI HTTP hatalarını FAIL
sayıyor; `provenance_check.py` CHK-01/02'de sahte PASS'i engelleyecek şekilde
sıkılaştırıldı (başlık eşleşmesi + tablo satırı doğrulaması); `check_integrity.sh
--full/--gate` artık gerçekten tüm fazları ve gate zincirini doğruluyor (önceden
sadece 2 dosyanın varlığına bakıyordu); `budget_guard.py`'deki crash ve aylık
reset hataları giderildi; agent'lara teknik `permission` sınırları eklendi (kör
gate artık FIX-MANIFEST'i okuyamaz, gate/lens agent'ları kendi çıktı
dizinleri dışına yazamaz, hiçbir agent `git commit`/`push` çalıştıramaz);
CHK-01..07 şiddet/tanım çakışmaları (lens vs gate vs writer vs checklist)
tek kaynağa (`templates/CHK-CHECKLIST.md`) göre harmonize edildi; DEC-036
mantıksal kilidi açık bir bypass mekanizmasıyla çözüldü; kurulum talimatı
artık paketin tamamını kapsıyor.

## v5.5.1 — CONFIG-FIX & CONSISTENCY

v5.5 üzerine, opencode'u gerçekten çalıştıran ve tutarlılık sağlayan düzeltmeler.
Pipeline artefakt token'ı (`-v5.5` dosya adları) korundu — script/agent referansları bozulmadı.

### Kritik (opencode başlatma)
- **opencode.json şema-geçerli yapıldı.** Şema-dışı üst düzey anahtarlar (`version`,
  `description`, `pipeline`) ve `provider.openrouter.models.<id>.role` alanları
  kaldırıldı. opencode `Config` ve model şemaları `additionalProperties: false`
  olduğu için bunlar `ConfigInvalidError` ile başlatmayı engelliyordu (v5, v5.1, v5.5).
- **`default_agent: atlas-orchestrator`** eklendi; orchestrator `mode: primary` yapıldı.
- **`instructions: ["AGENTS.md"]`** eklendi — roster her oturumda bağlama girer.
- Kaybolan pipeline/version/model→rol bilgisi `docs/PIPELINE.md`'ye taşındı.

### Tutarlılık
- **[UNVERIFIED] çelişkisi giderildi.** orchestrator §8 M1'de DEC-027 kapsamında
  `[UNVERIFIED]`'a izin verirken writer/gate-2a bunu P0→FAIL sayıyordu. Artık her
  ikisinde de DEC-027 §8 M1 istisnası (CHK-07/SC-006 mantığıyla) açıkça tanımlı.
- **CHK-01 sayısı harmonize edildi.** Sabit "22 ZORUNLU" ifadeleri "tüm ZORUNLU (≥22)"
  yapıldı; scoper 22 sabit + 2 esnek ZORUNLU üretir, `provenance_check.py` dinamik sayar.
- `verify_doi.py`'ye DEC-027 istisna notu (yorum) eklendi; davranış değişmedi.

### Temizlik
- Deprecated wrapper'lar (`atlas-gate-strong`, `atlas-gate-manifest`, `atlas-gate_2`)
  `disable: true` yapıldı — aktif agent olarak yüklenip listeyi kirletmiyorlar.
- Çalışan agent'lara `mode` eklendi (orchestrator=primary, diğerleri=subagent).
- writer-master'daki geçersiz `default: true` kaldırıldı (yerine `default_agent`).
- 5 template (SCOPE-CONTRACT, DEC-REGISTER, FIX-MANIFEST, PROVENANCE, CHK-CHECKLIST)
  boş tek-satır iskeletten, dokümante edilmiş sütun formatlarıyla gerçek iskeletlere
  dolduruldu; başlık v5.4 → v5.5.

### Bilinçli bırakılanlar (davranış değişmedi; bkz. docs/HANDOFF-CONTEXT.md)
- **Girdi taslağı:** FAZ1 lens'leri MASTER'ı denetler → kullanıcı pipeline'a girmeden
  bir taslak MASTER sağlar (denetim aracı modeli). Sadece dokümante edildi.
- **DEC-036 hep OPEN → gate FAIL:** etik güvenlik önlemi; kasıtlı, korundu.

## v5.5 — FINAL OPTIMIZE


v5.4 uzerine 3 kritik iyilestirme + genel temizlik:

### Duzeltmeler
- **Writer-master**: 17 satir → 57 satir detayli prompt (bolum sablonu, CHK kurallari, format, self-healing)
- **Scoper**: 36 satir → 52 satir (22 sabit ZORUNLU tanimli, DEC-REGISTER ornegi, tanimlar sozlugu)
- **Gate 2A**: 28 satir → 56 satir (tablo formatinda CHK listesi, tam JSON sablonu, evidence kurallari)
- **Gate 2B**: 24 satir → 41 satir (JSON sablonu, KANITSIZ detayi, PROVENANCE coverage)

### Temizlik
- Tum agent dosyalarindan meta-yorumlar silindi
- Tek frontmatter, tek versiyon (v5.5), tek role alani
- Wrapper dosyalari (gate-strong, gate-manifest) net yonlendirici
- Lens prompt'lari v4.0 kalitesinde korundu, v5.3 regresyonu kalici olarak duzeltildi
- gate_merge.py: timezone-aware, rapor dosyasi uretiyor, duzgun docstring
- verify_doi.py: rate limiting (1.1s), 4 dosya adi fallback, UTF-8 DOI
- provenance_check.py: duzgun docstring, detayli hata mesajlari
- check_integrity.sh: --faz0 --faz1 --faz2 --faz3 --gate --full, check_json, kullanim bilgisi
- budget_guard.py: timezone-aware, history[-100] limiti
- Command dosyalari: normalize edilmis adim listesi, self-healing adimlari dahil
- opencode.json: pipeline haritasi (FAZ0-FAZ4), model→role eslemesi
- AGENTS.md: agent roster tablosu, model maliyet tablosu

## v5.4 — MERGED

v5.2 icerik + v5.3 temizlik:
- v4.0 kaliteli lens prompt'lari (73/93/47 satir) korundu
- Orchestrator 100 satir korundu
- Script'ler v5.2 seviyesine geri getirildi

## v5.3 — CLEAN

- Cift frontmatter temizlendi
- Versiyon tutarliligi (tum dosyalarda v5.3)
- Kopya gate → wrapper approach
- gate_merge.py asymmetric P0/P1 bug duzeltildi
- Regresyon: lens prompt'lari silindi (v5.4'te geri getirildi)

## v5.2 — FIXED

- Gate: GPT-OSS → Claude Sonnet 4
- FAZ0/FAZ3 ayrildi (scoper + writer-master)
- Self-healing script'leri eklendi
- gate_merge.py 2-of-2 voting eklendi

## v5.1

- v5 ile bayt bayt ayni (gercek degisiklik yok)

## v4.0 — Orijinal

- Orchestrator (96 satir) + 3 Lens (213 satir) + Gate (GPT-OSS 20B)
- CHK-01..07, DEC-XXX, SCOPE-CONTRACT, PROVENANCE, FIX-MANIFEST
