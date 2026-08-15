# Atlas v5.5 — Agent Roster

## Ajanlar (9 calisan + 3 deprecated)

| Agent | Model | Rol | Dosya |
|-------|-------|-----|-------|
| **Orchestrator** | Claude Sonnet 4 | Pipeline beyni, tum FAZ'leri koordine eder | `atlas-orchestrator.md` |
| **Scoper** | Claude Sonnet 4 | FAZ0 — kapsam sozlesmesi, 30 SCOPE-ID, DEC-REGISTER | `atlas-scoper.md` |
| **Writer Master** | Claude Sonnet 4 | FAZ3 — MASTER belgesini yazar | `atlas-writer-master.md` |
| **Structure Lens** | Gemini 2.5 Flash | FAZ1 — yapisal butunluk, CHK-01..07, tablo/CSV/JSON | `atlas-lens-structure.md` |
| **Consistency Lens** | Llama 3.3 70B | FAZ1 — sayisal/terminolojik/mantiksal/istatistiksel tutarlilik | `atlas-lens-consistency.md` |
| **Editor Lens** | Claude Sonnet 4 | FAZ1 — akademik dil, APA 7, atif, jargon, intihal | `atlas-lens-editor.md` |
| **Gate 2A** | Claude Sonnet 4 | FAZ4 — kor denetim, FIX gormez, CHK-01..07 | `atlas-gate-2a.md` |
| **Gate 2B** | GPT-OSS 20B | FAZ4 — manifest dogrulama, FIX kanit arar | `atlas-gate-2b.md` |
| **Gate Orchestrator** | Claude Sonnet 4 | FAZ4 — 2A+2B birlestirir, 2-of-2 voting | `atlas-gate.md` |
| Gate Strong Wrapper | — | atlas-gate-2a yonlendirici (DEPRECATED, `disable: true`) | `atlas-gate-strong.md` |
| Gate Manifest Wrapper | — | atlas-gate-2b yonlendirici (DEPRECATED, `disable: true`) | `atlas-gate-manifest.md` |
| Gate Legacy | — | v4.0 uyumlulugu (DEPRECATED, `disable: true`) | `atlas-gate_2.md` |

**Not:** Varsayilan (primary) ajan `atlas-orchestrator` (opencode.json `default_agent`).
Diger calisan ajanlar `mode: subagent`. Deprecated 3 wrapper `disable: true` — yuklenmez.
Model→rol eslemesi ve faz haritasi icin `docs/PIPELINE.md`.

## Model Maliyet Tablosu

| Model | Rol | Cost |
|-------|-----|------|
| Claude Sonnet 4 | Orchestrator, Scoper, Writer, Editor, Gate 2A | $$$ |
| Gemini 2.5 Flash | Structure Lens | $ |
| Llama 3.3 70B | Consistency Lens | $$ |
| GPT-OSS 20B | Gate 2B | $ |