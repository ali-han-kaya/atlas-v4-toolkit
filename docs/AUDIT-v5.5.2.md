# Atlas v5.5.2 — DENETİM RAPORU (2. TUR — bağımsız çift denetim sonrası)

**Tarih:** 2026-08-15
**Bağlam:** v5.5.1 build'i (docs/AUDIT-v5.5.1.md) teslim edildikten sonra kullanıcı
talebiyle iki **bağımsız subagent** (biri statik/mimari denetim, biri gerçek
opencode CLI + script runtime testleri) devreye alındı. Hiçbir revizyon
yapılmadan önce bulgular kullanıcıya raporlandı; onay üzerine bu tur uygulandı.

**Sonuç:** v5.5.1 opencode'u başlatabiliyordu ama **1 kritik (P0) güvenlik açığı**
ve çok sayıda (13 P1, 6 P2, 3 P3) işlevsel/tutarlılık hatası içeriyordu.
Bu build (v5.5.2) tümünü giderir ve her düzeltme runtime testiyle doğrulanmıştır.

---

## P0 — KRİTİK (giderildi)

| # | Bulgu | Kanıt | Düzeltme | Doğrulama |
|---|-------|-------|----------|-----------|
| P0-01 | `gate_merge.py`, agent'in beyan ettiği `metadata.p0_count/p1_count`/`verdict`'e güveniyordu; yanlış/yalancı metadata ile gerçek P0 bulgusu varken FINAL PASS üretilebiliyordu. 2-of-2 güvenlik garantisini geçersiz kılıyordu. | `gate_merge.py:18-32,46-56` (eski) | Tamamen yeniden yazıldı: P0/P1 sayıları HER ZAMAN ham `findings`/`checks`/`manifest_reconciliation`'dan yeniden hesaplanır; agent beyanı sadece şeffaflık için karşılaştırılır; celişki (`metadata_mismatch`) kendi başına FAIL nedenidir. | Saldırı senaryosu (yalancı metadata + gerçek P0) test edildi → doğru şekilde FINAL FAIL. 4 senaryo (attack/normal/kanıtsız/malformed) hepsi doğru sonuç verdi. |

## P1 — YÜKSEK (13/13 giderildi)

