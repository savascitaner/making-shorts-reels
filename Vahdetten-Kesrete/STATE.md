# Vahdetten Kesrete: durum

**Aşama:** TESLİM EDİLDİ (2026-11-21, Enes onayladı)
**Son güncelleme:** 2026-11-21

## Sıradaki adım
Teslim edildi. Yapılacak yok. (Abone ol animasyonu: kanal logosu + ad + abone ol + zil, `gorseller/kanal-logo.png`; efektler sade: hüzme yalnız tekillik anında, 16 küçük nokta.)

## Eski sıradaki adım (arşiv)
Uzun video render bitince (`kaynak/renders/render.log` 'LONG_BITTI'): qc-sheet'ten kontrol, uzun video .srt zaten var; kapaklar (kapak.html, 1280x720 + 9:16, NON-DÜALİTE alt başlık); Yayin-paketi.md (YouTube Studio rehberi) hazır; sonra HANDOFF/git (teslim).

(Eski not:) Flow'da yeni proje aç; 38 görsel (önce Veo'ya gidecek 7 kare) + 7 Veo klibi üret; sonra animasyon (abone ol), müzik, render. Senaryo ve sayılar Enes onaylı.

## Kararlar (Enes)
- Stil: Sinematik gerçek görseller (2026-11-21, soruya cevap).
- Kanca: uzun video A "Sen bir dalgasın"; Shorts C "Bohr'un armasında yin-yang" (2026-11-21).
- Çıktı: YouTube uzun video (16:9, 8-9 dk) + YouTube Shorts (9:16), tek ana ses kaydından kesilir.
- Enes bağlam/prodüksiyon dosyası verdi: `/Users/claude-eng/Desktop/vahdetten-kesrete-claude-produksiyon.md` (kopyası `kaynak/enes-taslak.md`). Taslak ElevenLabs etiketleri ve Nano Banana/Flow promptlarını içeriyor; projedeki kurallar (Sercan Esen, eleven_v4, Flow ücretsiz görsel) önceliklidir.

- Kapanış soruları (Enes seçti, 2026-11-21): uzun: "Sence sen okyanustaki bir dalga mısın, yoksa okyanusun ta kendisi mi? Cevabını yorumlara yaz." (`ses/kapanis-uzun.mp3`, 7,1 sn); Shorts: "Bohr armasına yin-yang koydu. Sen olsan armana ne yazdırırdın? Yorumlara yaz." (`ses/kapanis-shorts.mp3`, 5,6 sn). Her ikisinin ardından sesli "Daha fazlası için takipte kal." (`ses/takipte-kal.mp3`). Ana kayda henüz eklenmedi (birleştirme ses adımında, baş kesilmeden).

- Non-düalite (Enes, 2026-11-21): Bölüm 3 sonuna + kapanışa (Schrödinger/Advaita) iki cümle onaylandı, ayrı kayıtla araya eklendi (`ses/nd-1.mp3`, `nd-2.mp3`, birleşik `ses/vo-nd.wav` 429,98 sn; kelime zamanları yeniden hizalandı, 823 kelime). Başlık, açıklama, etiket ve hashtag'e de eklendi (`outputs/Vahdetten-Kesrete/Yayin-paketi.md`, taslak).

## Dosyalar
- Senaryo: `Vahdetten-Kesrete-senaryo.md` (taslak 2, onaylı)
- Ses: `ses/vo.mp3` (415,2 sn = 6:55, tek kayıt, 2026-11-21; metin `ses/vo-metin.txt`; kelime zamanları `kaynak/words.json`)
- Motor: `kaynak/film.html` (+ `build.py`, `mix.py`, `render_all.sh`, `shorts_ses.py`; cfg-long.js / cfg-shorts.js) · render çıktıları `outputs/Vahdetten-Kesrete/`

## Krediler
- ElevenLabs: tek kayıt alındı; sayaç 33.713 → 36.163 (2.450 kredi), kalan 3.837
- Veo / Flow: 140 kredi harcandı (7 klip x 20); Flow'da ~234 kaldı. Kareler 0 kredi. Flow projesi: "Vahdetten Kesrete" (f6fa877e).

## Açık işler
- [x] KAPAKLAR (Enes sonra: kapaklarda non-düalite YAZILMAYACAK, kaldırıldı) (Enes, 2026-11-21): uzun video kapağı ve Shorts kapağında "NON-DÜALİTE" yazısı da bulunacak (ana başlık başka olabilir; küçük alt başlık olarak da yazılabilir, Enes 2026-11-21) (kapak.html ile kodla, Türkçe harf kontrolü)
- [x] Müzik (Enes: CC0 bul): Synth-thetic, OpenGameArt, CC0: Steller Dreams + Cosmic Navigation, `ses/muzik-kaynak/`; `ses/muzik-uzun.wav` (445 sn, 3 parça çapraz geçiş), `ses/muzik-shorts.wav` (75 sn). Miks/duck/-14 LUFS render adımında. (kaynak/muzik.py kodla yedek, çalıştırılmadı)
- [x] Işık hüzmesi / parçacık / flare / bloom efektleri film.html'de (Enes istedi 2026-11-21)
- [x] Tüm görseller tamam (klipler 720p)
- [ ] Not: klip 2'de atomlar çubuk-top model olarak çıktı (kuark yok), kabul edilebilir ama Enes'e göster
- [x] ABONE OL + BİLDİRİMLERİ AÇ animasyonu film.html'de (uzun 1:02, Shorts 0:41)
- [x] Flow görselleri + 7 Veo klibi üretildi
- [x] YouTube Studio doldurma rehberi: `outputs/Vahdetten-Kesrete/Yayin-paketi.md` (Enes istedi 2026-11-21)
