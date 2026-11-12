# Shorts - Reels: iş akışı (her video için zorunlu)

Kullanıcı: Enes. Dil: Türkçe. YouTube kanalı: @TanerSavaşçı. Her video `cinecode` skill'i tetiklenerek yapılır, aşağıdaki adımlar onun üstüne eklenir. Her video kendi klasöründe: `/Users/claude/Shorts - Reels/<Konu>/` (araştırma, senaryo, kaynak kod, görseller).
Teslimler (bitmiş video, .srt, Yayin-paketi.md, kaynak listesi, kapak): `/Users/claude/Shorts - Reels/outputs/<Konu>/` (ana klasör, worktree değil). **Büyük mp4 dosyaları sohbete EK OLARAK KONMAZ** (sadece klasör yolu). Metin dosyaları (senaryo, Adim-1-2-3.md, Yayin-paketi.md, .srt) ve küçük dosyalar sohbete eklenebilir/yazılabilir.

## Klasör ve kredi kuralları
- `outputs/` içindeki medya dosyalarını (mp4, wav, mp3, png, jpg) iş yaparken **asla okuma** (Read/görüntüleme yok). QC'yi render sırasında `kaynak/renders/qc` karelerinden yap. Sadece metin dosyalarını okuyabilirsin.
- `araclar/` 12 GB: içinde gezinme, sadece bilinen betikleri çalıştır.
- Az okuma, az adım: her şey `_sablon/` + `./uret.sh` ile yapılır. Tek tek görsele/kareye bakma; sadece `gorseller/ai-sheet.jpg` ve `kaynak/renders/qc-sheet.jpg` toplu görsellerine bak (ayarlarla tekil okumalar kapalı).
- Bir videoya özel olanlar sadece 4 dosya: `video.json` (süre, düzeltmeler, vurgular, boom, QC kareleri), `gorseller/prompts.json`, `kaynak/index.html` (IMG haritası + SH sahne listesi + kartlar), senaryo/ElevenLabs metni.

## Komutlar (`./uret.sh <Konu> <adim>`)
`yeni` → klasörü kur · `gorsel` → SDXL çizimleri + ai-sheet · (ElevenLabs sesi `<Konu>/ses/vo.mp3`) · `hizala` → kelime zamanları + .srt · `ses` → müzik/miks/-14 LUFS · `qc` → qc-sheet · `render` → outputs'a video + telefon önizlemesi · `git` → commit + push

## Yedek
- Bitmiş videolar Google Drive'a YEDEKLENMEZ (Enes istemedi). Sadece GitHub (metin + kod).

## GitHub senkronu
Repo: https://github.com/savascitaner/making-shorts-reels (private). Ara adımlarda commit/push YOK. Sadece proje sonunda (teslimden sonra) tek seferde handoff: `git add -A && git commit && git push`. Medya ve `araclar/` `.gitignore` ile dışarıda. Bilgisayar değişirse: `KURULUM.md`.
Bu adımların hiçbiri atlanmaz ve Enes'e hatırlattırılmaz.

