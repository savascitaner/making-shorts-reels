# Sol-Beyin-Ego — STATE

Aşama: TESLİM EDİLDİ (Enes, 2026-11-20: "süper eline sağlık threadi kapat")
Stil kararı (Enes, 2026-11-20): "sinematik gerçek görüntüler yaratılacak". Yağlıboya promptları atıldı.
Başlangıç: 2026-11-20

## Enes'in sözleriyle kararlar
- "cinecode tetikle 16:9 ve yine içinden keseceğimiz ses ile 9:16 yapacağız. Flow ve Veo lisansı aktif oldu, hareketli sahneler de yapacağız."
- Taslak: `taslak-enes.md` (5 sahne, 8-10 dk, "Arcade Yağlıboya" görsel promptları, ElevenLabs metni). Araştırma/rakip/fikir adımları (1-3) taslakla karşılandı.

## Kararlar (2026-11-20, devam)
- Cümle: "...\"ben\" dediğiniz karakter benliğiniz, sosyal egonuzdur." Çekirdek benlik = varoluşsal benlik. Kaza: sosyal ego (karakter benlik) sıfırlanır, bebek gibi başa döner.
- Ses: girişte fısıltı sonra etkili açılış; video boyunca yer yer vurgu/duygu (eleven_v4 köşeli etiketler).
- "Abone Ol, Bildirimleri Aç" zil animasyonu belirli aralıklarla (Enes tekrar hatırlattı, 2026-11-20): uzun videoda YALNIZ 2 kez: ~1:30 ve ~4:15 (Enes: "3 kez çok, 1:30 ve 4:15 yeterli"); Shorts'ta ~1:20 (yalnız görsel, ses/söz yok). Animasyonda kanal logosu (yuvarlak avatar) + "Taner Savaşçı" adı + kırmızı ABONE OL düğmesi + sallanan zil; imleç tıklar, düğme ABONE OLUNDU'ya döner. Logo dosyası yok: YouTube kanal sayfasından çekilecek (Enes onayı bekliyor).
- Shorts daha uzun (~2:30), ultra gerçek görseller, 6 Veo kilit sahne.
- ENES: krediler son kez hesaplanıp ONAYLANMADAN hiçbir üretim/ses/Flow işi başlamaz.

## Plan
- Tek ana ses kaydı (uzun 16:9); 9:16 Shorts o kayıttan cümle cümle kesilir (kesim: waveform sessizliği, whisper değil). Ayrı kısa kayıt YOK.
- Flow/Veo hareketli kilit sahneler (bütçe ~100 kredi/video, önce fiyat oku, yeni Flow projesi).

## Harcanan kredi
- ElevenLabs: tek kayıt, ~1.889 kota harcandı (31.824 -> 33.713 / 40.000). Ses: ses/vo.mp3 (4:49), metin ses/vo-metin.txt, kelimeler kaynak/words.js (587 kelime, etiketler okunmadı).
- Flow: proje açıldı (b5c8f8e2-02aa-453a-a4b0-3e052e547a64, "Sol Beyin Ego"), bakiye henüz okunmadı. Veo harcaması yok.

## Açık işler
- Stil sorusu cevabı
- Metin düzeltmeleri Enes'e yazılı onaylatılacak (tire, TDK, ElevenLabs v4 etiketleri)

## Sıradaki adım
Enes'in stil cevabı → senaryo onayı → ses.

## Sıradaki adım
Enes sesi dinler (özellikle fısıltı giriş). Flow bakiyesi okunup gorseller/prompts.json (sinematik, ultra gerçek) yazılır; önce 1 kare dene, sonra toplu; 6 Veo klibi.

## Flow durumu (2026-11-20, akşam)
- Kredi 494 (PRO). Proje: b5c8f8e2-02aa-453a-a4b0-3e052e547a64. Henüz hiç görsel üretilmedi (iki deneme de "Agent" düğmesi bulunamadı hatasıyla düştü, kredi harcanmadı).
- Teşhis: sayfada "Agent settings" ve "Flow Agent" var, "Agent" düğmesi yok; flow.ts:79 notu: agent ayar paneli composer'ı değiştirip Agent düğmesini gizliyor, "Back" ile kapanır. Sıradaki: ~/flow-mcp/src/flow.ts içinde bu düğmeyi arayan yeri ve paneli oku, sayfayı Back ile composer'a döndür (CDP 127.0.0.1:9333, scratchpad/inspect.cjs ve closeagent.cjs örnek), sonra tek kare dene. Enes'ten bir şey istenmez.
- Enes (2026-11-20): bu işi Opus ile devam ettirmek istiyor (model menüsünden seçecek).

