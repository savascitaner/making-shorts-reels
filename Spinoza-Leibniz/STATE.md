# Spinoza-Leibniz: durum

**Aşama:** TESLİM EDİLDİ
**Son güncelleme:** 2026-11-17

## Sıradaki adım
Yok: reels teslim edildi (2026-11-17). Enes yayınlayacak; isterse not üzerine düzeltme.

## Teslim özeti (2026-11-17)
- Kurgu motoru `kaynak/index.html`: 34 plan, Veo klipleri `gorseller/klip/<ad>/` (188 kare, 24 fps) sync.json çapalarıyla doğrusal eşlenir (captureFrame async, kare isteğe göre yüklenir). İmza: prizmatik mercek huzmesi süpürmesi (7 bölüm geçişi) + cam tınısı; Cinzel izli kartlar; mum kodla söner (90.06 sn "öldü.") + duman; son soru ikiye bölünmüş ekran (Spinoza | Leibniz, ortada ışık çizgisi).
- Ses `kaynak/music.py` (bu videoya özel): Spinoza = çello notası, Leibniz = yükselen klavsen arpejleri, "senfoni" anında açık akora çözülme; kibrit, yağmur, kapı vuruşu, taş yükselişi/düşüşü, tüy kalem, gök gürültüsü, mum üfleme. -14 LUFS master.
- Kapak: Canva tasarımı DAHbHafgq70 (kodla kurulan `kaynak/kapak.html` yüklendi; Canva İ harflerinin noktasını düşürdü, düzeltildi, Enes "harika kaydet" dedi).
- Yayın paketi `outputs/Spinoza-Leibniz/Yayin-paketi.md`.

## (eski) Adım 7 notu
Adım 7 kurgu: `kaynak/index.html` motorunu bu videoya özel kur (SH sahne listesi + IMG haritası + kartlar), sonra `./uret.sh Spinoza-Leibniz ses` (müzik/sfx/miks), `qc`, `render`. Sonra adım 8 kapak, 9 yayın paketi, 10 QC/teslim, git.