## Adımlar
1. **Araştırma** (konunun en ilgi çeken kavramları, kaynaklar)
2. **Rakip analizi** (Türkçe ve İngilizce, tutan kanca kalıpları, boşluk)
3. **Fikirler ve kancalar** (3-4 fikir, öneri). 1-3'ü `Adim-1-2-3.md` dosyasına yaz, Enes'e sun. **Fikir seçimini bekle.**
4. **Senaryo** (`<Konu>-senaryo.md`). Kanca senaryodan önce yazılır ve çok vurucu olur, ses tonuyla da (fısıltı → sessizlik → sert vuruş gibi). **Onay bekle.**
5. **Ses**: ElevenLabs yalnızca ses için. Sercan Esen (voice_id `dLAxUPEUCZ9cz4KHisnL`), model eleven_v4, tek kayıt (generations_count 1), önce estimate. ElevenLabs'te görsel/video üretme.
6. **Görseller ve hareket (Flow/Veo + SDXL + kodla hareket, hedef toplam ≤1 saat)**:
   - **Flow / Veo** (Enes'in Google AI üyeliği, `flow` MCP, `~/flow-mcp`; ek ücret yok): en çok hareket isteyen 4-6 kilit sahne (yürüyen, konuşan, oturup kalkan karakter). Veo 3.1 Fast ~20 kredi/klip; önce fiyatı oku, video başına ~100 kredi sınırı. Görsellerin bir kısmı da Flow'un ücretsiz görsel üretiminden. Tarayıcı sadece üretim sırasında açık; iş bitince kapat.
   - **Görsel dağılımı (Enes, 2026-11-12):** karakterler ve Veo'ya gidecek kareler Flow'da (Nano Banana, ücretsiz, kare başı ~2-3 dk); mekân, nesne ve atmosfer görsellerinin hepsi yerel SDXL'de (`araclar/sd`, ~1 dk/görsel). Kaliteye göre denge sonradan kaydırılabilir.
   - **LTX devre dışı (2026-11-12, Enes'in kararı):** ağırlıklar ve `i2v.py` silindi (Çöp Sepeti: `LTX-kaldirildi-2026-11-12`). Hareket = Veo kilit sahneler + kalan sahnelerde kodla kamera/ışık/parçacık hareketli fotoğraf. İleride gerekirse LTX-Video yeniden indirilip önce tek klip test edilir (Spinoza'da 30 adımla çalıştı, 8 adımlık distilled ayar gürültü verdi).
   - Gerçek lisanslı foto/gravür de kullanılabilir. Stil: Enes'in o videoda verdiği; vermediyse photoreal.
   - Bekleme 1 saati aşacaksa sahneler Flow'a kaydırılır; Enes saatlerce bekletilmez.

7. **Kurgu (cinecode)**: canvas motoru `kaynak/index.html` (örnek: `Diyalektik-Materyalizm/kaynak`), `capture.mjs --video`, müzik kodla, `master_audio.py` ile -14 LUFS.
   - İlk 0-3 sn büyük kanca yazısı (Anton), altyazı o sırada gizli.
   - Altyazı: Nietzsche videosundaki stil. Şerit/kutu YOK; harflerin etrafında kalın koyu kontur + yumuşak gölge (silüet). Okunan kelime altın renk ve bir tık büyük, diğerleri krem. Ekranın orta-altında (y≈1340). Şablonda hazır.
   - Kapanış ekranı: "Daha fazlası için takipte kal" + YouTube simgesi + @TanerSavaşçı.
8. **Kapak**: Enes'in Canva hesabında (Reels 1080x1920), videodaki ana karakter görseliyle. Önizlemeyi göster, sonra kaydet (commit) ve PNG olarak `outputs/<Konu>/Kapak-Reels-9x16.png`'ye indir.
9. **Yayın paketi**: `outputs/<Konu>/Yayin-paketi.md`: 5 başlık, kaynaklı açıklama, YouTube etiketleri, 18 hashtag, yayın öncesi kontrol listesi. Video ile birlikte, istenmeden teslim edilir.
10. **QC ve teslim**: ilk 15 sn ve her sahneden kare, başı/sonu dinle, süre ≤3 dk (Reels). Tam dosya 20 MB'tan büyükse telefona 720p önizleme de gönder.

## Bilinen tuzaklar ve kalıplar (2026-11-12, Leibniz videosundan)
- Flow: yeni projede sağda ajan paneli açık gelir ve `flow_generate` "Agent" düğmesini bulamayıp düşer. Üretimden önce CDP (127.0.0.1:9333, `~/flow-mcp/node_modules/playwright-core`) ile paneldeki "Close" düğmesine bas. İlk işte tek kareyle dene, sonra topluca kuyruğa al. Flow'un kendi bekleme süresi var: kare başına ~2-3 dk, Veo klibi ~3-4 dk.
- Kilit sahne akışı: önce Flow'da ücretsiz Nano Banana kareleri, sonra o kareler `first_frame` olarak Veo 3.1 Fast'e verilir (5 klip = 100 kredi). Veo klibi `fps=24` karelere açılıp `gorseller/klip/<ad>/` + `n.txt` + `done` olarak konur.
- Müzik: CC0/PD kaydı Claude seçer (ör. Musopen, Wikimedia). `logs/sesler.py` ile müzik, ambiyans ve efekt üretilir, sonra mixdown ve master yapılır.
- Kapak: `kaynak/kapak.html` ile kodla kurulur (Anton, videonun ana karakterleri). Canva'ya `create-upload-url` ile yüklenir, önceki kapak `copy-design` ile kopyalanıp görseli `update_fill` ile değiştirilir, kaydedilir ve PNG olarak dışa aktarılır.
- Ses metninde zor isimler IPA ile yazılır (ör. Leibniz `/ˈlaɪbnɪts/`). Altyazıdaki yazım `video.json` → `duzelt` ile düzeltilir.
- Sohbete sadece büyük mp4 dosyaları eklenmez. Senaryo, ses (mp3), yayın paketi ve .srt eklenir.

Kredi kıt: en az adım, tek ses kaydı, yeniden render'ı önlemek için ilk seferde eksiksiz yap.