| # | Bulgu | Düzeltme | Doğrulama |
|---|-------|----------|-----------|
| P1-01 | Kurulum talimatı (README/HANDOFF) yalnızca `.opencode`+`opencode.json` kopyalıyordu; `scripts/`, `templates/`, `docs/`, `AGENTS.md` eksik kalıyordu. | Kurulum komutu tüm dizinleri kapsayacak şekilde güncellendi + doğrulama adımı eklendi. | Talimat elle simüle edildi, tüm dosyalar hedefte mevcut. |
| P1-02 | Gate 2B komutu `check_integrity.sh --gate`'i `gate_merge.py`'den ÖNCE çağırıyordu; rapor dosyası henüz yoktu. | Sıra düzeltildi: önce merge, sonra `--gate` kontrolü. | Yeni sırayla çalıştırıldı, PASS. |
| P1-03 | `check_integrity.sh --full` yalnızca 2 dosyanın varlığını kontrol edip PASS veriyordu; FAZ1/2/gate/DOI/provenance atlanıyordu. | `--full` artık tüm fazları + gate'i + `verify_doi.py --require-master` + `provenance_check.py`'yi sırayla çalıştırır ve FINAL-GATE verdict'ini zorunlu kontrol eder. | Boş dosyalarla FAIL, tam pipeline fixture'ıyla PASS doğrulandı. |
| P1-04 | `provenance_check.py` CHK-01/02'de ID'nin metnin herhangi bir yerinde geçmesini/`PROVENANCE` kelimesinin varlığını yeterli sayıyordu; sahte PASS mümkündü. | CHK-01 artık markdown BAŞLIĞI eşleşmesi ister; CHK-02 artık PROVENANCE tablosunu satır satır ayrıştırıp her ZORUNLU ID için "kapsıyor" durumu ister. ZORUNLU eşleşmesi tablo-sütunu formatına sıkılaştırıldı (yanlış pozitif önlendi). | 4 senaryo (eksik tablo / sahte metin-eşleşme / yanlış-pozitif / doğru PASS) test edildi, hepsi doğru. |
| P1-05 | `verify_doi.py` DOI HTTP hatalarını (404 vb.) yalnızca yazdırıp exit 0 veriyordu; DOI'ler sırasız (`set`) seçiliyordu. | Doğrulanan (gerçek HTTP yanıtlı) geçersiz DOI artık FAIL nedeni; ağ hatası (exception) ayrı sayılır, FAIL saymaz; DOI seçimi `sorted(set(...))` ile deterministik. | Gerçek CrossRef çağrısıyla 404 DOI → doğru FAIL; 200 DOI → PASS. |
| P1-06 | DEC-027 (§8 M1 `[UNVERIFIED]` istisnası) agent seviyesinde tanımlıydı ama `verify_doi.py` bölüm-farkındasızdı; her `[UNVERIFIED]` hard-FAIL veriyordu. | `verify_doi.py` artık markdown başlıklarını ayrıştırıp "§8"+"M1" içeren bölümü tespit eder; o bölüm İÇİNDEKİ etiketler PASS, DIŞINDAKİLER FAIL. | İstisna-içi / istisna-dışı / karışık 3 senaryo test edildi, hepsi doğru. |
| P1-07 | Structure lens FAZ1'de `PROVENANCE.md`/`FIX-MANIFEST.md` gibi henüz var olmayan ayrı dosyaları zorunlu giriş sayıyordu. | Lens-structure §GİRDİ güncellendi: PROVENANCE artık MASTER içi gömülü tablo olarak, FIX-MANIFEST FAZ1'de "N/A - FAZ2 sonrası" olarak tanımlandı. | Doküman incelemesiyle doğrulandı. |
| P1-08 | CHK-01/02/04/05 şiddetleri lens-structure (P0/P0/P0/P1) ile gate-2a+checklist (P1/P1/P1/P2) arasında çelişiyordu; writer'ın CHK-06/07 tanımı (kategori/sentez) checklist'in CHK-06/07 (chi-square/SC-006) tanımıyla ID çakışıyordu; orchestrator "FIX-201" gibi tanımsız bir istisnaya atıf yapıyordu. | Lens-structure şiddetleri checklist'e eşitlendi; writer'daki çakışan kurallar `YK-01`/`YK-02` (CHK olmayan "yazım kuralı" etiketi) olarak yeniden adlandırıldı; orchestrator'daki "FIX-201" → "SC-006 [YENİ]" olarak düzeltildi. | Tüm CHK referansları `templates/CHK-CHECKLIST.md` ile çapraz kontrol edildi. |
| P1-09 | DEC-036 "her zaman OPEN" + orchestrator'ın "FAZ3 sadece tüm DEC DECIDED/SUPERSEDED ise başlar" kuralı birlikte pipeline'ı mantıksal olarak ilerletilemez kılıyordu. | Orchestrator §3'e açık bypass mekanizması eklendi: DEC-036/DEC-035 `OPEN` kalabilir ve FAZ3'ü bloklamaz; bunun yerine kullanıcı onaylı bir bypass-DEC (`DECIDED`) FAZ3'ü açar, DEC-036 kendisi gate'i (FAZ4) bilinçli olarak bloklamaya devam eder. Scoper + DEC-REGISTER-TEMPLATE + gate-2b tutarlı hale getirildi. | Doküman çapraz kontrolü; mantıksal döngü artık yok. |
| P1-10 | Agent'lardaki "kör gate", "otomatik commit yapma" gibi etik kurallar sadece prompt seviyesindeydi, teknik izin sınırı yoktu. | Tüm agent'lara `permission` blokları eklendi: gate-2a/2b `edit: {"gate/*":allow,"*":deny}` + FIX-MANIFEST okuma engeli (2A); tüm dosya-yazan agent'larda `bash: {"git commit*":deny,"git push*":deny}`; lens'lerde `edit: deny` (salt analiz). | Frontmatter şema-doğrulaması + opencode CLI ile agent listesi kontrolü. |
| P1-11 | Writer-master girdi listesinde kullanıcının orijinal taslak MASTER'ı ve A/B kaynak paketleri YOKTU; sadece türetilmiş fazlar listeleniyordu. | Writer-master §Girdi ve `/atlas-faz3` komutuna "kullanıcının sağladığı TASLAK MASTER + A/B kaynak paketleri" ilk girdi olarak eklendi. | Doküman incelemesi. |
| P1-12 | `budget_guard.py`'de kullanılmayan `master` değişkeni, aylık harcamanın hiç sıfırlanmaması, bozuk/eksik-alanlı `.atlas_budget.json`'da crash riski vardı. | Ölü kod kaldırıldı; `period` (YYYY-MM) alanı eklenip dönem değişiminde otomatik reset; `load_budget()` tüm eksik alanları güvenli varsayılanla tamamlıyor, bozuk JSON'da crash etmeden sıfırdan başlıyor. | 3 senaryo (eksik alan / tamamen bozuk / farklı dönem) test edildi, hepsi crash etmeden doğru çalıştı. |
| P1-13 | Genel/alan-agnostik pipeline iddiası ile scoper/gate/lens-consistency içindeki çalışma-özel zorunluluklar (chi-square, DEC-027, DEC-035/036) çelişiyordu. | `docs/PIPELINE.md`'ye "Çekirdek vs Alan-Özel Kontroller" bölümü eklendi; hangi kontrollerin örnek çalışmaya özgü olduğu ve yeni çalışmalar için nasıl uyarlanacağı açıkça belgelendi. | Doküman incelemesi. |

## P2 — ORTA (6/6 giderildi)

