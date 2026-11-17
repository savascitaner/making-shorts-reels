# Kanal Kimliği: @TanerSavaşçı (YouTube)

## Teslim dosyaları
| Dosya | Ölçü | Boyut |
|---|---|---|
| `YouTube-Banner-2560x1440.png` | 2560×1440 (16:9) | 3,9 MB (sınır 6 MB) |
| `YouTube-Profil-800x800.png` | 800×800 | 1,4 MB |
| `Guvenli-Alan-Onizleme.png` | TV (tamamı), masaüstü (2560×423 bant), mobil (1546×423 orta) kırpımları ile 98/48/36 px yuvarlak profil | 3,4 MB |

## Tasarım
- **Banner:** Kömür karanlıkta asılı bir bronz kandil yanıyor, amber ışığı yazıya doğru yayılıyor. Kanal adı "TANER SAVAŞÇI" (Anton, krem) ve "FELSEFE · PSİKOLOJİ · İNSAN" (Cinzel, amber) yazılı; altında Instagram @sevgiliinsann ve www.sevgiliinsan.com, kodla çizilmiş simgeleriyle. Kandil ve tüm yazılar, her cihazda görünen 1546×423 güvenli alanın içinde.
- **Profil:** Enes'in taş kabartma portresi. Oyması değişmedi, yalnızca ışığı yeniden kuruldu: koyu zemin, soldan vuran amber kandil ışığı. Yüz yuvarlak kırpımda ortalı ve 98 px'te de okunuyor.
- Görseller Google Flow'da Nano Banana ile ücretsiz üretildi (Flow projesi "Kanal-Kimligi"). Nano Banana Pro üç denemede de "kullanım sınırı" hatası verdi, kredi düşmedi. Yazılar ve son düzen kodla kuruldu (`Kanal-Kimligi/kaynak/kimlik.html` ve `capture.mjs`). Türkçe İ, Ş ve Ç harfleri doğru.

## Ölçüler ve kaynaklar
- **Resmî (YouTube Yardım, "Manage your channel branding"):** banner en az 2048×1152 (16:9), TV için önerilen 2560×1440, dosya en çok 6 MB. En küçük boyutta yazı ve logo güvenli alanı 1235×338; bu, 2560 genişliğe ölçeklenince ≈1546×423 eder. Banner'a gölge, kenarlık ya da çerçeve gibi süsler eklenmemeli. Profil 98×98 px'te gösterilir, biçim JPG/GIF/BMP/PNG (hareketli GIF olmaz), dosya en çok 15 MB.
  https://support.google.com/youtube/answer/10456525
- **Üçüncü taraf rehberler (2026):** profil için önerilen yükleme ölçüsü 800×800, gösterim yuvarlak. Güvenli alan 1546×423.
  https://havecamerawilltravel.com/youtube-banner-size/ · https://www.linearity.io/blog/youtube-size-guide/ · https://socialsizes.io/youtube-cover-photo-size/

## Yükleme adımları
1. YouTube Studio → **Özelleştirme** → **Profil** sekmesi.
2. **Banner görseli** → Değiştir → `YouTube-Banner-2560x1440.png`. Kırpma penceresinde varsayılan kutuyu olduğu gibi bırak (tüm görsel seçili), **Bitti**.
3. **Resim** → Değiştir → `YouTube-Profil-800x800.png`. Kırpma karesini tüm görsele yay, **Bitti**.
4. Sağ üstten **Yayınla**. Kanal sayfasını telefonda ve bilgisayarda bir kez aç, kırpımlar önizlemedeki gibi görünmeli.
