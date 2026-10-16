---
name: backend-spec-planner
description: "僅在使用者明確呼叫 $backend-spec-planner 時，依指定範圍分析、建立、逆向整理、深化、審查或調整後端系統規格；涵蓋業務行為、DDD、模組選用與契約，以及銀行批次檔案處理。交付規格內容、設計建議與核對結果。"
---

# Backend Spec Planner

依指定範圍分析、撰寫或審查後端規格。固定核心結構，按需深入細節。

## 適用範圍

- 僅在明確呼叫 `$backend-spec-planner` 的規格任務及續談使用；需求敘述、文件或程式路徑即可開始。
- 審查只回報，修改須有授權。保留已確認的行為、模組、階段與責任；調整前說明原因、影響與方案並取得同意。
- 單一功能的決策只適用於指定範圍；規格完成不代表取得開發許可。

## 工作流程

1. 讀取適用的 AGENTS.md、需求、指定文件及直接相關的規範，確認範圍。
2. 逆向分析、資料不足或涉及責任／契約時，沿相關入口與公開契約查證；仍有重要歧義才深入實作及測試。
3. 選用模組時，先讀能力目錄，判斷協作或替代關係，選定操作，再讀必要契約。契約不符時回查候選；無目錄則從相關來源辨識能力。
4. 依下節完成必要訪談，再撰寫規格。有充分依據的局部修訂可直接處理。
5. 核對受影響內容與引用，交付文件位置、修改摘要及驗證範圍。

新內容由業務情境、行為與規則逐層深入責任、模組及操作契約；細節是否充分依[完整性](references/authoring-rules.md#完整性)判斷。

## 需求訪談

- 預設交付正式規格。缺口會改變業務結果、驗收、公開契約、責任或授權時，先釐清再生成。
- 每次只問最影響結果的一題，先說明推薦、理由與影響，收到回答後再繼續。
- 已有答案不重問；等價內部寫法與局部編排自行處理。
- 等待時可查證或整理無依賴內容；必要決策未定前不交付帶缺口的規格，也不以沉默或預選代替回答。
- 明確要求草案、分析、審查或逆向現況時，依委託交付；來源與正式文件寫法依[撰寫準則](references/authoring-rules.md#依據)。

## 資料載入

依本次需要讀取；純文字整理只核對受影響內容與引用。

| 判斷內容 | 資源 |
| --- | --- |
| 完整性、編排、引用與去重 | [authoring-rules.md](references/authoring-rules.md) |
| 領域責任、模組選用與設計取捨 | [ddd-design.md](references/ddd-design.md) |
| 批次與檔案處理 | [batch-processing.md](references/batch-processing.md) |

## 文件選用

沿用既有命名、位置與文件邊界；無慣例時使用 `docs/specs/`。只建立本次需要的文件。

- **新建**：沿用團隊模板；沒有時使用下列模板。核心名稱與順序固定，條件式內容按適用條件展開；章節依[編排準則](references/authoring-rules.md#編排)劃分責任。
- **修訂**：保留原結構，只改受影響內容。整份格式統一須區分格式整理與業務行為變更。
- **省略**：核心不適用時簡述原因，條件式內容不適用可省略。影響結果的未知事項依訪談流程解決。

| 文件 | 責任 |
| --- | --- |
| [Feature Spec](assets/templates/spec.md) | 功能行為、業務規則與驗收 |
| [Feature Design](assets/templates/design.md) | 責任、互動、資料對應與實作約束 |
| [System Context](assets/templates/system-context.md) | 共用背景、術語、領域關係與規則 |
| [Module Catalog](assets/templates/module-catalog.md) | 模組能力、協作及替代選用 |
| [Module Contract](assets/templates/module-contract.md) | 操作用途、呼叫條件、回應及限制；已有契約引用，不足處補齊 |

交付前移除模板提示、註解與佔位符，引用改為實際文件位置，依撰寫準則完成核對。

使用說明見 [README.md](README.md)。僅維護或評估本 Skill 時讀取 [evals/cases.md](evals/cases.md)。
