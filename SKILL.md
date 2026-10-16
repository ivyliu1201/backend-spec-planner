---
name: backend-spec-planner
description: "僅在明確呼叫 $backend-spec-planner 時，依需求、文件或程式證據建立、修訂、逆向整理或審查後端規格；涵蓋行為、責任、契約與驗收，批次及複雜設計按需展開。"
---

# Backend Spec Planner

將需求轉為精煉、可開發及可驗收的後端規格。

## 適用範圍

- 明確呼叫 $backend-spec-planner 或延續同一規格任務時使用。
- 依授權分析、審查或修改。變更已確認的行為、模組、階段或責任前，說明原因、影響與方案並取得同意。
- 功能決策限於指定範圍；規格完成不授權自動開發。

## 工作流程

1. 讀取適用的 AGENTS.md、需求及相關規範，確認範圍。
2. 依相關入口與契約查證；必要時深入實作及測試。
3. 依[驗收準則](references/authoring-rules.md#驗收)釐清情境，完成必要訪談。
4. 定義責任、契約與品質約束；沿用既有架構，設計方法按需選用。
5. 撰寫最少必要文件，核對[完整性](references/authoring-rules.md#完整性)與[開發交接](references/authoring-rules.md#開發交接)，回報位置、修改及驗證範圍。

## 需求訪談

- 缺口影響業務結果、驗收、契約、責任或授權時，先確認再產出正式規格。
- 每次只問最重要的一題，附推薦、理由與影響。
- 已確認答案不重問；等價內部寫法及局部編排自行處理。
- 等待時可處理無依賴內容；必要答案未齊不交付正式規格，沉默或預選不算同意。
- 草案、分析、審查及逆向整理依委託交付，來源處理見[依據](references/authoring-rules.md#依據)。

## 參考資料

按任務載入，局部文字修訂只核對受影響內容。

| 內容 | 文件 |
| --- | --- |
| 撰寫、來源、驗收及交接 | [authoring-rules.md](references/authoring-rules.md) |
| 責任、契約、方法及效能 | [design-rules.md](references/design-rules.md) |
| 批次與檔案處理 | [batch-processing.md](references/batch-processing.md) |

## 文件選用

- 沿用專案位置與模板；無慣例時使用 docs/specs/ 及下列模板。
- 模板提供建議順序，依用途合併或省略章節。
- 修訂保留既有結構；格式調整與行為變更分開回報。
- 交付移除模板提示、註解及佔位符，引用指向實際來源。

| 文件 | 使用時機 |
| --- | --- |
| [Feature Spec](assets/templates/spec.md) | 預設交付，包含行為、必要設計與驗收 |
| [Feature Design](assets/templates/design.md) | 設計需詳細展開，或使用者指定拆分；Spec 保留行為與驗收 |
| [System Context](assets/templates/system-context.md) | 多功能共用背景、術語及規則 |
| [Module Catalog](assets/templates/module-catalog.md) | 共用模組能力與選用依據 |
| [Module Contract](assets/templates/module-contract.md) | 共用操作契約不足；已有完整定義直接引用 |

使用說明見 [README.md](README.md)；維護或評估時才讀 [evals/cases.md](evals/cases.md)。
