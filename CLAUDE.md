# Shorts - Reels: iş akışı (her video için zorunlu)

Kullanıcı: Enes. Dil: Türkçe. YouTube kanalı: @TanerSavaşçı. Her video `cinecode` skill'i tetiklenerek yapılır, aşağıdaki adımlar onun üstüne eklenir. Her video kendi klasöründe: `/Users/claude-eng/Shorts - Reels/<Konu>/` (araştırma, senaryo, kaynak kod, görseller).
Teslimler (bitmiş video, .srt, Yayin-paketi.md, kaynak listesi, kapak): `/Users/claude-eng/Shorts - Reels/outputs/<Konu>/` (ana klasör, worktree değil). **Büyük mp4 dosyaları sohbete EK OLARAK KONMAZ** (sadece klasör yolu). Metin dosyaları (senaryo, Adim-1-2-3.md, Yayin-paketi.md, .srt) ve küçük dosyalar sohbete eklenebilir/yazılabilir.

## Klasör ve kredi kuralları
- `outputs/` içindeki medya dosyalarını (mp4, wav, mp3, png, jpg) iş yaparken **asla okuma** (Read/görüntüleme yok). QC'yi render sırasında `kaynak/renders/qc` karelerinden yap. Sadece metin dosyalarını okuyabilirsin.
- `araclar/` 12 GB: içinde gezinme, sadece bilinen betikleri çalıştır.
- Az okuma, az adım: her şey `_sablon/` + `./uret.sh` ile yapılır. Tek tek görsele/kareye bakma; sadece `gorseller/ai-sheet.jpg` ve `kaynak/renders/qc-sheet.jpg` toplu görsellerine bak (ayarlarla tekil okumalar kapalı).
- Bir videoya özel olanlar sadece 4 dosya: `video.json` (süre, düzeltmeler, vurgular, boom, QC kareleri), `gorseller/prompts.json`, `kaynak/index.html` (IMG haritası + SH sahne listesi + kartlar), senaryo/ElevenLabs metni.

## Komutlar (`./uret.sh <Konu> <adim>`)
`yeni` → klasörü kur · `gorsel` → SDXL çizimleri + ai-sheet · (ElevenLabs sesi `<Konu>/ses/vo.mp3`) · `hizala` → kelime zamanları + .srt · `ses` → müzik/miks/-14 LUFS · `qc` → qc-sheet · `render` → outputs'a video + telefon önizlemesi · `git` → commit + push

