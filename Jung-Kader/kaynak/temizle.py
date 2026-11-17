import re
L=[l.rstrip("\n") for l in open("transkript-ham-mlx.txt") if l.strip()]
def sec(t): m,s=t.split(":"); return int(m)*60+int(s)
rows=[(sec(l[1:6]), l[8:].strip()) for l in L]
B=[("00:00","Giriş: Jung'un sözü"),("01:21","Birinci düğüm: Aşırı genelleme ve kaderin dört yüzü"),
("06:03","Freud ve Jung: Her şey bilinçdışı mı?"),("08:41","Marx-Engels ve Freud'un itirazı"),
("11:51","Dinciler ve üç kardeş hikâyesi"),("16:30","Varoluşçular: Kaderini insan mı belirler?"),
("17:52","Altın anahtar: Tek sebep yoktur"),("19:44","Kaderi belirleyenler 1-3: Bilinçdışı, genler, koordinatlar"),
("26:39","Önceden yazılmış kader inancı ve standart ruh"),("36:40","Kavramlar: Tanrı kavramı, kader = ölçü, eta fonksiyonu"),
("44:40","Kaderi belirleyenler 4-7: Dış olaylar, varoluş sorunları, içgüdüler ve duygular, şartlandırılmış zihin"),
("60:52","Yedi başlık ve ikinci düğüm: İnsanın doğası diye standart bir şey var mı?"),
("68:08","Tekâmül ve entropi"),("73:39","Neden yanlış soru? Köpek örneği, cennet, Nietzsche"),
("81:53","Kendini tanı: Ölçü artık senin elinde"),("86:42","Kapanış: Hangi insanın?")]
R=[(r"\b(?:Yunka|Yunko|Yunk|Junko|Jung|yunka|yunk)\b","Jung"),(r"[Bb]ilin[çc]\s?alt","bilinçdış"),(r"[Kk]ollektif","kolektif"),
(r"Fuat Basar Sema|Fuad Basar'da Sema","fuad-basar-sem'"),(r"Fuat sevdam","fuad sevdam"),(r"fevbesen","FBS'n"),(r"fevbesi","FBS'si"),(r"febeseler","FBS'ler"),(r"\bfbs","FBS"),
(r"Senofenos","Ksenofanes"),(r"Windgenstein","Wittgenstein"),(r"İbni Meymun","İbn Meymun"),(r"İbni\s+Haldun","İbn Haldun"),
(r"Fahrettin Razi","Fahreddin Râzî"),(r"Kıvanç tatlıtuğu","Kıvanç Tatlıtuğ'u"),(r"\b[Tt]anatos","Thanatos"),(r"\beros\b","Eros"),(r"\btanatos\b","Thanatos"),
(r"Niçe","Nietzsche"),(r"übermensch","Übermensch"),(r"Open Theism","açık teizm (open theism)"),(r"etaf? fonksiyon","eta fonksiyon"),
(r"İh agape\s+mui\s+arate","İ agapi mu arete (Yun. Η αγάπη μου αρετή)"),(r"\barate","arete"),(r"Eşedde çağını da\s+geçip Şeyahun","eşüdd çağını da geçip şuyûh"),
(r"ehli musaf","ehl-i mushaf"),(r"el kuran musafında","el-Kur'an mushafında"),(r"Cebri kadar yoktur","Cebir, kader yoktur"),
(r"Cebriye mi kaderiye mi","Cebriye mi, Kaderiye mi"),(r"onli Kurancılar","only Kur'ancılar"),(r"plezada","plazada"),(r"Kelammi","Kelami"),
(r"Esma-ül Hüsnay","Esmâü'l-Hüsnâ'yı"),(r"5tl'lerinize 3tl'lerinize","5T'lerinize, 3T'lerinize"),(r"Göbekli\s+tepeden beri","(…)"),
(r"men arefe nefsihi\s+fekad arefe rabbihi","men arefe nefsehû fekad arefe Rabbehû"),(r"[Mm]en arefe nefsihi","Men arefe nefsehû")]
out=["# Murat Avcıoğlu: Jung'un \"bilinçdışı ve kader\" sözü üzerine (22.02.2019)\n",
"Kaynak: `ses/kaynak-kayit/avcioglu.mp3` (91:46). Transkripsiyon: whisper large-v3 (GPU). Zaman damgalı ham metin: `transkript-ham-mlx.txt`.\n",
"**Bu dosya:** konuşmanın tamamı, bölümlere ayrılmış. İsim, kavram ve terim düzeltmeleri uygulandı (\"bilinçaltı\" → \"bilinçdışı\", Jung, Thanatos, Ksenofanes, Wittgenstein, İbn Haldun, Fahreddin Râzî, FBS = fuad-basar-sem'). Konuşma dilindeki cümleler olduğu gibi duruyor; TDK'ya göre cümle düzeltmesi videoya alınan her bölümde senaryoda yapılır.\n",
"**Emin olunamayan kelimeler** `[?]` ile işaretli: \"novluç\" (iki kez \"birinci/ikinci novluç\" diye geçiyor), \"2Z 2M\", \"Berces'te\", \"Engip'te\", \"Nahl'imin Nem suresi\", \"Rasiyun\".\n"]
for i,(t,h) in enumerate(B):
    a=sec(t); b=sec(B[i+1][0]) if i+1<len(B) else 10**9
    txt=" ".join(x for s,x in rows if a<=s<b)
    for p,q in R: txt=re.sub(p,q,txt)
    for w in ["novluç","novlucumuz","novuluc","no'lu cuna","neoluş","2Z 2M","Berces'te","Engip'te","Nahl'imin Nem suresinin","Rasiyun"]: txt=txt.replace(w,w+" [?]")
    out.append(f"\n## [{t}] {h}\n\n{txt}\n")
open("transkript.md","w").write("\n".join(out)); print(sum(len(x.split()) for x in out),"kelime")
