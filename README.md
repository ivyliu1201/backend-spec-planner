<div align="center">

# backend-spec-planner

**後端規格分析、設計與修訂的 Codex Skill**

依據需求、既有文件與程式證據，整理業務行為、模組責任及操作契約。  
固定核心結構，按需深入細節，用可讀敘述表達精確規格。

[適用情境](#適用情境) · [安裝方式](#安裝方式) · [使用範例](#使用範例) · [工作流程](#工作流程) · [文件產出](#文件產出) · [生成示例](#生成示例) · [驗證狀態](#驗證狀態)

</div>

## 適用情境

- **建立規格**：從需求敘述整理用例、業務規則、例外與驗收情境。
- **修訂既有文件**：分析現有 spec 的缺口，沿用原有結構調整受影響內容。
- **規格審查**：檢查行為、設計、契約與責任分工是否一致。
- **逆向整理**：依既有入口與相關程式描述目前行為，區分實作現況與已確認需求。

涉及領域與模組設計時，協助分析 DDD（領域驅動設計）、模組協作及設計模式的適用性；涉及銀行批次或檔案處理時，再檢查格式、重送、防重、交易與恢復等細節。

## 安裝方式

本專案由指令、參考文件與模板組成，沒有套件安裝、建置或服務啟動步驟。

1. 將完整 Skill 內容放在名為 `backend-spec-planner` 的資料夾中。本儲存庫根目錄已是 Skill 根目錄，`SKILL.md` 應直接位於其中。
2. 依使用範圍選擇放置位置：

   | 使用範圍 | 路徑 |
   | --- | --- |
   | 個人使用，跨專案共用 | `~/.codex/skills/backend-spec-planner/` |
   | 僅供指定專案使用 | `<專案根目錄>/.codex/skills/backend-spec-planner/` |

   `~` 代表使用者家目錄。保留 `agents/`、`references/`、`assets/` 與 `evals/` 的相對位置。

3. 在 Codex 開啟目標專案，確認 Skill 已出現在可用清單；若未出現，可重新啟動 Codex。

位置與使用方式依 [Codex 官方 Skills 文件](https://learn.chatgpt.com/docs/build-skills)整理。本 Skill 設定為明確呼叫，使用 `$backend-spec-planner` 啟動；實際宿主驗證狀態見下方說明。

## 使用範例

### 修訂既有規格

指定文件與目的即可開始，不必先選模板或決定文件數量：

```text
$backend-spec-planner
請分析並調整 docs/spec.md，沿用既有結構。
涉及新的業務決策時，先提出建議讓我確認。
```

### 建立正式規格

```text
$backend-spec-planner
請依需求文件建立批次結果查詢的正式規格。
必要問題先在對話中一題一題問清楚，再產出完整文件。
```

### 審查規格一致性

```text
$backend-spec-planner
請審查 docs/specs/payroll/ 的規格與設計。
重點檢查模組責任、受理與完成條件、重試及失敗處理，只回報，不修改。
```

### 逆向整理現有行為

```text
$backend-spec-planner
請從既有批次提交入口及相關契約整理目前規格，
保留文件與程式之間的差異，區分實作現況與已確認需求。
```

上述路徑與功能名稱均為示例，可依專案調整。同一規格任務的後續對話可直接補充需求或回覆決策，不必重複呼叫名稱。

## 工作流程

| 處理環節 | 主要內容 |
| --- | --- |
| 範圍與來源確認 | 讀取指定文件、適用規則及直接相關的依據 |
| 缺口與影響分析 | 判斷哪些歧義會改變業務結果、契約、資料一致性或責任 |
| 必要證據查核 | 資料不足、逆向分析或涉及模組／契約時，才追查相關來源 |
| 必要訪談 | 先說明推薦、理由與影響，每次問一題，收到答案再繼續 |
| 內容撰寫與修訂 | 必要決策齊備後，依固定結構產出正式規格 |
| 一致性檢查與交付 | 核對受影響規則、設計、引用及驗收情境，回報修改與檢查範圍 |

- 資料已充分時直接撰寫，不重問已有答案，也不為等價的內部寫法訪談。
- 正式規格直接描述行為、責任與設計理由；問題與選項留在對話，必要的來源引用仍保留。
- 明確要求先看草案時才交草案；只審查時在對話回報發現。

流程與授權邊界見 [SKILL.md](SKILL.md#需求訪談)。

## 文件產出

**文件數量依實際需求決定。** 修改一份既有 `spec.md`，通常仍只修改該檔；審查任務則在對話中回報。沒有既有位置慣例時，才使用 `docs/specs/`。

新建文件依各模板的固定核心章節與順序撰寫，條件式細節依模板中的適用條件展開：

| 文件類型 | 何時需要 |
| --- | --- |
| [Feature Spec](assets/templates/spec.md) | 定義功能行為、規則、例外與驗收情境，通常從此開始 |
| [Feature Design](assets/templates/design.md) | 功能需要約束模組責任、互動、契約對應與重要實作決策 |
| [System Context](assets/templates/system-context.md) | 多個功能共用系統背景、術語、領域關係與規則 |
| [Module Catalog](assets/templates/module-catalog.md) | 需要整理可重用的模組能力、協作及替代選用依據 |
| [Module Contract](assets/templates/module-contract.md) | 共用操作缺少足夠契約或使用限制；已有完整契約時優先引用 |

- 日常以 Spec 與 Design 為主；另外三種按共用需求選用，已有足夠文件就引用。
- 同類文件核心固定；相關內容合併閱讀，不同責任分開。條件式細節不適用時省略。
- 資訊不足先依訪談流程釐清；無適用內容的核心章節則簡述原因。
- 局部修訂沿用原結構；整份格式統一須區分格式與業務行為變更。

Feature Spec 以六個核心章節描述功能，其中「輸入、輸出與完成條件」集中說明操作的起點與結果。Feature Design 保留「設計依據、責任分工、執行流程、資料對應」；模型、交易與恢復等細節依適用性展開。理由寫在相關內容，需集中說明取捨時才另設「設計決策」。

Module Contract 以「模組職責、操作說明」組織。已有完整契約時，保留引用與簡短使用說明；缺少定義時，才按需補充呼叫條件、輸入、結果、錯誤及限制。

## 生成示例

以下「曙光企業」與「批次 B-042」都是虛構資料，政策只示範寫法，不代表銀行共用規範。B-042 是顯示代號，實際操作使用該批次的 UUID。為便於閱讀，這裡節錄同一用例的 Spec 與 Design；正式文件仍保留模板的完整核心章節。

### 示例素材與契約

本例的訪談已完成，以下是用於展示的素材；業務政策集中在 BR-Q-001 定義。

- 能力目錄：`BatchQuery` 提供結果查詢；`FileStore` 只保存原始檔，兩者不互為替代。
- 操作契約：`BatchQuery v1 / getResult(actorContext, batchId)` 接受可信登入脈絡與 UUID 批次識別，成功回傳同一時點的狀態及成功、失敗筆數。
- 使用限制：模組負責權限與企業範圍檢查；儲存服務不可用時回傳 `Unavailable`，不自動重試。

### Feature Spec 片段

**功能概述**

企業經辦提交批次後，需要查詢目前結果，以安排後續核對。

- 開始：已登入經辦從查詢入口提供批次識別。
- 範圍：本功能只查詢結果，不執行付款或重新處理批次。

技術細節見 [Feature Design 片段](#feature-design-片段)。

本例規則與情境的共同依據為上方[示例素材與契約](#示例素材與契約)。

**輸入、輸出與完成條件**

- 輸入：登入脈絡與批次識別。
- 輸出：所屬企業批次的目前狀態及成功、失敗筆數。
- 完成條件：取得查詢結果即完成本次查詢，不代表批次處理已完成。

**業務規則 — BR-Q-001：企業範圍內查詢**

- 經辦具備 `result:read` 權限時，只能取得所屬企業的批次結果。
- 缺少權限時回傳 403；跨企業與不存在的批次均回傳 404，且不揭露批次內容。
- 所有查詢均不得改變批次資料。

**處理流程**

1. 經辦從結果查詢入口提供批次識別，系統先依 BR-Q-001「企業範圍內查詢」檢查資格。
2. 檢查通過後取得結果並呈現；拒絕時即結束查詢，不進入結果呈現步驟。

**驗收情境 — BDD-Q-002：跨企業查詢不揭露資料**

- **Given** 曙光企業經辦具備查詢權限，而批次 B-042 屬於另一企業。
- **When** 經辦從查詢入口要求 B-042 的結果。
- **Then** 系統回傳 404，不揭露狀態與筆數，批次資料維持不變。

### Feature Design 片段

**責任分工**

依[示例能力目錄](#示例素材與契約)，本功能使用既有 `BatchQuery.getResult`：

- `BatchQuery` 負責 BR-Q-001 的權限與資料範圍判定。
- 查詢入口負責傳遞可信登入脈絡及呈現結果。
- `FileStore` 的原始檔儲存能力不參與此用例。
- 選用理由：企業資料範圍由既有模組統一判定，避免入口另維護一套規則；代價是模組不可用時，本功能也無法查詢。

**資料對應**

引用 [BatchQuery v1 的 getResult 契約](#示例素材與契約)，此處只記錄本功能如何使用：

| 契約資料 | 本功能對應 |
| --- | --- |
| `actorContext` | 取自已驗證登入脈絡；企業識別不採用請求自行填入的值 |
| `batchId` | 取自查詢入口的批次識別，依契約驗證 |
| 狀態與筆數／錯誤 | 成功結果直接呈現；403、404 保留契約定義的結果；Unavailable 呈現查詢暫時無法完成，不觸發批次重跑 |

本例已在責任分工交代選用理由，無須另設決策章節。

## 文件導覽

| 路徑 | 職責 |
| --- | --- |
| [SKILL.md](SKILL.md) | 任務範圍、分析流程、參考文件載入條件與模板選用 |
| [agents/openai.yaml](agents/openai.yaml) | 顯示名稱、起始提示與明確呼叫設定 |
| [references/authoring-rules.md](references/authoring-rules.md) | 共用撰寫判準：顆粒度、可讀性、去重、來源引用與一致性 |
| [references/ddd-design.md](references/ddd-design.md) | 領域模型、模組責任、協作／替代選用及設計模式 |
| [references/batch-processing.md](references/batch-processing.md) | 批次與檔案處理的專門檢查項目 |
| `assets/templates/` | 上方五種文件的起始結構與填寫欄位 |
| [evals/cases.md](evals/cases.md) | 維護時使用的行為評估案例 |
| README.md | 使用說明、文件索引及設計來源 |

使用者提供需求或文件即可；Skill 按需載入準則及模板。BDD（行為驅動開發）以 Given／When／Then 描述驗收情境，實際測試結果另行記錄。

## 驗證狀態

2026-10-16 驗證結果：

- 官方 Python 驗證器與結構檢查通過，涵蓋 13 份 Skill 文件、設定語法、本地引用、五種模板及 23 個案例欄位。
- 獨立模型對話完成案例 16、19、21、23：相同輸入一致性、複雜批次、逐題訪談及契約引用／補充。
- 批次首輪發現未有契約支援的狀態保存假設；補強核對後，以相同原始材料重測，模型先詢問缺少的操作，取得補充後才完成正式文件。
- 本輪其餘 19 個案例未重跑；未測宿主安裝／觸發、真人可讀性與銀行系統執行。生成 BDD 不等於產品測試通過。

實際結果及歷史紀錄見[執行紀錄](evals/cases.md#執行紀錄)。

## 設計來源

本 Skill 參考下列方法，並保留適合規格工作的部分；使用時不依賴這些工具。

<details>
<summary>方法來源與採用範圍</summary>

| 官方來源 | 採用的方法與本 Skill 對應 |
| --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | SKILL.md 的 name／description、相對資源引用、逐步揭露；主檔導航、references 規則、assets 模板 |
| [Codex Skills](https://learn.chatgpt.com/docs/build-skills) | 專案 Skill 位置、openai.yaml 與明確觸發設定 |
| [OpenSpec 專案](https://github.com/Fission-AI/OpenSpec)、[Project configuration](https://openspec.dev/docs/project-config)、[Schemas](https://openspec.dev/docs/customize-schemas) | 共用背景、文件專屬規則、可客製模板與 spec／design 分工，分別落在背景模板、references 與各文件模板 |
| [Spec Kit 官方說明](https://github.com/github/spec-kit) | 共用原則與「先 what／why，再 how」的責任分離，對應 System Context、Spec 與 Design |
| [arc42 overview](https://arc42.org/overview/)、[Building Block View](https://docs.arc42.org/section-5/) | 黑箱責任與重要模組逐層展開，配合 Runtime View、Crosscutting Concepts、Architecture Decisions，落在目錄、Design 與 DDD 檢查 |
| [Context Mapper](https://contextmapper.org/)、[Bounded Context](https://contextmapper.org/docs/bounded-context/)、[Context Map](https://contextmapper.org/docs/context-map/) | 術語／模型適用邊界、責任及上下文整合關係，落在背景與領域設計 |

模板與規則依本專案需求撰寫，未複製上游完整模板。

</details>

README 編排參考 [reverse-domain-discovery](https://github.com/ivyliu1201/reverse-domain-discovery)。
