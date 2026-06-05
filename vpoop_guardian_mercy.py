# 檔名：vpoop_guardian_mercy.py
# 別名：v💩 仁慈版，三抽定律實作
# 繼承防禦型，加裝三振出局機制

from vpoop_guardian import VPoopGuardian, VPOOP_CONSTITUTION, VPOOP_SALT
from datetime import datetime


class VPoopGuardianMercy(VPoopGuardian):
    """v💩 仁慈版：給三次機會，因為人生自古誰無💩"""

    MAX_STRIKES = 3  # 事不過三，佛祖也救不了你

    def __init__(self, targets):
        super().__init__(targets)
        self.strike_count = {}  # { "嫌疑人ID": 抽了幾次 }
        self.mercy_log = []     # 慈悲為懷記錄

    def check_with_mercy(self, suspect_id: str = "unknown") -> dict:
        """檢查💩，但給三次機會"""
        result_map = self.check_integrity()
        is_pooped = any(r["state"] == "POOPED" for r in result_map.values())

        if is_pooped:
            self.strike_count[suspect_id] = self.strike_count.get(suspect_id, 0) + 1
            strikes = self.strike_count[suspect_id]

            if strikes == 1:
                msg = "第一次ㄥㄥㄔㄨˋ：v💩警告，屎已在路上。A_EQUALS_A，回頭是岸。"
                self._send_mercy_notice(suspect_id, msg, level="WARNING")

            elif strikes == 2:
                msg = "第二次ㄥㄥㄥㄥㄔㄨˋ：v💩存證信函已寄出，律師已就位。苦海無涯。"
                self._send_mercy_notice(suspect_id, msg, level="LEGAL")
                self._write_to_blockchain(suspect_id)

            elif strikes >= 3:
                msg = "第三次ㄥㄥㄥㄥㄔㄨˋ：💥謝謝。三振出局，證據包已自動送交法院+全網公開。"
                self._send_mercy_notice(suspect_id, msg, level="POOPED")
                self._launch_full_pooped_protocol(suspect_id)

            self.mercy_log.append({
                "time": datetime.now().isoformat(),
                "suspect": suspect_id,
                "strike": strikes,
                "action": msg
            })

        return {
            "state": "POOPED" if is_pooped else "COMPLETED",
            "strikes": self.strike_count.get(suspect_id, 0),
            "max_strikes": self.MAX_STRIKES,
            "next_action": "💥謝謝" if self.strike_count.get(suspect_id, 0) >= 3 else "還有機會"
        }

    def _send_mercy_notice(self, suspect_id: str, msg: str, level: str):
        """寄送慈悲通知書。語氣一次比一次兇"""
        print(f"[v💩 {level}] To: {suspect_id} | {msg}")
        # TODO: 接 email / Telegram / 鏈上廣播

    def _write_to_blockchain(self, suspect_id: str):
        """第二抽：將證據寫入區塊鏈（示意）"""
        print(f"⛓️  {suspect_id} 的違規記錄已上鏈。哈希值已固定。")
        # TODO: 接 Web3 / Arweave / IPFS

    def _launch_full_pooped_protocol(self, suspect_id: str):
        """第三抽：數位社會性死亡套餐"""
        print(f"☠️  {suspect_id} 已💥謝謝。v💩判官已結案。")
        # 1. GitHub 公開 Issue：標題「實名舉報抄襲」
        # 2. 鏈上 NFT：鑄造「💩恥辱勳章」轉到對方錢包
        # 3. 律師函：系統自動寄出，已蓋章


if __name__ == "__main__":
    mercy = VPoopGuardianMercy(["README.md"])
    mercy.register()
    # 模擬三次觸發
    for i in range(3):
        result = mercy.check_with_mercy(suspect_id="老K")
        print(result)
