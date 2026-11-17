# Insanin-Ozu: durum

**Aşama:** TESLİM EDİLDİ (2026-11-17)
**Son güncelleme:** 2026-11-17

## Sıradaki adım
Teslim edildi (ikinci tur, 2026-11-17). Oturum Enes'in onayıyla tamamlandı işaretlenecek.
Canva: create-design PNG'yi yeniden çizdi (3:4, İ noktası yok) → teslimde kodla üretilen kapak PNG'leri kullanıldı.
Yapılanlar (2026-11-17): 83 SDXL karesi kontrol edildi; h03 (palmiye çıkmıştı) tohum 293, h02 dikey tohum 192 ile yeniden (`SEEDT` haritası index.html'de). Zıtlık kartına koyu zemin. Kapanış: "takipte kal" kartı → temiz kapak (gorseller/kapak-w|t.jpg) → adresler; uzun +5,6 sn (424,5 sn), Reels +3,5 sn (179,9 sn ≤ 3 dk). Ses yeniden miks + master (-14 LUFS).

## Kararlar (Enes)
- Konu: "İnsanın bir doğası, özü var mıdır?" Bilim ne demiş, felsefe ne demiş, mistikler ne demiş. Mistikler = yalnız tasavvuf değil, doğu anlayışı da (2026-11-17).
- Biçim: 5-7 dk 16:9 uzun video + içinden kısaltılmış 3 dk 9:16 Reels (2026-11-17).
- Stil: sinematik. "Kredimiz kalmadı... ağız hareketiyle konuşturacak bir video istemiyorum." Veo/konuşan klip yok. Yerelde üretilen çok kaliteli görseller, illüstrasyonlar, gerçek fotoğraflar. "Önemli olan içerik çok güçlü olsun, görsel çok güçlü olsun." (2026-11-17)
- "Stoacıları da ekle." (2026-11-17) Epiktetos, Zenon, Khrysippos felsefe bölümünde.
- Mistik gelenekler (itiraz gelmedi): tasavvuf, Budizm, Vedanta, Taoizm (+ Zen, Eckhart).
- Fikir: 1 "Soğan" (Peer Gynt). "Fikir A üzerinden yürüyebiliriz." (2026-11-17)
- Ses tonu: "fısıltılı giriş filan istemiyorum... aniden yükselen, aniden düşen ses kullanmanı istemiyorum bu videoda... çok güzel, çok premium bir video olsun." Seste ve miksajda ani dinamik sıçrama/boom yok.
- Görseller: "Kamuda bulduğum bütün görseller çözünürlüğü küçükse, kötüyse birebir aynalarını yapay zekada yarat. Ultra yüksek kalitede olsun."
- Düzeltmeler (2026-11-17): "Kendini tanıyan Rabbini tanır" (bilen değil); bebek deneyi çıktı; İbn Arabî adı yok, "vahdet ehli" + insanın âleme ve Tanrı'ya bakan iki yönü.
- Eklemeler (2026-11-17): çöp DNA → ENCODE 2012 ("galiba çöp değilmiş"); psikologlar Freud, Adler, Lacan, Jung (ayrı bölüm). Yer açmak için Mencius/Xunzi, antropologlar, Zen koanı çıktı.
- Senaryo onaylandı (2026-11-17). "Ultra gerçekçi görseller, çok iyi ses tonlaması... altyazının arkasında rahat okunması için ince siyah bir arka alan... fısıltılı bağırmalı çağırmalı olmadan güçlü vurgularla... çok kaliteli görsel cümbüşlü bir proje... video ve reel için yayın paketi içeriğini de daha güçlü yap: açıklama, tagler, etiketler." Bu videoda altyazı: ince siyah yarı saydam şerit üstünde.
- "Local AI ile üreteceğin ultra yüksek çizgiler de kullanabilirsin" → fotogerçekçi + ince çizgi gravür/illüstrasyon + yağlı boya karışık.
- "ElevenLabs'te asla ve asla görsel üretmiyoruz, sadece ses."
- "Bilinç altı diye bir şey yok, bilinç dışı" → iki cümle yeniden seslendirildi ve yalnız o yerler değiştirildi ("sadece cümlenin geçtiği yeri değiştir").
- Müzik (Enes, 2026-11-17): "Kamu malı kayıt" → düzen "Gnossienne → Sarabande ★" (1. perde Satie Gnossienne 1, 2. perde Bach Sarabande, sonu Gymnopédie 1; Reels'te Jung'da Sarabande'a geçer).
- Gerçek portreler Wikimedia'dan indirilsin: "Evet, indir" (Ibsen, Freud, Adler, Jung, Hume, Aristoteles; Adler düşük çözünürlüklü → SDXL img2img aynası `adler-hq.jpg`).
- Kapanış (Enes'in sözleri): "Peki sence insanın bir doğası, bir özü var mı? Böyle bir şey mümkün mü? Varsa sence insanın özü nedir? Bunu yorumlara yaz. Daha fazlası için takipte kal." + kapak fotoğrafı + adres kartı.

## Ses
- `ses/vo-1.mp3` (giriş+bilim+felsefe 3:08) + 0,9 sn + `ses/vo-2.mp3` (psikoloji→kapanış 3:48, +0,7 dB) → `ses/vo-ilk.wav`; yamalar `ses/yama-1.mp3` (4.80-8.65 → 193.10-196.90), `ses/yama-2.mp3` (0-2.95 → 235.78-238.38) → `kaynak/audio/vo.wav` 417,3 sn, LRA ~2-3 LU.
- Hizalama: whisper 101-131 sn arasını halüsine etti ("izlediğiniz için teşekkürler"); `logs/parca.py` ile ayrı transkribe edildi. Altyazı yazımı `logs/metne_esle.py` ile senaryodan (885 kelime = senaryo). `video.json` duzelt boş.
- Kontrol edilecek: "Jung" telaffuzu (whisper "Yom" duydu, 235.6 / 255 / 377 sn civarı). Enes'e dinletilecek.

## Motor
- `kaynak/index.html`: tek motor, `?ar=w|t`. Çekimler senaryo cümlesine çapalı (SH listesi), Reels'te kesilen çekimler düşer. İmza: soğan zarı geçişi (merkezden açılan damarlı yarı saydam zar), bölüm kartları I-IV (Cinzel, harf aralıklı), isim etiketleri, sayı kartları (Anton), altyazı ince siyah şerit + altın aktif kelime.
- `logs/plan.py`: paragraf → kelime aralığı, Reels [R] parçaları → `kaynak/words-r.js` + `kaynak/audio/vo-r.wav` (176,3 sn).

## Ses (miks)
- `logs/ses.py w|t` → `kaynak/audio/mix.wav` / `mix-r.wav` (müzik konuşmada -17, aralarda -9 dB, 1,2 sn yumuşak rampalar; zar geçişlerinde alçak whoosh) → `master.wav` / `master-r.wav` -14 LUFS, LRA 2,7.
- Teslimde hazır: `outputs/Insanin-Ozu/Yayin-paketi.md` (uzun + Reels), `Insanin-Ozu-altyazi.srt`, `Insanin-Ozu-Reels-altyazi.srt`.

## Dosyalar
- Araştırma, rakip, fikirler: `Insanin-Ozu/Adim-1-2-3.md`
- Senaryo: `Insanin-Ozu/Insanin-Ozu-senaryo.md` (henüz yok)
- Görseller: yerel SDXL `gorseller/ai/`, arşiv PD `gorseller/arsiv/`. Flow/Veo yok.

## Krediler
- ElevenLabs: 6.271 karakter (eleven_v4, Sercan Esen; 6.000 karakterlik tek istek sınırı aştı, kredi düşmedi → iki parça 2.746 + 3.244; yama 146 + 155). Kalan ~24.300.
- Veo / Flow: 0 (kullanılmayacak)

## Açık işler
- [x] "Jung" telaffuzu: Enes "yung" dedi; deneme okumasından 3. yazım /juŋ/ seçildi ("3 doğru olan")

## Teslim
- `outputs/Insanin-Ozu/`: 16:9 uzun mp4, 9:16 Reels mp4, Onizleme-telefon.mp4, iki .srt, Kapak (YouTube 16:9 + Reels 9:16), Yayin-paketi.md

## İkinci tur (2026-11-17)
- Telaffuz: Enes "jung'un okunuşunu yazılı veriyorum = yung". "Yung" yazımı "Yang" okundu (250 kredi boşa); 4 yazımlık deneme (136), Enes "3 doğru olan" → /juŋ/ ile 4 cümle tek kayıt `ses/yama-4.mp3` (254). `logs/jung_yama.py` ile vo.wav'a eklendi (+1,3 sn), kelime zamanları kaydırıldı, Reels aralığı 0,30 sn (2:59 sınırı).
- Eller: Enes "mevcut videodaki tüm eller bozuk ... en sondaki esmer el ... hayvan toynağına benziyor", "bebek parmakları yanlış". El geçen 14 sahne (21 kare) Flow Nano Banana'da referanssız, 2K yeniden çizildi (`logs/eller_kur.py`, tohum 5NN). Enes soğan soymada 2. (yatay) ve 3. (dikey) kareyi seçti. Dikey kapak 3. kareyle yeniden kuruldu.
- Uzun 7:06 (425,8 sn), Reels 2:59 (179,8 sn), ikisi de -14 LUFS.
