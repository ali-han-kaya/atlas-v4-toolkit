# FIX-MANIFEST-TEMPLATE — Atlas v5.5

> FAZ2 (fixer) çıktısı `02-FAZ-2-FIXER-SWARM.md` bu iskeleti temel alır.
> Her FIX-XXX ardışık ve benzersizdir (FIX-001'den). "UYGULANMIŞ" denen her
> FIX'in MASTER'da before→after alıntı kanıtı olmalıdır; kanıtsız = KANITSIZ
> (gate-2b bunu P0 sayar).

## FIX-MANIFEST

| FIX-ID | CHK-Kaynak | Açıklama | Severity | Durum | Kanıt (before→after / bölüm ref) |
|--------|-----------|----------|----------|-------|----------------------------------|
| FIX-001 | CHK-0X | <ne düzeltildi> | P0\|P1\|P2 | UYGULANMIŞ\|UYGULANMAMIŞ | "<önce>" → "<sonra>" (MASTER §X.Y) |
| FIX-002 | CHK-0X | <ne düzeltildi> | P0\|P1\|P2 | UYGULANMIŞ\|UYGULANMAMIŞ | <kanıt> |
| FIX-XXX | ... | ... | ... | ... | ... |

**Onay durumu:** her FIX kullanıcı tarafından `onaylı` veya `ertelendi (gerekçe)`
olarak işaretlenir. Ertelenen FIX'ler `UYGULANMAMIŞ` kalır ve gerekçesi yazılır.
