#!/usr/bin/env python3
# 🏎️ 檔案守護引擎 v3 — 分兩包版本

import os, hashlib, json, datetime, zipfile
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT, "輸出")
忽略清單 = {"輸出", "__pycache__", ".DS_Store"}

def 雜湊(路徑):
    h = hashlib.sha256()
    with open(路徑, "rb") as f:
        for 區塊 in iter(lambda: f.read(8192), b""):
            h.update(區塊)
    return h.hexdigest()

def 掃描():
    清單 = []
    for 根, 資料夾, 檔案 in os.walk(ROOT):
        資料夾[:] = [d for d in 資料夾 if d not in 忽略清單]
        for 名稱 in 檔案:
            路徑 = os.path.join(根, 名稱)
            相對路徑 = os.path.relpath(路徑, ROOT)
            清單.append({
                "檔案": 名稱,
                "路徑": 相對路徑,
                "雜湊": 雜湊(路徑),
                "大小": os.path.getsize(路徑)
            })
    return 清單

def 去重(清單):
    """
    規則：
    - SHA256 相同 + 檔名不同 → 去重包
    - SHA256 相同 + 檔名相同 → 保留包
    """
    已見雜湊 = {}
    保留清單 = []
    重複清單 = []

    for 項目 in 清單:
        h = 項目["雜湊"]
        名 = 項目["檔案"]

        if h not in 已見雜湊:
            已見雜湊[h] = 名
            保留清單.append(項目)
        else:
            首次檔名 = 已見雜湊[h]
            if 名 == 首次檔名:
                # 同名同雜湊 → 保留
                保留清單.append(項目)
            else:
                # 不同名但同雜湊 → 去重包
                項目["重複來源"] = f"{首次檔名}（SHA256: {h[:16]}...）"
                重複清單.append(項目)

    return 保留清單, 重複清單

def 打包兩包(保留清單, 重複清單):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    時間戳 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # ✅ 保留包
    保留zip名 = f"守護引擎_保留_{時間戳}.zip"
    保留zip路徑 = os.path.join(OUTPUT_DIR, 保留zip名)
    with zipfile.ZipFile(保留zip路徑, "w", zipfile.ZIP_DEFLATED) as zf:
        for 項目 in 保留清單:
            完整路徑 = os.path.join(ROOT, 項目["路徑"])
            if os.path.exists(完整路徑):
                zf.write(完整路徑, 項目["路徑"])
        # 附上保留清單紀錄
        zf.writestr("保留紀錄.json", json.dumps(保留清單, ensure_ascii=False, indent=2))

    # 🗑️ 重複包
    重複zip名 = f"守護引擎_重複待刪_{時間戳}.zip"
    重複zip路徑 = os.path.join(OUTPUT_DIR, 重複zip名)
    with zipfile.ZipFile(重複zip路徑, "w", zipfile.ZIP_DEFLATED) as zf:
        for 項目 in 重複清單:
            完整路徑 = os.path.join(ROOT, 項目["路徑"])
            if os.path.exists(完整路徑):
                zf.write(完整路徑, 項目["路徑"])
        # 附上重複清單紀錄
        zf.writestr("重複紀錄.json", json.dumps(重複清單, ensure_ascii=False, indent=2))

    return 保留zip名, 重複zip名

def 主程式():
    print("🏎️ 檔案守護引擎 v3 啟動")
    print("🔍 掃描中...")

    全部清單 = 掃描()
    保留清單, 重複清單 = 去重(全部清單)

    結果 = {
        "時間": datetime.datetime.utcnow().isoformat() + "Z",
        "原始檔案數": len(全部清單),
        "保留數": len(保留清單),
        "重複待刪數": len(重複清單),
        "保留清單": 保留清單,
        "重複待刪清單": 重複清單
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "審計紀錄.json"), "w", encoding="utf-8") as f:
        json.dump(結果, f, ensure_ascii=False, indent=2)

    print(f"✅ 掃描完成：原始 {len(全部清單)} 個檔案")
    print(f"📋 保留：{len(保留清單)} 個")
    print(f"🗑️  重複待刪：{len(重複清單)} 個")

    print("📦 分兩包打包中...")
    保留zip名, 重複zip名 = 打包兩包(保留清單, 重複清單)

    print(f"✅ 保留包：輸出/{保留zip名}")
    print(f"🗑️  重複包：輸出/{重複zip名}")
    print()
    print("👉 確認重複包內容無誤後，可安心刪除原始重複檔案")

if __name__ == "__main__":
    主程式()
