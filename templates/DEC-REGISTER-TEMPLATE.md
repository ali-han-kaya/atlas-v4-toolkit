# DEC-REGISTER-TEMPLATE — Atlas v5.5

> FAZ0 (atlas-scoper) DEC-REGISTER'ı bu iskeleti temel alır. Durum yalnızca
> `OPEN` | `DECIDED` | `SUPERSEDED`. DECIDED için: karar + gerekçe (≥1 cümle) +
> kaynak + düşünülen ≥1 alternatif. SUPERSEDED: eski→yeni DEC-ID + gerekçe.

## §0.2 DEC-REGISTER

| DEC-ID | Durum | Karar | Gerekçe | Kaynak | Alternatif |
|--------|-------|-------|---------|--------|-----------|
| DEC-001 | DECIDED | RQ netleştirildi | <gerekçe ≥1 cümle> | SCOPE §0.1 | <alternatif> |
| DEC-026 | DECIDED | DEC-036 açıkken FAZ3'e ilerleme onaylandı (bypass) | Etik onay süreci uzun sürebilir; taslak üretimi bekletilmez | Kullanıcı onayı | FAZ3'ü etik onaya kadar durdur |
| DEC-027 | DECIDED | §8 M1 sentetik veri; `[UNVERIFIED]` etiketi kasıtlı | Doğrulanmamış veri şeffaf işaretlenir | PROVENANCE | Veriyi çıkar / gerçek veri bekle |
| DEC-035 | OPEN | QURAN_AYET teolojik iddia | Teolojik çalışmaysa açık; sahibi kullanıcı; FAZ3'ü bloklamaz (istisna) | — | <alternatif> |
| DEC-036 | OPEN | Etik onay bekleniyor | Etik kurul kararı olmadan yayına hazır denemez; FAZ3'ü bloklamaz (istisna, bkz. DEC-026) | — | Onay al / kapsamı daralt |
| DEC-XXX | OPEN\|DECIDED\|SUPERSEDED | <karar> | <gerekçe> | <PROVENANCE / SCOPE> | <alternatif> |

**Kapanış kuralı:** FAZ3, REGISTER'daki tüm kayıtlar `DECIDED`/`SUPERSEDED` ise
başlar. **İSTİSNA:** DEC-036 ve DEC-035, gerçek onay gelene kadar `OPEN`
KALABİLİR ve FAZ3'ü bloklamaz — bunun yerine kullanıcı onayıyla bir bypass
kararı (yukarıdaki `DEC-026` örneği gibi) `DECIDED` edilir. Diğer OPEN'lar
(M2/M4/M1'e bağımlı olanlar dahil) için de aynı bypass deseni kullanılabilir.
DEC-036/DEC-035 kendisi `OPEN` kaldığı sürece FAZ4 gate'i **bilinçli olarak
FAIL** verir — etik/teolojik onay gelene kadar FINAL PASS beklenmez.
