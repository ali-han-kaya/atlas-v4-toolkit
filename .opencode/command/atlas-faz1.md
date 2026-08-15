---
name: atlas-faz1
description: Atlas v5.5 FAZ1 — Lens Swarm
agent: atlas-orchestrator
---
# /atlas-faz1

1. `wc -c 00-FAZ-0-*.md` — token tahmini: ≤50K SINGLE, >50K PAIRWISE
2. 3 lens paralel:
   - `atlas-lens-structure` (Gemini Flash) → structure JSON
   - `atlas-lens-consistency` (Llama 3.3 70B) → consistency JSON
   - `atlas-lens-editor` (Claude Sonnet 4) → editor JSON
3. Ham JSON'lari al, celişen bulgulari tara (ayni konumda farkli severity)
4. Çelişkileri orchestrator cozer — kanit agirligi, lens cogunlugu DEGIL
5. Birlesik bulgu listesini `01-FAZ-1-LENS-SWARM-DENETIM.md` olarak yaz
6. `bash scripts/check_integrity.sh --faz1`
7. `python3 scripts/budget_guard.py`
8. Bulgulari P0 > P1 > P2 sirasiyla goster, otomatik uygulama YAPMA.