## Oturum (thread) düzeni (Enes, 2026-11-16)
Kredi ve bağlam küçük kalsın diye proje "doküman + thread" yapısında yürür:
- **Proje dokümanı bu dosyadır** (her oturum otomatik okur). Kalıcı kurallar SADECE buraya yazılır; sohbet geçmişine güvenilmez.
- **Her reels = ayrı oturum.** Yeni reels: yeni oturum aç, `./uret.sh <Konu> yeni`, adım 0'dan başla. Aynı oturumda ikinci reels yapılmaz.
- **Durum dosyası `<Konu>/STATE.md`** (şablon `_sablon/STATE.md`): aşama, alınan kararlar (Enes'in sözleriyle), harcanan krediler, açık işler, "Sıradaki adım". Her onay kapısında ve oturum sonunda güncellenir.
- **Devam eden reels:** yeni oturum yalnızca `<Konu>/STATE.md`'yi ve gerekirse senaryoyu okuyarak devam eder ("<Konu>/STATE.md'den devam et"). Eski thread'e dönülmez.
- **Oturum uzarsa** (çok mesaj, büyük görseller): STATE.md'yi güncelle, kalan işi `STATE.md'den devam et` notuyla yeni oturuma devret.
- **Reels bitince:** STATE.md "TESLİM EDİLDİ" olur, `HANDOFF.md` reels dizinine bir satır eklenir, `./uret.sh <Konu> git` (GitHub Desktop ile push), oturum Enes'in onayıyla "tamamlandı" işaretlenir.
- `HANDOFF.md` artık kısa bir dizindir (reels listesi + açık genel işler); ayrıntı her reels'in kendi STATE.md'sindedir.

## Araçlar her oturumda hazır (Enes, 2026-11-16: "her araç her zaman her an kullanılacak gibi yapılandır")
- **Flow MCP** üç yerde kayıtlı: proje `.mcp.json` (+ `.claude/settings.json` enableAllProjectMcpServers), kullanıcı `~/.claude.json` mcpServers, Claude masaüstü `claude_desktop_config.json`. Node: `/Users/claude-eng/.local/node/bin/node`, sunucu `~/flow-mcp/dist/index.js`, Studio 127.0.0.1:8787.
- MCP araçları oturumda görünmüyorsa mazeret yok: **`./flow.sh <metot> '<json>'`** (proje kökü) aynı motoru HTTP'den sürer (status, generate, wait, assets, download, agent, edit, character...). Studio kapalıysa betik kendisi başlatır. Enes'e "yüklü değil" denmez.
- **sfx ses motoru** (sound-design skill'inin motoru, `whaleyxbt/claude-motion`): proje kökünde `sfx/` (saf Python, 48 kHz, -14 LUFS master). `python3 -m sfx --list` üreteçleri gösterir (whoosh, impact, riser, scratch, chime, pad, pop, click...). Reels için cue sheet: `<Konu>/kaynak/cues.py` (TIMELINE yerine words.json zamanları), `python3 -m sfx <Konu>/kaynak/cues.py`. Ses dalgası/ses yüksekliği: `scripts-motion/wave.mjs`, kare panosu: `scripts-motion/sheet.mjs`. Kaynak depo: `araclar/claude-motion` (motion-design, sound-design, review-loop, web-sims skill'lerinin örnekleri burada).
- node/ffmpeg/ffprobe/uv PATH'i `.claude/settings.json` → env.PATH içinde; ayrıca `export PATH` gerekmez.

## Her reels eşsiz (Enes, 2026-11-16: "her reels kendine özeldir, sen eşsiz bir şey yapmalısın")
- **Eski bir reels'in klasörü, motoru, kapağı ya da müziği hiçbir yeni çalışmada açılmaz, örnek alınmaz ve Enes'e anılmaz** (Enes, 2026-11-16: o videonun adını bir daha hiçbir reels çalışmasında duymak/görmek istemiyor). Teknik altyapı yalnızca `_sablon/` ve bu dosyadaki kurallardan gelir.
- Enes'in getirdiği bir taslak eski bir reels'in konusuna/mekânına atıf yapıyorsa o kısım sormadan çıkarılır ve önerilerde, araştırmada, kaynaklarda o konu hiç anılmaz (Enes, 2026-11-16).
- Önceki videonun kartlarını, geçişlerini, efekt katmanlarını, kapanış/kapak düzenini, müzik şablonunu KOPYALAMA. Ortak olan yalnızca zorunlu kurallar (ilk 3 sn kanca, altyazı stili, kapanış bilgileri, -14 LUFS).
- Her videoda konunun kendi nesnesinden doğan bir imza dili kur (geçiş, tipografi, renk, ses motifi) ve bunu `motion-design`, `design-motion-principles`, `sound-design`, `cinecode` (references: motion, camera-moves, finish, motion-design, sound) skill'leriyle tasarla. Motorun teknik altyapısı (kare = zaman fonksiyonu, klip açma, senkron) yeniden kullanılabilir; görünüş ve ses kullanılamaz.

## Konuşan karakter ve teslim (Enes, 2026-11-16, KESİN)
- **Kodla ağız açıp kapatma YASAK** ("bir daha asla böyle ağız açıp kapatarak reels istemiyorum"). Çizgi film olsa bile konuşan karakter Flow/Veo'da gerçekten konuşan klip olarak üretilir. Veo konuşmayı vermiyorsa illüstrasyondan gerçek fotoğraf türetilir ve reels gerçek sinematik videolarla hazırlanır. Ağız biçimi kareleri (kapalı/yarı/açık/o) ve ses zarfıyla ağız sürme hiçbir reels'te kullanılmaz.
- **Mazeret yok:** "hata oldu, ses taştı, şu oldu bu oldu" kabul edilmez. Sorun teslimden önce çözülür; Enes'e sorun anlatılarak iş sunulmaz.
- **Eski reels hiçbir yolla sohbete gelmez:** Canva'da `search-designs`/listeleme ile eski tasarımları açma ya da listeleme (eski kapak küçük resimleri sohbete düşüyor ve kredi harcatıyor); `HANDOFF.md` reels listesini okuma; eski reels adı, görseli, kapağı hiçbir araç çıktısıyla getirilmez. Canva'da yalnız o oturumda oluşturulan tasarımın ID'siyle çalış.

## Yedek
- Bitmiş videolar Google Drive'a YEDEKLENMEZ (Enes istemedi). Sadece GitHub (metin + kod).

## GitHub senkronu
Repo: https://github.com/savascitaner/making-shorts-reels (private). Ara adımlarda commit/push YOK. Sadece proje sonunda (teslimden sonra) tek seferde handoff: `git add -A && git commit && git push`. Medya ve `araclar/` `.gitignore` ile dışarıda. Bilgisayar değişirse: `KURULUM.md`.
Push'u Claude yapar (2026-11-16): `gh` (`~/.local/bin/gh`, hesap sapiensdear-tr, collaborator) git kimlik yardımcısı olarak kurulu; `git push` doğrudan çalışır. Enes'e GitHub Desktop'tan push yaptırılmaz.
Bu adımların hiçbiri atlanmaz ve Enes'e hatırlattırılmaz.

## Adımlar
0. **Stil sorusu (2026-11-14, Enes'in kararı):** Enes reels istediğinde, ADIM 1'den ÖNCE sor: "Sinematik mi, çizgi film (hareketli 2D çizgi sahneler) formatında mı?" Cevaba göre ilerle:
   - **Sinematik:** mevcut akış (gerçek arşiv görselleri + fotogerçekçi AI, Flow/Veo kilit sahneler, kodla hareketli fotoğraf).
   - **Çizgi film stili KALICI (Enes, 2026-11-19):** Arcane'den ilham alan çizgi roman tarzı, görünür yağlı boya fırça dokusu, dramatik chiaroscuro, ultra kalite. Görseller Flow Nano Banana Pro'da (0 kredi). Her reels'in paleti ve imza dili yine konudan doğar ve eşsizdir; kalıcı olan yalnızca bu çizim/doku stilidir.
   - **Çizgi film:** 2D animasyon / çizgi roman tarzı hareketli sahneler; kilit sahneler Flow/Veo'da aynı çizgi stilinde (başlangıç karesi Flow'da çizilir), kalanlar çizgi görsel + hafif hareket (kamera, katman, parçacık). Tüm sahneler tek stil ve tek palet. Videoya özel stil istisnaları (ör. Diyalektik/Spinoza graphic novel) geçerli kalır.
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
   - Kapanış (Enes, 2026-11-16): önce son soru kartı ("Sence ...? Cevabını yorumlara yaz"), sonra "Daha fazlası için takipte kal" + YouTube simgesi @TanerSavaşçı + Instagram @sevgiliinsann + www.sevgiliinsan.com. Adresler SADECE burada.
8. **Kapak**: Enes'in Canva hesabında (Reels 1080x1920), videodaki ana karakter görseliyle. Giriş kapağı vurucu ve tıklatıcı olur: kanca sorusu + konu adı, büyük ve 4:5 güvenli alanda; kapakta ADRES YOK (Enes, 2026-11-16). Önizlemeyi göster, sonra kaydet (commit) ve PNG olarak `outputs/<Konu>/Kapak-Reels-9x16.png`'ye indir.
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

## Bilinen tuzaklar (2026-11-13, Marx-Feuerbach videosundan)
- Gerçek kişi: Enes izleyicinin tanıyacağı yüz istiyor ("kim bu" dedirtme). Gerçek PD fotoğrafı Flow'a referans verip Nano Banana kare üret (ücretsiz, çalışıyor). Ama Veo bu yüzlerin bir kısmını "prominent people" diye reddediyor (kredi düşmez, tekrar denemek işe yaramaz): o zaman konuşan planı yan veya üç çeyrek profilden, çene ve dudak hareketi net görünecek şekilde yeniden üret (gerekirse karakteri fotoğraftan değil tarifle çizdir). Tanınmış kişi mutlaka konuşurken görünmeli (Enes, 2026-11-13: yoksa fotoğraf slaytı olur); arkadan/B-roll en fazla tek replik için son çare.
- Dudak senkronu: konuşan karakter sadece Veo'da tam Türkçe repliği söylerken gösterilir; klibin konuşma aralığı (whisper ile) `klip/<k>/off.txt`'ye yazılır, `index.html` SYNC repliğe eşler. Diğer konuşmalarda dinleyen yüz, ağız kapalı.
- İki ses istenirse: tek kayıt Sercan + diğer karakterin replikleri ayrı tek kayıt, `logs/birlestir.py` ile birleştir; seviye eşitle.
- Reels 3 dk: ses 176 sn'yi geçerse atempo ≤1.05 ile sıkıştır.
- Flow MCP "fetch failed" verirse Studio sunucusu düşmüştür: `cd ~/flow-mcp && nohup node dist/studio.js &` (kuyruk sıfırlanır, işleri yeniden gönder).

## Bilinen tuzaklar (2026-11-13, Locke-Berkeley videosundan)
- Whisper "ikincil/birincil + nitelik" gibi l+n birleşimlerini "ikinci/birinci" diye yazar; ses doğru olabilir. Yeniden kayıt almadan önce kısa parçayı `initial_prompt` ile tekrar transkribe et (gereksiz yama 100 kredi yaktı). Yazımı `duzelt` ile düzelt.
- `birlestir.py` ile kesitte bir karakterin son parçasının sonunu `None` bırak; sabit saniye son kelimeyi ("oldu?") kesti.
- Veo, gerçek portreden üretilmiş Locke/Berkeley yüzlerini önden reddetmedi (6/6 klip geçti). Veo replik başını bazen değiştirir ("Bay Lok" → "Hayır"); SYNC yine oturur.
- Enes birden çok kanca seçeneğini birlikte isteyebilir: biri sesli kanca, diğerleri ekran yazısı ve videonun ortasına sesli ara olarak girer.

## Bilinen tuzaklar (2026-11-13, Yunus-Tapduk videosundan)
- Flow görsel kuyruğu kare başı ~5-7 dk sürdü (insan benzeri bekleme). Önce yalnızca Veo'ya gidecek kareleri kuyruğa al, Veo'yu hemen arkasına koy; ara sahne görsellerini SDXL'e kaydır, Flow'a en fazla 1-2 ek kare.
- `flow_character` bazen `waitForURL` zaman aşımıyla düşüyor; tekrar denemek yerine karakter portresini `type: image` ile üret, sonraki karelerde dosya yolunu `reference_images` olarak ver (tutarlılık iyi çıktı).
- Commons'ta CC0/PD ney kaydı yok; ney müziği `logs/sesler.py` içinde kodla sentezlendi (Hicaz/Uşşak taksim + dem + yaylı).
- Menkıbe karakterleri (gerçek portresi olmayan) için Veo 7/7 klipte Türkçe repliği birebir söyledi, hiç reddetmedi.

## Bilinen tuzaklar (2026-11-16, tarih öncesi video)
- Tarih öncesi sahnelerde Veo metal murç/saplı çekiç ekliyor ve ağır taşları havaya zıplatıyor (Enes iki kez yakaladı). Her Veo klibini kare kare kontrol et; temiz değilse yalnızca temiz saniyeleri kullan ya da Flow karesi + kodla hareket. Promptta aleti açıkça tarif et ("yalnızca elde tutulan yuvarlak taş, keski/murç/sap yok"), fiziği yaz ("taban yuvada kalır, iplerle döndürülerek dikilir").
- SDXL özgün arkeolojik nesneleri (ör. T biçimli dikilitaş) bilmiyor; Moai, Mısır dikilitaşı, tekerlek, at çiziyor. Bu sahneler Flow'da gerçek kareyi `reference_images` vererek üretilir (ücretsiz, ~1 dk). SDXL yalnızca nesnesiz atmosfer (ateş, gökyüzü, buğday, kitap) için.
- Kanca kelimesi döneme uymalı ("ekmek" tarım öncesinde takıldı → "açlık"). Kapak vurucu ve adressiz; adresler yalnızca kapanışta.
- Kısmi ses değişikliğinde whisper'ı yalnızca yeni parçada çalıştır (`logs/kapanis.py` + `kapanis_birlestir.py` kalıbı); tüm kaydı yeniden hizalamak kelime sayısını kaydırıp kartları yanlış kelimeye düşürdü. Kapanış kartlarını kelime numarasıyla değil adıyla bağla (`IDX('Bunu')`).
- Üst üste büyük Anton satırlarında alt satırın konturu üst satırın Ç/virgül kuyruğunu örtebilir; kanca kartını büyük kırpıp kontrol et.
- Metin değişikliği önce yazılı olarak Enes'e onaylatılır, sonra kayıt alınır (Enes: "önce yaz ve bana onaylat").

## Bilinen tuzaklar (2026-11-16, Marcus Aurelius videosundan)
- Flow Veo: gerçek büst/foto referanslı yüz + promptta kişinin adı → "prominent people" reddi (kredi düşmez). Veo promptlarında isim YAZMA ("the bearded old Roman emperor"); aynı kare isimsiz promptla geçti.
- Flow "Target crashed": Flow sekmesi bellek doldu (aynı Flow projesinde iki reels, 60+ görsel, 10+ video, Chrome 6,5 saat açık). Her reels YENİ Flow projesinde üretilir; 20+ işten sonra sekme yenilenir. Çöken işler `./flow.sh retry '{"job_ids":[...]}'` ile geri gelir.
- Veo klibinin sonuna doğru bozulma (alevde harfler, yüz dağılması) olabilir: kare panosuyla bak, `rate`/`off` ile yalnız temiz aralığı kullan.
- Konuşan klipte konuşma başı whisper `vad_filter` ile ölçülür (0.0 dönerse silencedetect ile doğrula); replik plan başından sonra geliyorsa negatif `off` ile ilk kare dondurulur.

## Bilinen tuzaklar (2026-11-16, Spinoza-Leibniz)
- `./flow.sh status` tüm eski işlerin listesini döker (eski reels adları sohbete düşer). Kredi için yalnız şunu çalıştır: `./flow.sh status '{}' | python3 -c "import json,sys;print(json.load(sys.stdin)['flow'])"`.
- `flow_wait` her zaman `job_ids` ile çağrılır; boş çağrı da eski işlerin tamamını döker.

## Bilinen tuzaklar (2026-11-17, Enes'in içerik düzeltmeleri)
- "Men arefe nefsehû fekad arefe Rabbehû": "Kendini **tanıyan** Rabbini **tanır**." "Bilen/bilir" yazılmaz (arefe = tanıdı; bilmek alime'dir).
- Tasavvufta isim (ör. İbn Arabî) yerine ekol adı: "vahdet ehli / vahdet inancına sahip olanlar": her şey o birin görünümü (birlikten kesrete); insanın bir âleme, bir Tanrı'ya bakan yönü vardır.
- Bebek/yavru deneylerini "ahlak, iyiyi tercih" kanıtı olarak sunma (Enes: 3,5-4 yaşa kadar farkındalık yok, bu etki-tepki/korunma). Yale kukla deneyi kullanılmaz.
- Enes fısıltı → sessizlik → sert vuruş kancasından sıkıldı (2026-11-17): premium videolarda ses düz ve dengeli, ani yükselme/düşme yok; kanca gücünü cümleden alır.
- Psikoloji terimi: "bilinçaltı" YAZILMAZ, "bilinçdışı" yazılır (Enes, 2026-11-17: bilimsel literatürde bilinçdışı).

## Dil kuralı (Enes, 2026-11-17)
- Transkript düzeltmesi, senaryo, ses metni, altyazı ve ekran yazılarında cümle yapıları TDK yazım ve dil bilgisi kurallarına uygun yazılır (yazım, noktalama, büyük harf, bitişik/ayrı yazım, devrik/eksik cümle düzeltmesi). Konuşmacının sözü aktarılırken anlam ve üslup korunur, yalnız dil bilgisi düzeltilir.

## Bilinen tuzaklar (2026-11-17, kapak)
- Canva `create-design` yüklenen kapak PNG'sini birebir koymuyor: kendisi yeniden çiziyor, formatı değiştiriyor (Story → 1080x1440) ve Türkçe büyük İ'nin noktasını siliyor ("INSANIN BIR"). Kapak `kaynak/kapak.html` ile kodla tam boyutta üretilip PNG olarak doğrudan `outputs/<Konu>/`ya konur; Canva yalnızca Enes isterse ve yazı kontrolüyle kullanılır.
- Kapanış sırası (Enes): soru kartı → "takipte kal" → temiz kapak (2 sn) → adresler. Kapak görseli adres kartının arkasında; kart kapağın yazısız tarafına konur. Reels kuyruğu 3 dk sınırını aşmasın.

## Bilinen tuzaklar (2026-11-17, telaffuz ve eller)
- Zor isim telaffuzu: önce 3-4 yazımı tek kısa denemede okut (~130 kredi), Enes seçsin, sonra cümleleri kaydet. "Jung" = /juŋ/ (Enes onayladı); "Yung" yazımı "Yang", /jʊŋ/ "Yom" okundu.
- SDXL elleri bozuk çiziyor (fazla parmak, toynak gibi el, bebek parmakları). El görünen her kare Flow Nano Banana'da referanssız, sıfırdan çizilir (`download_quality: upscaled`); eski kareyi referans vermek bozuk pozu kopyalıyor. SDXL yalnız elsiz sahneler için.

## Bilinen tuzaklar (2026-11-18, Jung-Freud: ses ve Flow görsel)
- **Uzun + kısa versiyon = TEK ses kaydı.** Önce uzun metnin tek ana kaydı alınır; kısa versiyon o kayıttan cümle cümle kesilir. Kısa metnin cümleleri uzun metinde BİREBİR yer almalı. Ayrı kısa kayıt ALINMAZ.
- **Kesim noktası whisper zamanından ALINMAZ** (Enes, 2026-11-18: "son harfler yutulmuş"). Whisper kelime zamanları gerçek sesten 0,1-0,7 sn sapıyor; ona göre kesince cümle başları ve son harfler kırpıldı. Cümleyi bulmak için whisper (karakter dizisi eşleştirme, `kaynak/cut916.py`), KESMEK için dalga biçimindeki gerçek sessizlik (−50 dB altı ≥90 ms) kullanılır: başlangıç = önceki sessizliğin sonu, bitiş = sonraki sessizliğin başı + 150 ms, 40 ms yumuşak kenar (`kaynak/cut916b.py`). Kayıt sessizlikle başlamıyorsa ilk cümle 0'dan başlar. Teslimden önce: yeniden whisper → metin senaryoyla harfi harfine aynı mı; her cümle sonunun son 50 ms'i −75 dB altında mı (kırpık son harf −25/−35 dB görünür).
- **Ses tonu:** eleven_v4 + köşeli parantez etiketleri (`[serious]`, `[pause]`, `[curious]`) Enes'in onayladığı tarz (test-b). Duygusal yerler ve vurgular metne baştan işlenir.
- **ElevenLabs MCP zaman aşımına uğrarsa** doğrudan API: anahtar `~/.cinecode/keys.env` (`ELEVENLABS_API_KEY`), `POST /v1/text-to-speech/<voice_id>`, tek istek, tekrar deneme yok. Kota: `GET /v1/user/subscription`.
- **Flow görsel üretimi:** `flow_generate` içinde `type: "image"` ve `model` HER SAHNENİN İÇİNE yazılır (en üst seviyeye yazılırsa yok sayılır, iş video olarak kuyruğa girer ve 20 kredi ister). Her görsel sahneye `max_credits: 0` konur; teklif 0 değilse hiçbir şey üretilmez. Nano Banana Pro görselleri 0 kredi.

## Bilinen tuzaklar (2026-11-18, Enes'in teslim sonrası yakaladığı hatalar)
- Ses parçası birleştirirken (kanca yeniden okuma + eski kayıt) baş KESİLMEZ: yeni parça başındaki sessizlikle birlikte tam konur. Kontrol: `silencedetect` ile birleşmiş dosyanın ilk sesi ≥0,08 sn'de başlamalı ve ilk kelime whisper'da ≥0,3 sn sürmeli; "Annesini 0.0-0.2" gibi kısa ilk kelime = kesik baş demektir. Teslimden önce ilk 2 sn ölçülür.
- Yazı tipi seçmeden önce Türkçe harf testi: `İıŞşĞğÜüÖöÇçÂâ` hem büyük hem küçük harfle tek karede çizilip bakılır. Cinzel (yalnız büyük harf/small-caps) "ı" harfini başka fontla basıyor: KULLANILMAZ. Serif ihtiyacında macOS Baskerville (bold/bold italic) Türkçe tam.
- Ekrandaki kart/damga konuşulan sözün aynısını yazıyorsa o süre boyunca altyazı gizlenir (iki kez yazı, üst üste binme yok). QC kareleri yalnız sahne başlarından değil, HER kartın/damganın/etiketin göründüğü andan da alınır.
- Başlık üstü küçük etiket ile Anton satırı arasında ≥size*1.2 boşluk, satır aralığı size*1.15 (İ noktası ve virgül çakışmasın); etiket ≥52 px ve konturlu.
- Sis/ışık katmanı dikdörtgen bölgeye radyal gradyanla çizilmez (sert şerit kenarı çıkar); elips (scale) ile çizilir.
