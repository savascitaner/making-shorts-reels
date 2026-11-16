# 03 - ElevenLabs v4 Seslendirme, Tonlama ve Duygu Yönetimi Promptları

Bu dosya, Spinoza, Leibniz ve Dış Ses (Anlatıcı) karakterlerinin **ElevenLabs v4** modelinde en doğal, tiyatral ve duygu yüklü şekilde seslendirilmesi için özel olarak tasarlanmış ayarları ve **Audio Tag (Ses Etiketi)** metinlerini içerir.

---

## 1. KARAKTER SES PROFİLLERİ VE ELEVENLABS v4 AYARLARI

### A. Baruch Spinoza (Sakin, Derin, Sarsılmaz ve Bilge)
* **Önerilen Ses Tipi:** Olgun erkek sesi, hafif bariton, dingin, entelektüel ve dingin bir otoriteye sahip (Örn: *Marcus*, *Daniel* veya Türkçe klonlanmış dingin belgesel sesi).
* **Stability (Kararlılık):** %65 *(Duygusal dalgalanmalardan uzak, vakur ve tutarlı bir ton için)*
* **Similarity (Benzerlik):** %80
* **Style Exaggeration (Stil Abartısı):** %25 *(Abartıdan uzak, saf akılcı ton)*
* **Speed (Hız):** 0.92x *(Düşündürücü ve ağırbaşlı tempo)*

### B. Gottfried Wilhelm Leibniz (Tutkulu, Hızlı Düşünen, Diplomatik ve Duygusal)
* **Önerilen Ses Tipi:** Enerjik, orta-kalın erkek sesi, hitabet gücü yüksek, duygusal vurguları belirgin (Örn: *Callum*, *Adam* veya tiyatral vurgusu güçlü erkek sesi).
* **Stability (Kararlılık):** %45 *(Öfke, hayret ve umut geçişlerini verebilmek için daha dinamik)*
* **Similarity (Benzerlik):** %75
* **Style Exaggeration (Stil Abartısı):** %55 *(Dramatik ve ikna edici tonlama)*
* **Speed (Hız):** 1.02x *(Zihni hızlı çalışan bir dahinin akıcılığı)*

### C. Dış Ses / Anlatıcı (Gizemli, Sinematik ve Merak Uyandırıcı)
* **Önerilen Ses Tipi:** Derin bas-bariton belgesel sesi.
* **Stability (Kararlılık):** %55
* **Style Exaggeration (Stil Abartısı):** %40
* **Speed (Hız):** 0.95x

---

## 2. ELEVENLABS v4 HAZIR SESLENDİRME METİNLERİ (TONLAMA ETİKETLERİYLE)

*Not: Köşeli parantez içindeki `[etiketler]` ElevenLabs v4'ün doğrudan duygu, nefes ve duraksama motorunu tetiklemek için optimize edilmiştir.*

### [00:00 - 00:18] SPINOZA - GİRİŞ KANCASI
```text
[calm, intriguing, slightly hushed] Sana bir soru sorayım Leibniz... [pause 0.8s] Havaya fırlatılan bir taş, tam uçuşun ortasında aniden bilinç kazansaydı, [thoughtful] sence ne düşünürdü? [pause 1.2s] 

[matter-of-fact, penetrating] O taş, kendi özgür iradesiyle havada süzüldüğünü sanırdı. Oysa onu fırlatan elden ve yerçekiminden habersizdir. [serious, slow] İşte insan da tam olarak böyle... Kendi arzularının farkında, ama o arzuları yaratan gizli sebeplerden [whispering intensity] tamamen habersiz.
```

### [00:18 - 00:55] LEIBNIZ - İTİRAZ VE GERİLİM
```text
[shocked, passionate, sharp breath] Bu korkunç bir hapishane Spinoza! [frustrated] Eğer her şey senin dediğin gibi kör bir zorunlulukla oluyorsa... [pleading, emotional] O zaman iyiliğin ne değeri kalır? Bir annenin çocuğuna duyduğu sevgi ile bir taşın yere düşmesi arasında ne fark var? [pause 1.0s]

[authoritative, resolute] Tanrı bir kör makine değildir! O, sonsuz ihtimaller arasından... "mümkün olan en iyi dünyayı" özgürce seçti. [inspiring] Bizler rüzgarda savrulan taşlar değiliz; her birimiz evrenin eşsiz birer aynasıyız!
```

### [00:55 - 01:40] SPINOZA - SARSICI YANIT
```text
[serene, unshakeable] İyi ile kötü... [pause 0.6s] Bunlar evrenin değil, sadece insanın kendi çıkarına göre uydurduğu kelimeler. [calm, objective] Doğa ne merhametlidir ne de acımasız. Yağmur, susuz bir tarlayı yeşertmek için yağmaz; atmosferdeki şartlar zorunlu kıldığı için yağar. [pause 1.0s]

[piercing, philosophical] Eğer Tanrı bir amaç uğruna yaratıyorsa, bu onun bir şeye "ihtiyacı" olduğu anlamına gelir. [soft, devastating] Eksik olan bir şey Tanrı olabilir mi?
```

### [01:40 - 02:20] LEIBNIZ - DUYGUSAL ZİRVE
```text
[deep exhale, melancholic yet firm] Senin Tanrın kusursuz ama soğuk Spinoza. Ne duaya cevap verir, ne de gözyaşını görür. [warm, hopeful] Benim evrenimde ise acının bile bir harmonisi var. Bir senfonideki karanlık notalar olmadan, o büyük müzik tamamlanmaz. [passionate conviction] İnsana anlam veren şey, seçebilme gücüdür!
```

### [02:20 - 02:45] KAPANIŞ VE DIŞ SES
**Spinoza:**
```text
[whisper, serene] Anlamı dışarıda arama... Sen doğanın bizzat kendisisin.
```

**Leibniz:**
```text
[firm, warm] Hayır... Sen, yaratıcının en özel melodisisin.
```

**Dış Ses (Anlatıcı):**
```text
[dramatic, low, captivating] Peki sen hangisisin? [pause 0.7s] Kendi hikayesini yazan özgür bir ruh mu... yoksa kusursuz bir zorunluluğun parçası mı? [intriguing] Yorumlarda tarafını seç.
```

---

## 3. SES MİKSAJI VE ATMOSFER ÖNERİSİ (KURGU İÇİN)
* **Arka Plan Sesi (Ambience):** Düşük seviyede (-28 dB) şömine çıtırtısı ve cama vuran hafif yağmur sesi.
* **Müzik:** Çello ağırlıklı minimalist barok/modern gerilim müziği (Örn: Max Richter tarzı). Spinoza konuşurken tek bir derin çello notası, Leibniz konuşurken yaylıların yükselişi kurguyu zirveye taşır.
