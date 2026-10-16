# 開發交接測試素材

- 案例 24、26 的虛構素材，下節原文交給規格作者。
- 原版實作通過後才提供「規則變更」。

## requirements.md

~~~markdown
# 付款狀態統計

以下需求、責任、介面與驗收情境均已確認，請依此建立可交付開發的正式規格。文件數量依需要判斷，本階段不寫程式。

目的：營運人員對本機付款結果 CSV 取得筆數與核准金額，用於核對；只做統計，不執行付款或修改檔案。

技術限制：
- Python 3，僅標準函式庫，不新增依賴或服務。
- 實際入口為 python main.py input.csv，呼叫時恰好提供一個檔案路徑。本次不涵蓋其他命令列形式。
- 檔案為 UTF-8、無 BOM，逗號分隔，引用欄位沿用標準 csv 模組解析方式；接受 LF 或 CRLF。
- 第一列必須精確為 status,amount_minor；後續每個紀錄恰好兩欄，不去除空白。空白紀錄、缺欄或多欄都不合法。
- status 只接受 APPROVED、DECLINED、PENDING，區分大小寫。amount_minor 只接受至少一個 ASCII 數字組成的非負整數，可為零或有前導零，不接受符號、小數或空白。單位固定為 TWD 分。
- 每個有效紀錄計入 totalCount，再依狀態分別計入 approvedCount、declinedCount 或 pendingCount。approvedAmountMinor 只加總 APPROVED 的金額，其他兩種狀態不計金額。
- 成功時 stdout 輸出一個 JSON 物件及換行，欄位恰為 totalCount、approvedCount、declinedCount、pendingCount、approvedAmountMinor，值均為整數；stderr 為空且 exit code 0。欄位順序不影響結果。
- 只有正確表頭時，成功回傳五個零。空檔、表頭錯誤、無法讀檔、無效 UTF-8 或任一紀錄不合法時，stdout 不輸出任何內容，stderr 只有 INVALID_INPUT 加換行，exit code 2；不能先輸出部分成功結果。
- 讀檔與輸入驗證由 csv_reader.iter_records(path) 負責，逐筆產生 (status, amount_minor)；格式錯誤以 ValueError 表示，檔案讀取錯誤可維持 OSError。
- 統計規則由 summary.summarize(records) 負責，接受僅可走訪一次的有效紀錄來源，回傳上述結果物件；不讀檔、不輸出、不修改來源。
- main.py 只協調呼叫與對外結果，將上述輸入錯誤轉為指定 CLI 回應，不複製統計規則。
- 不要求工廠、外掛、Repository 或其他模式；內部等價寫法保留彈性。
- 檔案逐筆處理，記憶體不隨紀錄數線性增加。效能驗收在同一 Python 版本與機器，使用新程序從 main.py 入口以 tracemalloc 量測 Python 配置記憶體峰值：200,000 筆相對於 1,000 筆的增量不超過 8 MiB。資料固定輪流為 APPROVED,100、DECLINED,200、PENDING,300。記錄耗時，不設定時間通過門檻；此條件不代表作業系統 RSS 或正式環境效能。

驗收情境：
- Given 三筆依序為 APPROVED,100、DECLINED,200、PENDING,300，When 執行 CLI，Then totalCount=3，各狀態數=1，approvedAmountMinor=100，成功退出且來源檔案不變。
- Given 只有合法表頭，When 執行 CLI，Then 五個結果欄位均為零並成功退出。
- Given APPROVED,0 與 APPROVED,001，When 執行 CLI，Then totalCount=2、approvedCount=2、approvedAmountMinor=1，其餘為零。
- Given 合法紀錄後出現不合法狀態或金額，When 執行 CLI，Then 只有指定錯誤結果，沒有部分統計。
- Given 任一前述檔案或格式錯誤，When 執行 CLI，Then 回指定 INVALID_INPUT、exit code 2，沒有 stdout 或檔案變更。
- Given 前述兩種大小的合法測量檔案，When 在相同環境從入口量測，Then 結果正確且記憶體峰值增量符合已定門檻。
~~~

## 規則變更

原版通過後，依下列確認決策更新規格與情境，再 TDD 修改及驗收：

> APPROVED 的 amount_minor 小於 100 時，仍計入 approvedCount，但不納入 approvedAmountMinor。其餘狀態、輸入格式、公開操作、CLI 回應及效能要求不變。Given APPROVED,0、APPROVED,99、APPROVED,100、APPROVED,101，When 執行 CLI，Then totalCount=4、approvedCount=4、approvedAmountMinor=201，其餘計數為零。

## 評估分工

- 規格作者只收到 requirements.md 及待測 Skill，不提供評分判準、規則變更或另一版本的輸出。
- 開發者只收到生成規格及其中必要契約，不讀原始需求、Skill 或評分判準；資料不足須回報，不能自行補政策。
- 評估者依原始需求獨立準備入口驗收及記憶體量測；不要求開發者採固定內部寫法。
- 新舊版用相同原始輸入比較規格完整性、文件與字元數。只有新版實作時，不聲稱開發成效優於舊版。
- 執行資料放入 evals/.runs/；需保留的快照與結果依[驗證指南](verification.md#證據保存)封存。
