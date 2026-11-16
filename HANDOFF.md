# HANDOFF (2026-11-16, yeni profile taşıma)

**Mac kullanıcı yolu artık `/Users/claude-eng/`.** Proje: `/Users/claude-eng/Shorts - Reels`.

## Bu oturumda yapılanlar
- Skill'ler `.claude/skills/` altına kuruldu: `cinecode` (sarpstar, tam kit), `design-motion-principles` (kylezantos), `motion-design`, `sound-design`, `review-loop`, `web-sims` (whaleyxbt/claude-motion; bunlar Remotion depo köküne bağlı, tam çalışmayabilir).
- `araclar/music-video-generator` (ialakey) kuruldu, NumPy+Pillow ile çalışıyor (`python3 -m musicvideo --help`).
- `araclar/audio-video-sync` (sanjeed5) dosyaları kondu. EKSİK: `pip install scipy librosa loguru typer` (bulut oturumunda internet yoktu).
- `mg-styles-15` (Vincentwei1021) Downloads'ta; SKILL.md yok, stil prompt'ları `prompts/` içinde. Gerekirse referans olarak `araclar/` altına alınacak.
- Bohr-Einstein TAMAMLANDI (devam eden iş değil).

## İlk iş (Claude Code'da)
1. ~~`araclar/audio-video-sync` bağımlılıklarını kur~~ YAPILDI (2026-11-16): `araclar/audio-video-sync/.venv/bin/avsync` (Python 3.12 venv). `araclar/remotion-skills` klonlandı, `araclar/mg-styles-15` kopyalandı.
2. `~/Downloads` içindeki açılmış depo klasörlerini (cinecode-main, claude-motion-main, design-motion-principles-main, mg-styles-15-main, music-video-generator-main, audio-video-sync-main) Enes'in onayıyla sil.
3. Büyük ara dosyalar için silme listesi çıkar, Enes'e onaylat: `Hegel/kaynak/tmp`, `Doga-Filozoflari/kaynak/tmp` (~4,5 GB), `*/kaynak/audio/*.wav` stem'leri, `*/kaynak/renders/picture*.mp4`, `.claude/worktrees/` (~1,3 GB). DİKKAT: teslim videoları outputs/'ta yalnızca Bohr-Einstein için var; diğerlerinin tek kopyası tmp/worktree'de olabilir, silmeden önce kontrol et.
4. Göbeklitepe reels'i devam ediyor: senaryo v2 Enes onayı bekliyor (kanca B, sinematik).
5. Açık: Yunus-Tapduk kapak onayı, Çöp Sepeti (~36 GB).

# HANDOFF (2026-11-12, Leibniz-Merkez-Efendi Reels sonrası)

**Yeni adım 0 (2026-11-14):** Yeni reels isteğinde ADIM 1'den önce Enes'e "Sinematik mi, çizgi film (hareketli 2D çizgi sahneler) formatında mı?" diye sorulur; akış cevaba göre ilerler (ayrıntı: CLAUDE.md > Adımlar > 0).

**LTX devre dışı:** `araclar/ltx`, HF önbelleğindeki LTX modeli ve tüm `i2v.py` dosyaları Çöp Sepeti'ne taşındı (`LTX-kaldirildi-2026-11-12`, 8,9 GB; Enes boşaltacak). İleride gerekirse yeniden indirilip tek klip testiyle denenir.

## Leibniz ve Merkez Efendi: TESLİM EDİLDİ
- outputs/Leibniz-Merkez-Efendi/: Reels mp4 (2:06), Onizleme-telefon.mp4, .srt, Kapak PNG, Yayin-paketi.md. Durum: Leibniz-Merkez-Efendi/STATE.md.
- Flow UI değişti: yeni projede sağda ajan paneli açık geliyor, composer'daki "Agent" düğmesini gizliyor ve flow_generate düşüyor. Çözüm: CDP 9333'e bağlanıp paneli "Close" ile kapat (hafızada). ~/flow-mcp kaynağı henüz yamalanmadı.
- LTX (steps 8) bu kez tamamen gürültü üretti; kullanılmadı. Hareket: 5 Veo klibi + kodla kamera/ışık.
- Teslim kuralı güncellendi: sadece büyük mp4 sohbete eklenmez; metin dosyaları eklenebilir.

# Önceki: Spinoza

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
5. Görsel/hareket kombinasyonu (hedef ≤1 saat bekleme): Flow/Veo (kilit 4-6 sahne, üyelik kredisi ~20/klip), yerel SDXL (ara görseller), kalanlar kodla hareketli fotoğraf (LTX 2026-11-12'den beri devre dışı).
6. Enes'e terminal komutu verilmez; onay gerekiyorsa "izin" istenir ve Claude yapar. Mac'te `claude` CLI YOK.
7. Yeni Reels thread'leri ana klasörde, worktree OLMADAN başlatılmalı (worktree'den ana klasöre yazılamıyor).
8. Adım 0 stil sorusu: sinematik mi, çizgi film mi? (2026-11-14)

## Araçlar
- Flow MCP: `~/flow-mcp` (GTAI-1/flow-mcp, commit 1d17b7b), `~/.claude.json` mcpServers.flow eklendi (yedek: `~/.claude.json.bak-flow`). Google girişi yapıldı (profil `~/.flow-mcp/chrome-profile`). Araçlar yeni oturumda görünür. Tarayıcı otomasyonu; resmi API yok. İş bitince Chrome'u kapat.
- LTX: KALDIRILDI 2026-11-12 (Enes). Eski not: 0.9.8 distilled 2B + bf16 T5 (`araclar/ltx/t5-bf16`). `_sablon/gorseller/i2v.py` buna göre; 8 adım, 97 kare ~54 sn. Eski ağırlıklar Çöp Sepeti'nde.
- Enes'in LTX hakkındaki yargısı: "reels'e kattığı hiçbir şey yok". Bir sonraki videoda hareketin ağırlığı Flow/Veo'da olmalı; LTX sadece küçük ara hareketler için, sonucu beğenilmezse tamamen bırakılabilir.

## Temizlik
- Çöp Sepeti'nde (Enes boşaltacak): `VoiceStudio-kaldirildi-2026-11-12` (~7,5 GB), `araclar-temizlik-2026-11-12` (~29 GB). araclar 54 GB → 25 GB.
- Spinoza taslak videoları (`Spinoza-Taslak-*.mp4`) worktree outputs'ta, silinmedi.

## Dersler
- Uzun yerel işler `nohup caffeinate` ile çalıştırılmalı; oturum kapanınca LTX durmuştu ve 2 saat kayboldu.
- Bekleme 1 saati aşacaksa önceden söyle, sahneleri Flow'a kaydır.
- Canva'nın AI tasarımı İngilizce/şablonlu çıkıyor: kapağı kodla kur (Anton, tam ekran), Canva'ya yerleştir.
