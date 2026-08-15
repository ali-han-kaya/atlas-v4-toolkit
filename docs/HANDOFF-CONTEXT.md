# Atlas — BAĞLAM DEVRİ (HANDOFF-CONTEXT)

> Bu belge, Atlas üzerinde çalışacak **başka bir yapay zekânın** (veya insanın)
> sıfırdan tam bağlamı kavrayıp kaldığı yerden devam edebilmesi için yazıldı.
> Tek başına okunduğunda projeyi bütünüyle anlatır.

---

## 1. Atlas nedir?

Atlas, **opencode** üzerine kurulu, çok-ajanlı bir **akademik makale denetim +
sertleştirme (yazım) pipeline**'ıdır. Alan odağı: sinirbilim, felsefe, teoloji,
bilişsel bilim (7 alan bağlantısı). Amaç: bir akademik makale taslağını sistematik
denetimden geçirip (yapı, tutarlılık, editöryel), düzeltip, bağımsız bir "kapı"dan
(gate) geçirerek güvenilir, izlenebilir (provenance'lı) bir MASTER üretmek.

Atlas kendi başına bir yazılım değildir; bir dizi **opencode agent + command +
script + template**'ten oluşan bir konfigürasyondur. Bir opencode projesine
kopyalanıp çalıştırılır.

## 2. Kurulum & çalıştırma

```bash
# TÜM paket kopyalanmalı — sadece .opencode + opencode.json YETERSİZDİR.
# Komutlar scripts/ altındaki dosyaları cagirir; config AGENTS.md'yi yukler.
cp -r .opencode opencode.json AGENTS.md scripts templates docs <proje>/
chmod +x <proje>/scripts/*.sh <proje>/scripts/*.py
# opencode'u <proje> içinde başlat. Değişiklik sonrası opencode'u yeniden başlat.
```

Ortam: `openrouter` sağlayıcısı (API anahtarı `.env` / `OPENROUTER_API_KEY`).
Kullanılan modeller (bkz. `docs/PIPELINE.md`): claude-sonnet-4 (ana), gemini-2.5-flash,
llama-3.3-70b, gpt-oss-20b.

## 3. Mimari — ajanlar

Varsayılan (primary) ajan: **atlas-orchestrator**. Diğerleri `subagent`.

| Ajan | Model | Görev |
|------|-------|-------|
| atlas-orchestrator | claude-sonnet-4 | Pipeline beyni; tüm fazları koordine eder, çelişkileri kanıt ağırlığıyla çözer, kullanıcıya sunar. Otomatik uygulama/commit YOK. |
| atlas-scoper | claude-sonnet-4 | FAZ0: 30 SCOPE-ID + DEC-REGISTER + tanımlar sözlüğü üretir. Makale yazmaz. |
| atlas-lens-structure | gemini-2.5-flash | FAZ1: yapısal bütünlük (CHK-01..07, tablo/CSV/JSON/link, provenance, fix-manifest). Sadece şekil. JSON döner. |
| atlas-lens-consistency | llama-3.3-70b | FAZ1: sayısal/terminolojik/mantıksal/çapraz-ref/istatistiksel tutarlılık. JSON döner. |
| atlas-lens-editor | claude-sonnet-4 | FAZ1: akademik dil, APA 7, atıf, jargon, intihal, yapı. JSON döner. |
| atlas-writer-master | claude-sonnet-4 | FAZ3: SCOPE + lens + fix girdilerini işleyip MASTER'ı finalize eder. |
| atlas-gate-2a | claude-sonnet-4 | FAZ4: KÖR denetim — sadece MASTER+SCOPE+PROVENANCE okur, FIX-MANIFEST'i ASLA. CHK-01..07. |
| atlas-gate-2b | gpt-oss-20b | FAZ4: manifest doğrulama — her FIX'in kanıtını arar, kanıtsız = P0. |
| atlas-gate (orchestrator) | claude-sonnet-4 | FAZ4: 2A+2B'yi `gate_merge.py` ile birleştirir, 2-of-2 voting. |
| ~~gate-strong / gate-manifest / gate_2~~ | — | DEPRECATED, `disable:true`. Yüklenmez. |

## 4. Pipeline (fazlar)

```
[Kullanıcı: taslak MASTER + A/B kaynak paketleri]
  → FAZ0 /atlas-faz0  → 00-FAZ-0-SCOPE-CONTRACT-ve-REGISTER.md
  → FAZ1 /atlas-faz1  → 01-FAZ-1-LENS-SWARM-DENETIM.md   (3 lens PARALEL, JSON → birleşik liste)
  → FAZ2 /atlas-faz2  → 02-FAZ-2-FIXER-SWARM.md          (kullanıcı FIX seçer, kanıtlı)
  → FAZ3 /atlas-faz3  → 03-FAZ-3-MASTER-v5.5.md          (writer finalize eder)
  → FAZ4 /atlas-gate-2a + /atlas-gate-2b → gate/FINAL-GATE-v5.5.json + 04-FAZ-4-...md
```

**Altın kurallar (orchestrator §7-§8):**
- Her faz sonunda kullanıcıya sun, **onay bekle**. `/atlas-full` KULLANILMAZ (insan denetimini atlar).
- Otomatik `git commit`/`push` YOK. Otomatik FIX uygulama YOK — kullanıcı karar verir.
- Halüsinasyon koruması: "dosyaya yazdım" → `ls -la`/`wc -c` ile doğrula; "FIX uyguladım" → `grep` + alıntı kanıtı.
- DEC-036 (etik) açıkken "yayına hazır" denmez. DEC-035 (Kur'an ayeti) açıkken teolojik iddia kabul edilmez.

## 5. Kavram sözlüğü

- **SCOPE-ID (SC-XXX):** makalenin kapsam kalemleri. SC-001..022 sabit ZORUNLU;
  SC-023..030 esnek (2 ZORUNLU + 6 OPSİYONEL).
- **DEC-XXX (REGISTER):** kararlar. Durum: `OPEN`/`DECIDED`/`SUPERSEDED`.
- **FIX-XXX (MANIFEST):** düzeltmeler; ardışık, kanıtlı, UYGULANMIŞ/UYGULANMAMIŞ.
- **CHK-01..07:** kontrol listesi (bkz. `templates/CHK-CHECKLIST.md`).
- **PROVENANCE:** hangi SCOPE-ID hangi bölüm/kaynak/satırla kapsanıyor tablosu.
- **Severity:** P0 kritik (bloklar), P1 düzeltilmeli, P2 kozmetik.
- **Gate 2-of-2:** 2A (kör) ve 2B (manifest) ikisi de PASS + P0/P1=0 ise FINAL PASS.

## 6. Script'ler (`scripts/`)

| Script | İş |
|--------|-----|
| `check_integrity.sh --faz0..--gate --full` | Dosya var mı, boyut, içerik, JSON geçerliliği. `--full` artık FAZ0..4 + gate zincirini tam çalıştırır (verify_doi + provenance_check dahil). |
| `provenance_check.py` | CHK-01 (ZORUNLU SC-ID MASTER'da BAŞLIK olarak), CHK-02 (PROVENANCE tablosu satır-satır "kapsıyor" doğrulaması), CHK-05 (başlık benzersiz). |
| `verify_doi.py [--require-master]` | `[UNVERIFIED]`/`[DOGRULANMADI]` etiketleri (DEC-027 §8 M1 bölüm-farkındalığıyla) + DOI'leri CrossRef ile doğrular; gerçek HTTP hatası FAIL, ağ hatası WARN. |
| `gate_merge.py 2a.json 2b.json` | 2-of-2 voting; P0/P1'i HAM verilerden bağımsız yeniden hesaplar (agent beyanına güvenmez); `gate/FINAL-GATE-v5.5.json` + bulgu-detaylı rapor üretir. |
| `budget_guard.py [--report]` | $30/ay bütçe takibi (`.atlas_budget.json`); aylık otomatik reset, bozuk dosyada crash etmez. |

## 7. Bu build'de (v5.5.1 → v5.5.2) yapılanlar

Ayrıntı: `docs/AUDIT-v5.5.1.md`, `docs/AUDIT-v5.5.2.md` ve `docs/CHANGELOG-v5.md`. Özet:

**v5.5.1 (1. tur):**
- opencode.json şema-geçerli yapıldı (KRİTİK: eski hali opencode'u başlatmıyordu).
- `default_agent`, `mode`, `instructions` eklendi; deprecated'lar disable edildi.
- `[UNVERIFIED]`/DEC-027 ve CHK-01 sayı tutarsızlıkları giderildi.
- 5 template gerçek iskeletle dolduruldu.
- Pipeline metadata `docs/PIPELINE.md`'ye taşındı.

**v5.5.2 (2. tur — iki bağımsız subagent denetimi sonrası):**
- **P0 (kritik):** `gate_merge.py` artık agent beyanına güvenmiyor, P0/P1'i
  ham verilerden bağımsız yeniden hesaplıyor (sahte PASS artık mümkün değil).
- `verify_doi.py`: DEC-027 bölüm-farkındalığı gerçek uygulandı; DOI HTTP
  hataları artık FAIL sayılıyor; deterministik DOI seçimi.
- `provenance_check.py`: CHK-01/02 sahte-PASS'e karşı sıkılaştırıldı.
- `check_integrity.sh --full/--gate`: artık gerçekten tüm zinciri doğruluyor.
- `budget_guard.py`: crash ve aylık reset hataları giderildi.
- Tüm agent'lara teknik `permission` sınırları eklendi (kör gate, no-commit,
  lens'lerin salt-analiz olması artık PROMPT değil, TEKNİK olarak zorunlu).
- CHK-01..07 şiddet/tanım çakışmaları tek kaynağa göre harmonize edildi.
- DEC-036 mantıksal kilidi bypass mekanizmasıyla çözüldü.
- Kurulum talimatı, command routing (`agent:` pin), `/atlas-verify` rapor
  üretimi, roster sayıları ve çekirdek/alan-özel kontrol ayrımı düzeltildi.

## 8. Açık konular / sonraki AI için karar noktaları

Aşağıdakiler v5.5.2'de KASITLI olarak değiştirilmedi (mimari tercih veya kapsam dışı):

1. **Faz yeniden numaralandırma (opsiyonel).** Denetim aracı yerine "sıfırdan üretim"
   modeli isteniyorsa Writer, Lens'ten önceye alınmalı (Scope→Draft→Lens→Fix→Finalize→Gate).
   Şu an "kullanıcı taslak MASTER sağlar" modeli kullanıcı onayıyla korunuyor.
2. **Model seçimleri.** gpt-oss-20b (gate-2b) ve gemini-flash (structure) maliyet için
   seçilmiş; kalite/maliyet dengesi gözden geçirilebilir (AGENTS.md maliyet tablosu).
3. **Template'ler** iskelet placeholder içerir; gerçek bir çalışmada doldurulur.
4. **Gerçek LLM çıktı kalitesi test edilmedi.** Bu iki denetim turu da config/script/
   mimari doğruluğuna odaklandı; agent promptlarının gerçek model çağrılarıyla
   üretim kalitesi (halüsinasyon oranı, akademik dil kalitesi vb.) ayrı bir
   değerlendirme gerektirir.

## 9. Sürüm geçmişi (özet)

v4.0 (orijinal, 3 lens + gate) → v5 (faz ayrımı denemesi, config kırık) →
v5.1 (v5 ~kopyası) → v5.2 (gate güçlendirme, self-healing) → v5.3 (temizlik, lens regresyonu)
→ v5.4 (merge) → v5.5 (optimize iddiası, config hâlâ kırık) → v5.5.1 (config-fix,
opencode çalışıyor ama P0 güvenlik açığı + çok sayıda P1 vardı) →
**v5.5.2 (P0 güvenlik açığı + 22 P1/P2/P3 bulgusu giderildi, runtime testli).**
