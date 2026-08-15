# Atlas v5.5 — Pipeline Haritası

> Bu belge, önceki sürümlerde `opencode.json` içine (şema-dışı olarak) gömülen
> `version` / `description` / `pipeline` / model→rol eşleme bilgisini taşır.
> opencode `Config` şeması `additionalProperties: false` olduğu için bu alanlar
> `opencode.json`'da bulunamaz (yoksa opencode `ConfigInvalidError` ile başlamaz).
> Bilgi buraya taşındı; makine tarafından okunmaz, yalnızca referanstır.

- **version:** v5.5.2 (guvenlik + tutarlilik sikilastirma build; pipeline artefakt token'ı `v5.5` olarak korunur)
- **description:** Atlas Akademik v5.5 — çok-ajanlı makale yazım/denetim pipeline (sinirbilim/felsefe/teoloji/bilişsel)

## Model → Rol Eşlemesi

| Model | Roller |
|-------|--------|
| `openrouter/anthropic/claude-sonnet-4` | orchestrator, scoper, writer-master, editor-lens, gate-2a, gate-orchestrator |
| `openrouter/google/gemini-2.5-flash` | structure-lens |
| `openrouter/meta-llama/llama-3.3-70b-instruct` | consistency-lens |
| `openrouter/openai/gpt-oss-20b` | gate-2b |

## Faz Haritası

| Faz | Ajan(lar) | Model(ler) | Komut | Mod | Çıktı |
|-----|-----------|-----------|-------|-----|-------|
| FAZ0 | atlas-scoper | claude-sonnet-4 | `/atlas-faz0` | — | `00-FAZ-0-SCOPE-CONTRACT-ve-REGISTER.md` |
| FAZ1 | atlas-lens-structure + atlas-lens-consistency + atlas-lens-editor | gemini-flash + llama-3.3-70b + claude-sonnet-4 | `/atlas-faz1` | PARALLEL | `01-FAZ-1-LENS-SWARM-DENETIM.md` |
| FAZ2 | orchestrator (fixer) | claude-sonnet-4 | `/atlas-faz2` | — | `02-FAZ-2-FIXER-SWARM.md` |
| FAZ3 | atlas-writer-master | claude-sonnet-4 | `/atlas-faz3` | — | `03-FAZ-3-MASTER-v5.5.md` |
| FAZ4 | atlas-gate-2a + atlas-gate-2b + gate_merge.py | claude-sonnet-4 + gpt-oss-20b | `/atlas-gate-2a`, `/atlas-gate-2b` | 2-of-2 voting | `gate/FINAL-GATE-v5.5.json`, `04-FAZ-4-STRONG-GATE-RAPORU-v5.5.md` |

## Girdi Modeli (önemli)

Atlas bir **denetim + sertleştirme** aracıdır. FAZ1 lens'leri `MASTER.md`'yi
denetler; bu nedenle pipeline'a girmeden önce **kullanıcı bir taslak MASTER
sağlar** (veya elindeki A/B kaynak paketlerinden bir taslak üretir). Akış:

```
[Kullanıcı taslak MASTER + A/B kaynak paketleri]
   → FAZ0 (scope sözleşmesi)
   → FAZ1 (3 lens taslağı denetler, paralel)
   → FAZ2 (fixer: seçilen P0/P1 düzeltmeleri, kullanıcı onayıyla)
   → FAZ3 (writer: düzeltmeleri işleyip MASTER'ı finalize eder)
   → FAZ4 (2-of-2 gate)
```

Her faz sonunda kullanıcı onayı zorunludur. `/atlas-full` KULLANILMAZ.

## Çekirdek vs Alan-Özel Kontroller (P1-13)

CHK-01/02/04/05 gibi kontroller **çekirdek** (her çalışmada geçerli). Ancak
aşağıdakiler bu Atlas kurulumunun **örnek/alan-özel profilinden** gelir ve
farklı bir çalışma için scoper/lens-consistency/gate ajanlarında uyarlanmalıdır:

- **CHK-06 (chi-square tutarlılığı):** yalnızca χ² istatistiği kullanan
  çalışmalar için anlamlıdır. Farklı istatistiksel yöntem kullanan bir
  çalışmada bu check'in ölçütü (lens-consistency §5) o yönteme göre
  yeniden yazılmalıdır.
- **DEC-027 / §8 M1 (sentetik veri istisnası):** belirli bir çalışmanın
  sentetik-veri kararıdır; her çalışmada M1/§8 bölümü olmayabilir.
- **DEC-035 (QURAN_AYET) / DEC-036 (etik-teoloji):** teolojik alan içeren
  çalışmalara özgüdür; sinirbilim-only bir çalışmada gereksizdir.
- **SC-006 [YENİ] / CHK-07:** örnek çalışmanın kasıtlı istisna deseni.

**Yeni bir çalışma için:** scoper'ın SC-023..SC-030 esnek slotlarını
kullanarak alan-özel gereksinimleri tanımla; lens-consistency §5'i
kullanılan istatistiksel yönteme göre uyarla; DEC-035/036 gibi alan-özel
DEC'leri çalışmanın gerçek etik/teolojik durumuna göre ekle veya çıkar.
