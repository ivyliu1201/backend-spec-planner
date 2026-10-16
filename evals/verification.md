# 驗證指南

在專案根目錄執行。專案內 Python 指令僅使用標準函式庫，檢查失敗時回傳非零退出碼。

## 文件與證據

~~~powershell
python -B evals/verify.py
git diff --check
~~~

- 檢查 UTF-8、相對連結、錨點、案例結構、封存內容及結果檔雜湊。
- 封存清單見 [SHA-256 紀錄](evidence/2026-10-16-redesign.json)。
- 這些檢查確認文件與證據完整性；模型行為依[現行案例](cases.md)另行評估。

若環境已提供 Codex 官方驗證器，可另執行：

~~~powershell
python -X utf8 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .
~~~

官方驗證器檢查 Skill 格式，需要其既有環境與依賴；未執行時如實記錄。

## 重跑開發交接驗收

[封存檔](evidence/2026-10-16-redesign.zip)保存原版與變更後程式、原始驗收腳本及當時證據。每次解壓至新的工作目錄：

~~~powershell
$evalRun = Join-Path "evals/.runs" ("redesign-" + [guid]::NewGuid().ToString("N"))
python -m zipfile -e evals/evidence/2026-10-16-redesign.zip $evalRun
python -B "$evalRun/evaluate.py" "$evalRun/implementation/original-baseline"
python -B "$evalRun/evaluate.py" "$evalRun/implementation" --changed
~~~

- 先通過文件與證據檢查，再重跑；每項指令應正常結束。
- 兩版各驗證 25 項，涵蓋 CLI 結果、輸入錯誤、來源不變、單次走訪及記憶體門檻。
- 腳本自行產生測試 CSV；每輪輸出新的 report.json 路徑，既有封存及結果檔不變。
- 原版與變更後的歷史結果分別見[原版報告](results/2026-10-16-original.json)、[變更報告](results/2026-10-16-changed.json)；量測值依環境變動。
- 此流程重跑已保存程式的驗收，不重演模型生成或原始 TDD 過程，也不代表現行 Skill 全案例通過。

## 封存內容

| 檔內位置 | 內容 |
| --- | --- |
| baseline/、revised/、final/ | 當時 Skill 快照、相同需求與三輪生成規格 |
| batch/ | 批次需求、契約及生成文件 |
| implementation/ | 變更後程式、測試、規格與歷史日誌 |
| implementation/original-baseline/ | 原版程式、規格及雜湊 |
| evaluate.py | 評估者獨立驗收指令 |
| style-before.json | 精簡前字元數 |

- 排除可重建的 CSV、量測暫存檔及 Python 快取。
- 歷史日誌中的絕對路徑僅記錄當時環境，重跑不依賴該路徑。
- 批次與效能訪談未留下完整對話逐字稿；保留原有結果摘要，不能由封存檔重演訪談。

## 證據保存

- 執行資料置於 evals/.runs/，已排除 Git 追蹤。
- 選定結果保存至 evals/results/；必要輸入、快照、指令與日誌封存至 evals/evidence/，按日期及用途命名。
- 記錄日期、案例、版本或內容雜湊、指令、環境、結果與未驗證範圍；結果摘要連結實際證據。
- 封存後保留原內容；新驗證另建紀錄及雜湊清單，不覆寫歷史檔案。