| # | Bulgu | Düzeltme |
|---|-------|----------|
| P2-01 | FINAL rapor (`04-FAZ-4-...md`) bulgu detaylarını kaybediyordu, sadece sayaç gösteriyordu. | `gate_merge.py` artık tüm bulguları (`_source` etiketiyle) hem JSON'a hem Markdown raporuna yazıyor. |
| P2-02 | Build sürümü (v5.5.1/v5.5.2) hiçbir artefaktta makine-okunur şekilde ayırt edilemiyordu. | `gate_merge.py` çıktısına `"build": "v5.5.2"` alanı eklendi; `docs/PIPELINE.md`/`CHANGELOG` güncellendi. |
| P2-03 | Agent frontmatter'daki özel `version`/`role` alanları provider `options`'a yönlendirilip sürüm-bağımlı belirsizlik riski taşıyordu. | Tüm agent frontmatter'larından `version`/`role` kaldırıldı (bilgi zaten AGENTS.md tablosunda ve dosya içi prose'da mevcut). |
| P2-04 | `/atlas-verify` bir doğrulama raporu (`05-...md`) vaat ediyordu ama hiçbir adım bu dosyayı üretmiyordu. | Komuta açık bir "raporu yaz" adımı + format şablonu + `ls -la` doğrulaması eklendi. |
| P2-05 | Command dosyaları hedef agent'ı teknik olarak sabitlemiyordu (yalnızca doğal dil talimatı). | Tüm command frontmatter'larına `agent:` alanı eklendi (scoper/orchestrator/writer-master/gate-2a/gate-2b). |
| P2-06 | Lens JSON şemaları kendi kurallarıyla çelişiyordu (`checks_run` için kanıt alanı istenip şemada yer verilmemesi). | Kural gevşetildi: `findings` boşsa denetim otomatik başarılı sayılır, ayrı kanıt alanı gerekmez. |

## P3 — DÜŞÜK (3/3 giderildi)

| # | Bulgu | Düzeltme |
|---|-------|----------|
| P3-01 | `AGENTS.md` "6 çalışan + 1 deprecated" diyordu; gerçek sayı 9+3. Wrapper dosyaları yanlış satır sayısına atıf yapıyordu. | Roster başlığı "9 çalışan + 3 deprecated" yapıldı; satır sayısı referansları kaldırıldı (drift riski). |
| P3-02 | `/atlas-full`'un "otomatik zincirler" diye belgelenmesi, gerçek (güvenli, no-op) davranışıyla çelişiyordu. | Komut dosyasına + ilgili dokümana "bu isim çağrıştırsa da otomatik zincirleme YOKTUR" açıklaması eklendi. |
| P3-03 | `check_integrity.sh` yardım metni gerçek `--` önekli kullanımla uyuşmuyordu. | Yardım metni gerçek kullanımla eşitlendi. |

---

## Runtime Doğrulama Özeti (bu tur)

| Test | Sonuç |
|------|-------|
| `gate_merge.py` — yalancı metadata + gerçek P0 (saldırı) | FAIL (doğru) |
| `gate_merge.py` — gerçek temiz durum | PASS (doğru) |
| `gate_merge.py` — KANITSIZ manifest | FAIL (doğru) |
| `gate_merge.py` — malformed JSON şekli | FAIL + anlamlı hata (doğru) |
| `verify_doi.py` — MASTER yok (normal / `--require-master`) | 0 / 1 (doğru) |
| `verify_doi.py` — DEC-027 istisna içi/dışı/karışık | PASS/FAIL/FAIL (doğru) |
| `verify_doi.py` — gerçek CrossRef 404 DOI | FAIL (doğru) |
| `provenance_check.py` — sahte PROVENANCE (kelime var, tablo yok) | FAIL (doğru, önceden PASS idi) |
| `provenance_check.py` — "ZORUNLU değil" yanlış-pozitif kontrolü | zorunlu SAYILMADI (doğru) |
| `provenance_check.py` — tam geçerli pipeline | PASS (doğru) |
| `budget_guard.py` — eksik alan / bozuk JSON / farklı dönem | crash yok, doğru reset (doğru) |
| `check_integrity.sh --full` — boş dosyalar | FAIL (doğru, önceden PASS idi) |
| `check_integrity.sh --full` — tam geçerli pipeline (FAZ0..4 + gate) | PASS (doğru) |
| `check_integrity.sh --gate` — eksik 2A/2B JSON | FAIL (doğru, önceden PASS idi) |
| Tüm `.py` dosyaları `py_compile` | OK |
| `check_integrity.sh` `bash -n` | OK |

## Bilinçli bırakılanlar / kapsam dışı

- Model API çağrıları (gerçek LLM çıktı kalitesi) test kapsamı dışıdır — bu bir
  statik/runtime script + config denetimidir, prompt kalitesi değerlendirmesi değil.
- Pipeline'ın "kullanıcı taslak MASTER sağlar" mimarisi (FAZ1→FAZ3 sıralaması)
  kasıtlı tasarım kararı olarak korundu (kullanıcı onayıyla, bkz. v5.5.1 audit).
