# HANDOFF (2026-11-12, Spinoza Reels sonrası)

## Spinoza: TESLİM EDİLDİ
- Video: `outputs/Spinoza/Spinoza-Reels-9x16.mp4` (2:04, 1080p), `Onizleme-telefon.mp4`, `Spinoza-altyazi.srt`, `Kapak-Reels-9x16.png`, `Yayin-paketi.md`.
- Worktree'de üretildi; ana klasöre yazma engellendiği için kopyası `~/Desktop/Spinoza-teslim/` içinde. Enes `outputs/Spinoza/`'ya sürükleyecek.
- Senaryo: `Spinoza/Spinoza-senaryo.md` (v2, felsefe odaklı, kanca "Havaya fırlattığın bir taş..."). Ses: ElevenLabs eleven_v4 Sercan, tek kayıt, 1865 kredi.
- Müzik: Bach Goldberg Aria (CC0, Musopen). Kapak Canva'da: "Spinoza Reels Kapak" (DAHatj8m0U4).
- Durum dosyası: `Spinoza/STATE.md`. Tekrar render GEREKMEZ (Enes: "bitmiş işe dokunma").

## Kalıcı kararlar (CLAUDE.md'ye işlendi)
1. Her video `cinecode` skill'i + CLAUDE.md adımları.
2. GitHub: ara adımlarda commit/push yok, sadece proje sonunda handoff.
3. Müziği Claude kendisi seçer (CC0/PD), Enes'e sorulmaz.
4. Teslim dosyaları sohbete EKLENMEZ; `~/Shorts - Reels/outputs/<Konu>/`'ya konur, sohbette yol + yayın paketi metni.
5. Görsel/hareket kombinasyonu (hedef ≤1 saat bekleme): Flow/Veo (kilit 4-6 sahne, üyelik kredisi ~20/klip), yerel SDXL (ara görseller), hızlı LTX (kalanlar).
6. Enes'e terminal komutu verilmez; onay gerekiyorsa "izin" istenir ve Claude yapar. Mac'te `claude` CLI YOK.
7. Yeni Reels thread'leri ana klasörde, worktree OLMADAN başlatılmalı (worktree'den ana klasöre yazılamıyor).

## Araçlar
- Flow MCP: `~/flow-mcp` (GTAI-1/flow-mcp, commit 1d17b7b), `~/.claude.json` mcpServers.flow eklendi (yedek: `~/.claude.json.bak-flow`). Google girişi yapıldı (profil `~/.flow-mcp/chrome-profile`). Araçlar yeni oturumda görünür. Tarayıcı otomasyonu; resmi API yok. İş bitince Chrome'u kapat.
- LTX: 0.9.8 distilled 2B + bf16 T5 (`araclar/ltx/t5-bf16`). `_sablon/gorseller/i2v.py` buna göre; 8 adım, 97 kare ~54 sn. Eski ağırlıklar Çöp Sepeti'nde.
- Enes'in LTX hakkındaki yargısı: "reels'e kattığı hiçbir şey yok". Bir sonraki videoda hareketin ağırlığı Flow/Veo'da olmalı; LTX sadece küçük ara hareketler için, sonucu beğenilmezse tamamen bırakılabilir.

## Temizlik
- Çöp Sepeti'nde (Enes boşaltacak): `VoiceStudio-kaldirildi-2026-11-12` (~7,5 GB), `araclar-temizlik-2026-11-12` (~29 GB). araclar 54 GB → 25 GB.
- Spinoza taslak videoları (`Spinoza-Taslak-*.mp4`) worktree outputs'ta, silinmedi.

## Dersler
- Uzun yerel işler `nohup caffeinate` ile çalıştırılmalı; oturum kapanınca LTX durmuştu ve 2 saat kayboldu.
- Bekleme 1 saati aşacaksa önceden söyle, sahneleri Flow'a kaydır.
- Canva'nın AI tasarımı İngilizce/şablonlu çıkıyor: kapağı kodla kur (Anton, tam ekran), Canva'ya yerleştir.
