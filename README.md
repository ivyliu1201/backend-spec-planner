<div align="center">

# backend-spec-planner

**產出精煉、可交付開發的後端規格**

依需求與專案證據，定義行為、責任、契約與驗收。<br>
簡單功能以一份規格交付，設計按需展開。

[適用情境](#適用情境) · [安裝方式](#安裝方式) · [使用範例](#使用範例) · [工作流程](#工作流程) · [文件產出](#文件產出) · [生成示例](#生成示例) · [驗證狀態](#驗證狀態)

</div>

## 適用情境

- **建立規格**：從需求敘述整理用例、業務規則、例外與驗收情境。
- **修訂既有文件**：分析現有 spec 的缺口，沿用原有結構調整受影響內容。
- **規格審查**：檢查行為、設計、契約與責任分工是否一致。
- **逆向整理**：依既有入口與相關程式描述目前行為，區分實作現況與已確認需求。

## 安裝方式

本專案包含指令、參考文件與模板，無須安裝套件或啟動服務。

1. 將完整內容放入 `backend-spec-planner/`，`SKILL.md` 直接位於根目錄。
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

指定文件與目的即可開始：

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

路徑與名稱依專案調整；同一任務續談無須重複呼叫 Skill。

## 工作流程

1. 確認範圍與來源。
2. 查核相關入口、契約及需求缺口。
3. 逐題確認必要決策與情境。
4. 產出正式規格及必要設計。
5. 核對完整性與開發交接。

流程與授權見 [SKILL.md](SKILL.md)；草案及審查依委託交付。

## 文件產出

- 新功能預設一份 [Feature Spec](assets/templates/spec.md)，涵蓋行為、必要設計及驗收。
- 設計及共用文件的用途、位置與選用條件見[文件選用](SKILL.md#文件選用)。

撰寫與去重依[規格撰寫準則](references/authoring-rules.md)。規格完成後，開發須有授權，再以確認情境進行 TDD（測試驅動開發）及入口驗收。

## 生成示例

以下為虛構規格節錄；正式交付須引用實際契約，並補齊必要驗收情境。

### 批次結果查詢

**目的與範圍**

企業經辦查詢已提交批次的目前結果，以安排核對。本功能到查詢結果交付為止。

**行為與規則**

- 已登入經辦從查詢入口提供 UUID 批次識別。
- 先檢查 result:read 權限，缺少時回 403；具權限者只能查詢所屬企業，跨企業與不存在均回 404。
- 成功回傳同一時點的狀態、成功數與失敗數；查詢完成不代表批次已終局。
- 儲存不可用回 503，不自動重試。所有查詢都不修改批次或觸發重跑。

**責任與契約**

- 查詢入口傳遞已驗證的登入脈絡及批次識別，呈現結果。
- BatchQuery.getResult 擁有權限與企業範圍判定；企業識別取自登入脈絡，不採用請求自行填入的值。
- 輸入、快照及錯誤型別沿用 BatchQuery v1 契約；本功能將 Unavailable 對應為 HTTP 503。

**驗收情境：跨企業不揭露資料**

- **Given** 曙光企業經辦具查詢權限，目標批次屬於另一企業。
- **When** 從查詢入口要求該批次結果。
- **Then** 回 404，不揭露狀態與筆數，批次資料維持不變。

## 文件導覽

| 路徑 | 職責 |
| --- | --- |
| [SKILL.md](SKILL.md) | 任務範圍、分析流程、參考文件載入條件與模板選用 |
| [agents/openai.yaml](agents/openai.yaml) | 顯示名稱、起始提示與明確呼叫設定 |
| [references/authoring-rules.md](references/authoring-rules.md) | 完整性、可讀性、去重、來源、BDD 與開發交接判準 |
| [references/design-rules.md](references/design-rules.md) | 責任、契約、方法選用與效能設計 |
| [references/batch-processing.md](references/batch-processing.md) | 批次與檔案處理的專門檢查項目 |
| `assets/templates/` | 功能規格及按需文件的起始結構 |
| [evals/cases.md](evals/cases.md) | 維護時使用的行為評估案例 |
| README.md | 使用說明、文件索引及設計來源 |

## 驗證狀態

- 現行判準：[評估案例](evals/cases.md)；指令與證據保存：[驗證指南](evals/verification.md)。
- 執行結果：[改版驗證](evals/redesign-results.md)、[歷史紀錄](evals/history.md)，依當時版本解讀。
- 模型評估、真人閱讀與正式環境驗收分開記錄。

## 設計來源

以下為方法參考，非工具依賴。

<details>
<summary>方法來源與採用範圍</summary>

| 來源 | 採用範圍 |
| --- | --- |
| [Cucumber BDD](https://cucumber.io/docs/bdd/)、[TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html) | 情境確認、測試與實作交接 |
| [Agent Skills specification](https://agentskills.io/specification) | Skill 結構、資源引用與按需載入 |
| [Codex Skills](https://learn.chatgpt.com/docs/build-skills) | 安裝位置、顯示與觸發設定 |
| [OpenSpec 專案](https://github.com/Fission-AI/OpenSpec)、[Project configuration](https://openspec.dev/docs/project-config)、[Schemas](https://openspec.dev/docs/customize-schemas) | 共用背景、文件分工與模板 |
| [Spec Kit 官方說明](https://github.com/github/spec-kit) | 行為與設計分工 |
| [arc42 overview](https://arc42.org/overview/)、[Building Block View](https://docs.arc42.org/section-5/) | 模組責任、互動與設計決策 |
| [Context Mapper](https://contextmapper.org/)、[Bounded Context](https://contextmapper.org/docs/bounded-context/)、[Context Map](https://contextmapper.org/docs/context-map/) | 術語、模型邊界與整合關係 |

模板與規則依本專案需求撰寫，未複製上游完整模板。

</details>

README 編排參考 [reverse-domain-discovery](https://github.com/ivyliu1201/reverse-domain-discovery)。