**Malzeme haritası**
- Ses: `ses/vo.mp3` 104 sn; konuşan parçalar `ses/parcalar.json`; kelimeler `kaynak/words.json` (192 kelime; Veo replikleri kelime no V1 29-37, V2 56-65, V3 113-126, V4 138-145).
- Veo (konuşan, 1080x1920, 24fps, 7.85 sn): `gorseller/veo/v1_spinoza_tas.mp4` (VO 18.23-22.92), `v2_leibniz_hapishane.mp4` (33.10-36.74), `v3_spinoza_eksik.mp4` (59.16-65.34), `v4_leibniz_senfoni.mp4` (72.86-76.38). Kelime kelime çapa: `gorseller/veo/sync.json` ([vo_sn, klip_sn] çiftleri; V4'te Veo "olmasa"dan sonra 1.7 sn duraklıyor, çapa arası doğrusal eşle). Klipler henüz `klip/<ad>/` karelerine açılmadı.
- Flow kareleri `gorseller/flow/`: f00 Spinoza taş (orta), f01 Leibniz öfke, f02 Leibniz yumuşak, f03 Leibniz dinler, f04 Spinoza bakış, f05 Spinoza dinler, f06 omuz üstü (Leibniz arkadan, Spinoza karşıda), f07 kapı (Leibniz arkadan, yağmurlu sokak), f08 mercekten kırılan ışık (el+mum), f09 Spinoza taş yakın. (`flow/eski/` = Spinoza'ya benzeyen ilk Leibniz denemeleri, kullanılmaz.)
- SDXL `gorseller/ai/`: iyi olanlar a01_sokak (s11,s23), a02_mum (s11,s23), a03_mercek_s11, a04_tas_s11, a05_elyazma_s11, a06_tarla (s11,s23), a08_pencere_s11. a07 kullanılmaz: kapanışta mumu kodla söndür + duman.
- Arşiv: `gorseller/arsiv/` Spinoza ve Leibniz kamu malı portreleri (`LICENSES.csv`).

**Kurgu notları**
- Konuşan karakter yalnız Veo klibinde ağzı hareketli görünür; diğer replikte dinleyen yüz (f03/f05, ağız kapalı), omuz üstü f06, mercek/taş/el yazması B-roll. Kodla ağız YOK.
- İmza: mercekten kırılan altın ışık huzmesi geçişi + cam tınısı + tek derin çello notası (Spinoza), yükselen yaylılar (Leibniz). Kanca 0-3 sn Anton "SEN Mİ SEÇTİN?", altyazı o sırada gizli; 3-14 sn "LAHEY, 1676 · ÖLÜMÜNE ÜÇ AY KALA".
- Kapanış: soru kartı "Sence sen hangisisin: atılan taş mı, seçen ruh mu? Cevabını yorumlara yaz." → takip kartı (YouTube @TanerSavaşçı, Instagram @sevgiliinsann, www.sevgiliinsan.com). video.json sure 112.

## Kararlar (Enes)
- Kapak: "harika kaydet" (2026-11-17)
- Stil: Sinematik (2026-11-16)
- Kanca: A "Sen mi seçtin?" (2026-11-16)
- "86 flow kredisi kaldı planlamayı buna göre yap. yüksek kaliteden bir şey kaybetmeden yapmamız lazım" → 4 Veo konuşan klip × 20 = 80 kredi, kalan her şey ücretsiz Nano Banana + SDXL + kodla hareket
- Enes'in Google taslakları eskiz: `taslak/01-03` ("faydalanacak alanları kullanırız")
- Taslaktan alınacaklar: taş kancası, dış ses sorusu, mercekten kırılan ışık imzası, mum ışığı/Rembrandt görsel tarifleri, ElevenLabs ton etiketleri
- Senaryo onaylandı (2026-11-16, "Onay, devam")
- Leibniz ikinci ses: Orhan (voice y6X1mFgtBqHFtQwrOezf); Spinoza + dış ses: Sercan Esen
- Veo replik aralıkları (vo.mp3 kelime no): V1 Spinoza 29-37 "Havaya…düşünürdü?", V2 Leibniz 56-65 "Bu bir hapishane…kalır?", V3 Spinoza 113-126 "Tanrı bir amaç…mi?", V4 Leibniz 138-145 "Bir senfonide…tamamlanmaz."
- Akışa göre değişenler: Veo promptlarında isim yok; dudak senkronu Veo'nun kendi Türkçe repliği (ses yüklenmez); ses Sercan Esen v4 tek kayıt

## Dosyalar
- Araştırma/rakip/fikirler: `Adim-1-2-3.md`
- Senaryo: `Spinoza-Leibniz-senaryo.md`

## Krediler
- ElevenLabs: 1094 (Sercan) + 548 (Orhan) = 1642
- Veo / Flow: 80 (4 klip × 20; 6 kredi kaldı). Nano Banana kareleri ücretsiz.

## Açık işler
- [x] Ses: `ses/vo.mp3` 104 sn (`logs/birlestir.py`, parça haritası `ses/parcalar.json`); kelimeler `logs/kelimeler.py` ile ayrı transkriptlerden (whisper birleşik kayıtta cümle atlıyordu); .srt outputs'ta
- [x] Flow kareleri + 4 Veo klibi (hepsi Türkçe repliği birebir söyledi, red yok)
- [x] Kurgu, ses miksi, QC, render
- [x] Kapak (Canva), Yayin-paketi.md, git

## Teslim
- `outputs/Spinoza-Leibniz/`

## Ek (Enes, 2026-11-17)
- Flow alternatifleri araştırması: `Arastirma/Flow-alternatifleri.md` (öneri Hedra + bizim ses). Hedra testi: "Şimdilik hayır".
