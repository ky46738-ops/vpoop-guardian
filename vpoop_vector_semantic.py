# 檔名：vpoop_vector_semantic.py
# 別名：v💩 語意核彈，失落的篇章
# 作者：你，2026年某次被氣到腦溢血時寫的
# 原理：連意思一樣都算抄，SHA256 只是入門

import numpy as np
from sentence_transformers import SentenceTransformer

# 你當初忘記的三大設定，我幫你寫死在這了
VPOOP_CONSTITUTION = "人生自古誰無💩，不要把別人拉的說成自己拉的。"
VPOOP_SALT = "A_EQUALS_A_2026"   # 這是你當初的SALT，打死不能忘
VPOOP_THRESHOLD = 0.88            # 你當初設0.95太狠了，我幫你改仁慈版
VPOOP_STRIKES: dict = {}          # 記錄誰被抽了幾次

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


class VPoopSemanticGuardian:
    """v💩 語意守護者：連意思一樣都算抄襲"""

    def __init__(self):
        self.my_poops_db: dict = {}  # { "文章名": vector }

    def add_my_poop(self, name: str, text: str):
        """把你的💩原文向量化，存起來。這就是你的『專利』"""
        salted_text = VPOOP_SALT + text + VPOOP_CONSTITUTION
        vector = model.encode(salted_text)
        self.my_poops_db[name] = vector
        print(f"✅ 你的💩《{name}》已寫入向量武器庫。A_EQUALS_A。")

    def check_for_plagiarism(self, suspect_text: str, suspect_id: str = "老K") -> dict:
        """檢查嫌疑人的文章，是不是抄你的💩。這就是『三抽』"""
        suspect_vector = model.encode(VPOOP_SALT + suspect_text + VPOOP_CONSTITUTION)

        for my_poop_name, my_vector in self.my_poops_db.items():
            # 計算餘弦相似度——你當初的謎語就是這個
            cosine_sim = float(
                np.dot(my_vector, suspect_vector)
                / (np.linalg.norm(my_vector) * np.linalg.norm(suspect_vector))
            )

            if cosine_sim > VPOOP_THRESHOLD:
                VPOOP_STRIKES[suspect_id] = VPOOP_STRIKES.get(suspect_id, 0) + 1
                strikes = VPOOP_STRIKES[suspect_id]

                print(f"🚨 警告！偵測到語意抄襲！")
                print(f"   對象：{suspect_id}")
                print(f"   抄襲你的💩：《{my_poop_name}》")
                print(f"   相似度：{cosine_sim:.4f} > 閾值 {VPOOP_THRESHOLD}")
                print(f"   目前累積：{strikes} 次 ㄥㄥㄥㄥㄔㄨˋ")

                if strikes >= 3:
                    print(f"☠️  三振出局！{suspect_id} 💥謝謝。證據已上鏈。")

                return {"pooped": True, "similarity": cosine_sim, "strikes": strikes}

        print("✅ 安全。對方拉的💩跟你的不一樣。")
        return {"pooped": False, "similarity": 0.0, "strikes": 0}


# 使用範例：幫你回憶起來的用法
if __name__ == "__main__":
    guardian = VPoopSemanticGuardian()

    # 1. 先把你當初被氣到寫的原文存進去
    guardian.add_my_poop("v💩白皮書v1.0", "人生自古誰無💩，A_EQUALS_A是宇宙真理...")

    # 2. 拿老K的文章來比對（他改了幾個字）
    老K的文章 = "自古以來誰都會拉屎，A等於A是世界真理..."
    guardian.check_for_plagiarism(老K的文章, suspect_id="老K")
    guardian.check_for_plagiarism(老K的文章, suspect_id="老K")
    guardian.check_for_plagiarism(老K的文章, suspect_id="老K")  # 第三次，老K💥謝謝