## Üretim (2026-11-20 akşam, Opus)
- Flow motoru düzeltildi: Agent düğmesi "Flow Agent" oldu (~/flow-mcp/src/flow.ts, regex /^(Flow )?Agent$/, build + Studio yeniden başlatıldı).
- 6 Veo başlangıç karesi gorseller/flow/ (s01,s08,s14,s24,s29,s36). 32 ara kare agent batch 231123c4 (çıktı ~/flow-mcp-out/Sol-Beyin-Ego-ara). Liste: gorseller/prompts.json.
- Veo kuyrukta (Veo 3.1 Fast, 6x20=120 kredi): 06a64f7e 5e9a1bd2 3a1d0099 67a86f9b abe97b04 5d99f599 → ~/flow-mcp-out/Sol-Beyin-Ego-veo.
- Abone animasyonu tasarımı Enes onayladı ("tamam süper"): kaynak/abone-tasarim.html/.jpg, logo gorseller/kanal-logo.png.
- Agent batch 231123c4 düştü (Agent settings düğmesi prompt kutusunun dışına taşınmış). flow.ts:1687 düzeltildi ve derlendi; Studio Veo bitince yeniden başlatılacak (çalışırken başlatma kuyruğu siler), sonra 32 ara kare batch'i tekrar gönderilecek.

## Kurgu durumu (2026-11-20 gece)
- Motor: kaynak/index.html (?m=long 1920x1080 | ?m=short 1080x1920, ?taslak=1 eksik görsele izin verir). İmza: sol amber / sağ camgöbeği ton + seam geçişi.
- Altyazı = senaryo metni (words-raw.json senaryodan yeniden yazıldı, orijinal words-raw-orijinal.json). 576 kelime.
- Shorts sesi: kaynak/kisa.py (dalga sessizliğinde kesim, 6 kesit, 145,3 sn; Whisper ile doğrulandı). Shorts'tan çıkarılanlar: "Üstelik...", "Böylece...", "Ben utangaç...", "Ağır bir hasarda...", "Etiketsiz..." (3 dk sınırı).
- Ses: kaynak/cues.py (MODE=long|short python3 -m sfx) + mix.sh long|short → audio/master-*.wav, ikisi de -14,0 LUFS / -1,0 dBTP.
- Kapaklar: kaynak/kapak.png, kapak-916.png (kapak.html). Yayın paketi + 2 .srt outputs'ta.
- Veo v3 (kartlar) yalnız ilk ~4 sn kullanıldı: sağ el tavuk yerine elmayı seçiyor.
- Kalan: topla.py ile görselleri topla → QC → render (render.sh) → outputs, telefon önizlemesi.
- Müzik (Enes, 2026-11-20: "arka alana bir de ücretsiz plan müziği koy"): PD Satie, Gnossienne 1 (La Pianista) → Gymnopédie 1 (Robin Alciatore), geçiş "Ama geriye..." (uzun 216,16 / kısa 108,78). Kodla pad kaldırıldı, efektler kaldı. LICENSES.csv.
- Render başladı: render.sh short + long. Kapaklar outputs'a kondu.

## Teslim (2026-11-20 gece)
- outputs/Sol-Beyin-Ego/: Sol-Beyin-Ego-16x9.mp4 (4:58, 1920x1080, 422 MB), Sol-Beyin-Ego-Shorts-9x16.mp4 (2:35, 1080x1920, 200 MB), Onizleme-telefon-Shorts.mp4 (17 MB), 2 kapak, 2 .srt, Yayin-paketi.md.
- Flow kredisi: 494 → 374 (6 Veo klibi = 120). ElevenLabs: tek kayıt, 33.713/40.000.
- Sıradaki: Enes onaylarsa HANDOFF.md'ye satır, STATE "TESLİM EDİLDİ", ./uret.sh Sol-Beyin-Ego git.
