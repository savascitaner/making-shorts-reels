# HANDOFF: reels dizini

Kısa dizin. Kurallar `CLAUDE.md`'de, her reels'in ayrıntısı kendi `<Konu>/STATE.md`'sinde. Yeni oturum: devam eden reels için "`<Konu>/STATE.md`'den devam et", yeni reels için "yeni reels: <konu>". Eski uzun notlar git geçmişinde (commit `4bb1588` ve öncesi).

## Reels
| Konu | Durum | Not |
|---|---|---|
| Zaman Ötesi Meclis | Teslim edildi 2026-11-16 (2:48, çizgi film) | `Zaman-Otesi-Meclis/STATE.md` |
| Seneca-Nietzsche | İPTAL 2026-11-16 (senaryo v1'de durdu, kredi harcanmadı) | `Seneca-Nietzsche/STATE.md` |
| Marcus Aurelius | Teslim edildi 2026-11-16 (2:56, çizgi film) | `Marcus-Aurelius/STATE.md` |
| Bohr-Einstein, Yunus-Tapduk, Locke-Berkeley, Marx-Feuerbach, Leibniz-Merkez-Efendi, Spinoza, Nietzsche, Hegel, Doğa Filozofları, Diyalektik Materyalizm | Teslim edildi; klasörleri 2026-11-16'da Enes'in isteğiyle silindi | Metin ve kodları git geçmişinde |
| Spinoza-Leibniz | TESLİM EDİLDİ (2026-11-17) | "Sen mi seçtin?" sinematik, 1:52, 4 Veo konuşan klip; ayrıntı `Spinoza-Leibniz/STATE.md` |
- Insanin-Ozu (2026-11-17): uzun 16:9 (7:04) + Reels 9:16 (2:59), "İnsanın bir özü var mı?" sinematik, SDXL + kamu malı portreler, soğan zarı geçişi. TESLİM EDİLDİ. Ayrıntı: `Insanin-Ozu/STATE.md`

## Genel açık işler
- Çöp Sepeti (~36 GB): Enes boşaltacak.

## Ortam (2026-11-16)
- Mac kullanıcı yolu `/Users/claude-eng/`. Eski profil `/Users/claude/` hâlâ duruyor; `uv`, whisper modeli (`/Users/claude/.cache/huggingface`) ve venv-vahdet'in Python'u oradan kullanılıyor.
- node `~/.local/node/bin`, ffmpeg/ffprobe `araclar/audio-video-sync/.venv/lib/python3.12/site-packages/static_ffmpeg/bin/darwin_arm64/` (uret.sh PATH'e ekli).
- Flow: MCP olarak `.mcp.json`, `~/.claude.json` ve masaüstü config'te kayıtlı (2026-11-16); oturumda araçlar görünmezse `./flow.sh` aynı Studio HTTP API'sini sürer (`node dist/studio.js`, port 8787, token `~/.flow-mcp/token`, `/api/status|generate|agent|wait|new_project`). Google oturumu açık.
- Canva: yeni hesap; eski kapaklara erişim yok. Kapak: kodla `kaynak/kapak.html` → Canva'ya tek görsel olarak yükle (Canva AI katmanlara ayırıp Türkçe büyük harfi bozuyor) → kaydet → PNG.
- GitHub: `savascitaner/making-shorts-reels`; push'u Claude yapar (`~/.local/bin/gh`, sapiensdear-tr, `gh auth setup-git`).

## Ses motoru
- `sfx/` (claude-motion sound-design motoru) proje kökünde; `python3 -m sfx --list`. Ayrıntı CLAUDE.md araçlar bölümü.

## Kalıcı dersler
- Veo, Neolitik sahnelere metal murç/saplı çekiç ekliyor ve ağır taşları havaya zıplatıyor: her Veo klibini kare kare kontrol et; gerekirse yalnızca temiz saniyeleri kullan ya da Flow karesi + kodla hareket.
- SDXL özgün arkeolojik nesneleri (T dikilitaş) bilmiyor (Moai, Mısır dikilitaşı, tekerlek, at çiziyor): dikilitaşlı sahneler Flow'da gerçek kareyi referans vererek üretilir.
- Kısmi ses değişikliğinde whisper'ı tüm kayıtta değil yalnızca yeni parçada çalıştır; tümünü yeniden çalıştırmak kelime sayısını kaydırıp kartları yanlış kelimeye düşürdü.
- Üst üste büyük yazılarda alt satırın konturu üst satırın Ç/virgül kuyruğunu örtebilir: satır aralığını kontrol et.
