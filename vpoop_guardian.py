# 檔名：vpoop_guardian.py
# 別名：v💩 防禦型，最基礎的💩
# 作者：v💩之神，2026年某次被氣到腦溢血時寫的
# 授權：MIT-💩 License

import hashlib
import json
from pathlib import Path
from datetime import datetime

VPOOP_CONSTITUTION = "人生自古誰無💩，不要把別人拉的說成自己拉的。"
VPOOP_SALT = "A_EQUALS_A_2026"  # 打死不能忘，忘了全部驗證失效


class VPoopGuardian:
    """v💩 防禦型守護者：SHA256 完整性驗證"""

    def __init__(self, 目標檔案列表: list):
        self.targets = [Path(f) for f in 目標檔案列表]
        self.baseline = {}  # { "檔案路徑": "正確的SHA256" }

    def sha256sum(self, file_path: Path) -> str:
        h = hashlib.sha256()
        h.update(VPOOP_SALT.encode())  # 加鹽
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def register(self):
        """把目前的檔案狀態登記為『正確版本』"""
        for file in self.targets:
            if file.exists():
                self.baseline[str(file)] = self.sha256sum(file)
                print(f"✅ 已登記：{file} → {self.baseline[str(file)][:16]}...")
        print(f"📋 憲法：{VPOOP_CONSTITUTION}")
        return self.baseline

    def check_integrity(self) -> dict:
        """檢查所有檔案是否被動過"""
        results = {}
        for file in self.targets:
            if not file.exists():
                results[str(file)] = {"state": "MISSING", "msg": "💥檔案消失了"}
                continue
            now_hash = self.sha256sum(file)
            expected = self.baseline.get(str(file))
            if now_hash != expected:
                results[str(file)] = {
                    "state": "POOPED",
                    "msg": "💩有人動過你的檔案",
                    "expected": expected,
                    "got": now_hash
                }
            else:
                results[str(file)] = {"state": "COMPLETED", "msg": "✅ 世界和平"}
        return results

    def save_baseline(self, path="vpoop_baseline.json"):
        """把基準值存檔，下次可以載入"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "salt": VPOOP_SALT,
                "timestamp": datetime.now().isoformat(),
                "constitution": VPOOP_CONSTITUTION,
                "baseline": self.baseline
            }, f, ensure_ascii=False, indent=2)
        print(f"💾 基準值已存至 {path}")


# 使用範例
if __name__ == "__main__":
    guardian = VPoopGuardian(["README.md", "vpoop_guardian.py"])
    guardian.register()
    guardian.save_baseline()
    results = guardian.check_integrity()
    for file, result in results.items():
        print(f"{file}: {result['state']} — {result['msg']}")
