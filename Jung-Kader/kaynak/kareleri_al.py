# Flow çıktılarını adlarıyla gorseller/ai/{r,w}/ altına kopyalar.  python3 kareleri_al.py
import json, os, shutil
G = "/Users/claude-eng/Shorts - Reels/Jung-Kader/gorseller"
for fmt, src, names, off in [("r", "Jung-Kader", "prompts-flow-reels-adlar.json", 3), ("r", "Jung-Kader-ek9", "prompts-flow-ek9-adlar.json", 1), ("w", "Jung-Kader-w4", "prompts-flow-w3-adlar.json", 1), ("r", "Jung-Kader-fix9", "prompts-fix-adlar.json", 1), ("w", "Jung-Kader-fix16", "prompts-fix-adlar.json", 1), ("r", "Jung-Kader-insan9", "prompts-insan9-adlar.json", 1), ("w", "Jung-Kader-insan16", "prompts-insan16-adlar.json", 1), ("r", "Jung-Kader-rot9", "prompts-rot9-adlar.json", 1)]:
    os.makedirs(f"{G}/ai/{fmt}", exist_ok=True)
    N = json.load(open(f"{G}/{names}")); n = 0
    for i, ad in enumerate(N):
        f = f"/Users/claude-eng/flow-mcp-out/{src}/scene-{i + off:02d}.jpeg"
        if os.path.exists(f): shutil.copy(f, f"{G}/ai/{fmt}/{ad}.jpg"); n += 1
    if fmt == "r" and os.path.exists(f"{G}/ai/flow/A0a-analiz-odasi.jpg"): shutil.copy(f"{G}/ai/flow/A0a-analiz-odasi.jpg", f"{G}/ai/r/A0a-analiz-odasi.jpg"); n += 1
    print(fmt, n, "/", len(N) + (1 if fmt == "r" else 0))
# eksikler listesi motor için
for fmt in "rw":
    have = sorted(x[:-4] for x in os.listdir(f"{G}/ai/{fmt}") if x.endswith(".jpg"))
    open(f"{G}/ai/{fmt}/liste.js", "w").write("window.HAVE=" + json.dumps(have) + ";")
