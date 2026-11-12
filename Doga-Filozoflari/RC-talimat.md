# Doğa Filozofları: Mac'te tam üretim (Hegel akışının aynısı)

Klasör: `/Users/claude/Shorts - Reels/Doga-Filozoflari/`. Örnek boru hattı: `../Hegel/kaynak/` (build.py, align.py, transcribe.py, gen_ai.py, covers.py, qc_frames.sh, qc_last.py, fonts). Bunları `kaynak/` altına kopyala ve bu videoya uyarla.

1. **Ses**: `ses/` klasörüne indir (Mac ağı elevenlabsusercontent'e erişir):
   - Parça 1: https://elevenlabsusercontent.com/database/workspace/4e60649e8a674ccd83f99a3c6b40d704/content_generation/p70OZcwPyitYt3ke652u/IyuyT7WnO7DGfkgN6PPh/content.mp3?Expires=1794002400&KeyName=assets-cdn-key-1&Signature=LQn1AFAsH0tmO7NkNPPAVY6r13w= (225 sn)
   - Parça 2: https://elevenlabsusercontent.com/database/workspace/4e60649e8a674ccd83f99a3c6b40d704/content_generation/D1Gwmd8HvMBgP2HTZf8N/xFNdz5rmsBsV7UE1Mqok/content.mp3?Expires=1794002400&KeyName=assets-cdn-key-1&Signature=sys9s2LNMNtv-ZvIo3Hrzib-dAQ= (188 sn)
   Araya 0,6 sn sessizlik koyarak `ses/Doga-tam.wav` yap.
2. **Hizalama**: faster-whisper ile kelime zamanları; metin kaynağı `Doga-Filozoflari-senaryo.md` (bölüm 0-8; sec/par/sent alanlarıyla words.json). Seslendirmede okunuş için yazılanlar altyazıda senaryodaki gibi görünsün: Tales→Thales, Milet→Miletos, Anaksimandros→Anaximandros, Anaksimenes→Anaximenes, apeyron→apeiron, arke→arkhe, Ahilleus→Akhilleus, Lökippos→Leukippos, Con Dolton→John Dalton, "Milattan önce beş yüz seksen beş, yirmi sekiz Mayıs"→"MÖ 585, 28 Mayıs", "Bin sekiz yüz üçte"→"1803'te". Son kelimeyi ("ne?") Whisper ile doğrula.
3. **Görseller**: `./gorselleri-indir.command` çalıştır (Commons, yavaş indirme). Her sahne için en iyi görseli seç → `gorseller/secilen/`. Senaryodaki _Görsel_ notlarını izle. Aynı eserin farklı varyantlarını karıştırma. Küçükleri 4x büyüt. Eksikler için yerel SDXL ile en fazla 3 AI illüstrasyon (zaman sınırı koy): (a) Thales gece yıldızlara bakarken kuyuya düşüyor, hizmetçi kız gülüyor, antik Miletos, yağlı boya; (b) MÖ 585 savaş alanında güneş tutulması, iki antik ordu duruyor, yağlı boya; (c) Empedokles Etna kraterinin kenarında, gece, yağlı boya. Kodla figür çizimi yok; 3D yalnız geçişlerde (su/buz/buhar, dört element, atom ve boşluk) isteğe bağlı.
4. **Kurgu** (build.py uyarlaması): Ken Burns + xfade, senkron altyazı (siyah bant/gradyan YOK, ince kenar + hafif gölge), bölüm başında büyük "TEZ / ANTİTEZ / SENTEZ" kinetik yazı kartı, CC0 müzik (Hegel'deki Goldberg 25 veya Spinoza/build/music'ten başka CC0) konuşmada ducking, cinecode master_audio ile -14 LUFS. "Sevgili İnsan" imzası YOK. Kanca ilk saniyede.
   Çıktılar `teslim/`:
   - `Doga-Filozoflari-16x9.mp4` (1920x1080): bölüm 0-8.
   - `Doga-Filozoflari-Reels-9x16.mp4` (1080x1920, ≤3 dk): bölüm 0 + 4 + 5 + 7 + bölüm 8'in son iki cümlesi. 3:00'ı aşarsa önce bölüm 5'teki Zenon cümlesini, sonra bölüm 7'deki Demokritos alıntısını çıkar.
   - `Shorts-1-tutulma.mp4`: bölüm 0 + 2. `Shorts-2-nehir.mp4`: bölüm 4 + 5 (≤60 sn olacak şekilde: 4'ün "Aynı nehre"den sonu + 5'in ilk 3 ve son 2 cümlesi). `Shorts-3-atom.mp4`: bölüm 7. `Shorts-4-etna.mp4`: bölüm 6. Hepsi ≤60 sn; aşarsa cümle bazında kırp.
   - Her video için .srt. Dikeyde yatay tablo bulanık arka planın ortasına.
5. **Kapaklar**: `Kapak-16x9-A/B.png` (1280x720) ve `Kapak-9x16-A/B.png` (1080x1920), vurucu font, imza yok. Başlık önerileri: "EVREN NEYDEN YAPILDI?", "2600 YILLIK KAVGA". Görsel: Atina Okulu detayı veya Herakleitos/Demokritos çifti.
6. **QC**: her videodan kareler al (altyazı okunur mu, bant yok mu, görsel tutarlı mı), son kelimeyi kontrol et, süreleri yaz. `KAYNAKLAR-VE-LISANSLAR.md` (gorseller/LISTE.txt'ten) teslim/'e.
7. Bitince kısa rapor: dosya listesi, süreler, sorunlar.
