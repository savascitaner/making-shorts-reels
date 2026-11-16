# Göbeklitepe: durum

**Aşama:** TESLİM EDİLDİ
**Son güncelleme:** 2026-11-16 akşam

## Sıradaki adım
TESLİM EDİLDİ (2026-11-16 17:08). Kalan: Enes'in telefonda izleyip dinlemesi (0:00-0:04 kanca, ~0:13.6 "Göbekli Tepe" darbesi, ~0:44-0:58 ip/taş sesleri, son 18 sn kapanış) ve GitHub Desktop'tan push. Not gelirse bu dosyadan devam.

## Kararlar (Enes)
- Stil: sinematik, ultra gerçekçi. Kilit sahneler Sapiens'in inşaatı.
- Kanca (2026-11-16): "Önce açlık mı geldi... yoksa Tanrı mı?" ("ekmek" tarım öncesi akla takıldığı için değişti). İlk cümle yeniden kaydedildi.
- Vurgu: tarla, yazı, metal ve YERLEŞİK DÜZEN YOK (damga kartları).
- Aletler: Neolitik, YALNIZCA taşla taşa vurma. Metal, murç, keski, saplı çekiç YOK. Veo bunları kendiliğinden ekliyor; Veo kliplerini mutlaka kare kare kontrol et.
- Dikilitaş dikme: yan yatan taş tabanı yuvada kalarak iplerle döndürülerek dikilir; havaya kalkmaz/zıplamaz.
- Kapak: vurucu, ADRESSİZ. "11.500 YIL ÖNCE / ÖNCE AÇLIK MI, TANRI MI? / GÖBEKLİTEPE / TARİHİ TERSİNE ÇEVİREN TEPE", arka plan Sapiens dikilitaş dikiyor (seçenek A). Canva: "Göbeklitepe Reels kapağı" (DAHbFQLP1-k), kaydedildi, PNG outputs'ta.
- Kapanış metni (Enes onayladı): "Sence neden yaptılar? Düşüncelerini ve varsa sorularını yorumlara yaz. Cevap, bugün pek çok yerde dile getirilenlerden biri mi? Yoksa Murat Avcıoğlu'nun bu soruya nitelikçe farklı bir temellendirmesi mi var? Bunu öğrenmek istiyorsan, Avcıoğlu'nu ve bu kanalı takip etmeyi unutma."
- Adresler yalnızca kapanış ekranında.
- Videolar: `videos/` içindeki iki video Enes'e göre kamu malı/telifsiz.

## Dosyalar
- Senaryo: `Gobeklitepe-senaryo-v2.md` (güncel metin)
- Ses: `ses/vo.mp3` (~2:31) = ana kayıt + yeni kanca (`kanca-aclik.mp3`) + yeni kapanış (`kapanis.mp3`). Yedekler: `vo-v1.mp3` (ilk), `vo-v2.mp3` (kanca sonrası).
- Görseller: SDXL `gorseller/ai/` (yalnızca kitap, ateş, Samanyolu, köy, buğday, ocak vb.), Flow `gorseller/flow/` (v3: düzeltilmiş dikilitaşlı sahneler; v4: taşla taşa vurma; v5: fiziksel dikme), Veo `gorseller/veo/` (kullanılan: avcılar scene-03, meşale scene-04; kullanılmayan: metal aletli/zıplayan klipler), gerçek kareler `gorseller/klip/`, arşiv `gorseller/arsiv/` (Commons, CC BY-SA).
- Motor: `kaynak/index.html` (çekimler kelime numarasına bağlı; kapanış IDX ile kelime adına bağlı) · Kapak: `kaynak/kapak.html` · Lisanslar: `LICENSES.csv`
- Yardımcı betikler: `logs/zaman.py` (video.json zamanları), `logs/kanca.py`, `logs/kapanis.py`, `logs/kapanis_birlestir.py`
- Araçlar: ffmpeg/ffprobe `araclar/audio-video-sync/.venv/.../static_ffmpeg/bin/darwin_arm64/` (uret.sh PATH'e ekli), node `~/.local/node/bin`, uv `/Users/claude/.local/bin`, Flow Studio `~/flow-mcp` (`node dist/studio.js`, port 8787, token `~/.flow-mcp/token`, Flow projesi "Gobeklitepe Reels").

## Krediler
- ElevenLabs: 1918 (ana) + 38 (kanca) + 279 (kapanış) = 2235
- Veo 3.1 Fast: 120 (6 klip; 2'si kullanılıyor) · Flow Nano Banana görseller: 0

## Açık işler
- [x] Render, QC, teslim (2:35)
- [ ] Git commit (push GitHub Desktop)

## Teslim
- `outputs/Gobeklitepe/`: Gobeklitepe-Reels-9x16.mp4, Onizleme-telefon.mp4, Gobeklitepe-altyazi.srt, Kapak-Reels-9x16.png, Yayin-paketi.md
