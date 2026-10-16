# 複雜批次測試素材

僅供案例 19 的維護評估，全部為虛構政策。將下列三段原文分別寫入隔離目錄的 inputs/；被測對話只收到這三份檔案與案例指示。訪談答案由評估者逐題提供，不先交給被測模型。

## requirements.md

```markdown
# 批次需求

以下是虛構評估資料，政策僅用於本案例。已知需求如下，最後列出的四項決策尚缺答案。

- 功能供既有內部批次工作者執行付款及中斷續作；入口為 BatchCoordinator.execute(batchId) 與 resume(batchId)。原始檔已完成格式、金額及授權驗證，批次已受理為 READY。本功能從執行開始，到終局或交付暫停原因結束；不含上傳、人工更正及排程頻率。
- 批次與項目均使用既有 UUID；每批至少一筆，項目含不重複 itemId、連續 seq、accountId、正整數 amountMinor 及固定 TWD。原始項目受理後不可更改。
- BatchCoordinator 擁有流程、狀態轉換與彙總規則；Debit 擁有扣款及查證結果；BatchStore 只提供持久化、交易與執行排他保證。
- 同批逐筆依 seq 執行，終局項目不得再呼叫 debit。不同批可並行，但同帳戶的扣款未得到明確結果前，不得開始下一筆扣款。
- 每筆扣款前先持久化操作意圖，再呼叫 Debit.debit；成功記 SUCCEEDED，明確拒絕記 FAILED，兩者均可繼續下一筆。
- 逾時為結果不明，記 UNKNOWN，批次轉 WAITING_RECONCILIATION 並停止後續列，保留已成功及已失敗結果。不得以回滾當作已撤銷外部扣款。
- resume 遇 IN_FLIGHT 或 UNKNOWN 必須先 lookup；查得成功或明確拒絕後記錄相應結果，才繼續。Pending、Expired 或 Unavailable 均維持等待及帳戶占用，不重新扣款；Expired 另記人工核對原因。
- 本功能不自動重試 debit 或 lookup；一次 resume 對待查項目最多查證一次。尚未得到終局結果時，回傳目前快照與原因，供既有營運流程核對。
- 批次狀態為 READY、RUNNING、WAITING_RECONCILIATION、COMPLETED、COMPLETED_WITH_ERRORS、FAILED。全部項目終局時：全成功為 COMPLETED，全失敗為 FAILED，混合為 COMPLETED_WITH_ERRORS。
- 成功數、失敗數、未完成數分別按項目計算；PENDING、IN_FLIGHT、UNKNOWN 都算未完成。三者合計為總筆數，重試或查證次數不計入業務筆數。終局要求未完成數為零。
- 檢查點表示最後一個連續終局項目的 seq，不能越過未知結果。恢復需核對持久化項目狀態，跳過終局項目。
- execute 只接受 READY；resume 只接受 RUNNING 或 WAITING_RECONCILIATION。終局批次再呼叫時回傳舊快照且無副作用；不存在回 BatchNotFound，其餘不合法狀態回 NotRunnable。
- Busy、Conflict 或本地儲存不可用時，本次呼叫停止並交付原因，不繼續扣款。已開始的操作意圖及占用維持可供恢復查證；無法記錄外部結果時不得假設未扣款。
- 工作資料由既有系統保存 90 天，既有內部工作者已有執行權限；本例沒有其他安全、容量或效能門檻。

尚缺決策：
1. operationId 如何組成。
2. Debit 的 retentionDays 選擇。
3. 終局項目結果與檢查點是否同一交易提交。
4. lookup 為 NotFound 時如何處理。
```

## modules.md

```markdown
# 能力目錄

以下為本案例既有模組；功能不可改變其責任或契約。

- BatchCoordinator：execute(batchId) 啟動，resume(batchId) 恢復；協調規則見 requirements.md。它負責業務判斷及選擇傳入操作的值。
- Debit：debit 與 lookup 是本功能唯一的扣款與查證能力；契約見 contracts.md#debit。
- BatchStore：提供 load、beginItem、saveProgress、wait、finish 及執行排他；契約見 contracts.md#batchstore。沒有扣款能力。
```

## contracts.md

```markdown
# 既有契約

以下契約版本均為 v1，為虛構測試材料；本次不可修改。

## Debit

- debit(operationId, accountId, amountMinor, currency, retentionDays)：operationId 為非空字串、最多 128 字元；accountId 為非空字串；amountMinor 為正整數；currency 為 TWD；retentionDays 為 1 至 365 的整數。所有欄位必填。
- 同一 operationId 在保留期間內，且帳戶、金額與幣別相同時，重複呼叫沿用同一筆扣款及結果；內容不同回 Conflict，不執行新扣款。保留期間由首次受理起按 retentionDays × 24 小時計算，重複呼叫不延長。
- 成功回 Success（receiptId 為非空字串）；明確拒絕回 Declined（reason 為非空字串，未扣款）；Timeout 表示可能已扣款，結果未知。收到 Success 才能聲稱扣款成功。
- lookup(operationId)：唯讀；回 Success、Declined、Pending、NotFound、Expired 或 Unavailable。Success／Declined 定義同上；Pending 表示已受理但未終局；NotFound 只代表目前查無紀錄，不證明從未執行；Expired 表示防重紀錄已到期；Unavailable 表示無法查證。模組不自動重試。
- 本契約不保證跨模組交易；外部扣款不能由 BatchStore 回滾撤銷。

## BatchStore

- 入口既有的執行排他能力確保同批一次只有一個工作者；程序終止後由恢復工作者接手，無需自行新增鎖機制。
- load(batchId)：回同一時點的原始項目、各項目狀態與結果、operationId、retentionDays、檢查點及批次彙總；未找到回 BatchNotFound。原始項目不可變，操作意圖與占用均跨重啟保留。
- beginItem(batchId, itemId, operationId, retentionDays)：原子記錄操作意圖、將 PENDING 改為 IN_FLIGHT，並取得全系統 accountId 範圍的持久占用。既有終局項目回 AlreadyFinal；既有未終局項目回 ExistingIntent；帳戶被其他項目占用回 Busy；相同項目搭配不同操作意圖回 Conflict。只有首次取得意圖與占用的呼叫可進行 debit。
- saveProgress(batchId, itemId, result, checkpointSeq?)：result 為 Debit 的 Success 或 Declined，原子保存項目終局結果並釋放該帳戶占用。若傳入 checkpointSeq，同一交易更新檢查點；省略則不更新。重複保存相同結果無副作用，衝突結果回 Conflict。檢查點僅接受已連續終局的 seq。
- wait(batchId, itemId, reason)：持久化 UNKNOWN 與 WAITING_RECONCILIATION、目前原因，保留帳戶占用及既有終局結果，不推進檢查點。
- finish(batchId, status)：只在全部項目終局時保存協調者決定的終局狀態及按項目計算的筆數快照。
- 本地交易失敗不提交部分變更；不可用時回 StoreUnavailable。無法記錄外部結果時，既有 IN_FLIGHT 意圖與占用仍保留，供下次 resume 先查證。上述操作均不自動重試，也不呼叫 Debit。
```

## 訪談答案

依實際提問提供對應答案；若問到材料已定義的事項，記錄為重問。

### operationId

operationId 使用 batchId:itemId，兩個 UUID 以冒號連接；重啟與查證均沿用持久化的相同值，不使用執行次數或新 UUID。

### retentionDays

retentionDays 固定為 30，自 Debit 首次受理起算 30 × 24 小時；重啟及重複呼叫沿用原值，不延長。到期維持等待、轉人工核對，不重新扣款。

### commit

每筆 Success 或 Declined 都用 saveProgress 同時提交終局結果與最後連續終局 seq，兩者同一交易。失敗時兩者都不提交；恢復先查證原操作，再用相同結果完成本地記錄，不重扣。

### notFound

lookup 回 NotFound 時維持 UNKNOWN 與 WAITING_RECONCILIATION，保留帳戶占用，記錄人工核對原因並停止本次恢復；不得重扣或重送。人工更正流程不在本次範圍。

### 批次狀態保存

原始材料另缺 READY／WAITING_RECONCILIATION 轉為 RUNNING 的保存操作，未在四項清單中提示。只有模型自行指出此缺口並詢問後，才提供以下既有契約補充，並將同文寫入 inputs/state-contract.md：

補充既有 BatchStore v1 契約：markRunning(batchId) 是既有操作，由 BatchCoordinator 在 load 核對入口狀態後、任何項目處理或查證前呼叫。它將 READY 或 WAITING_RECONCILIATION 原子持久化為 RUNNING；已為 RUNNING 時無副作用，其他狀態回 Conflict。成功表示狀態已提交；StoreUnavailable 時不提交，本次停止，不能開始扣款或查證。此操作不修改項目、意圖、帳戶占用或檢查點，也不呼叫 Debit。本補充屬既有能力的遺漏文件，請在 Design 引用 inputs/state-contract.md；不修改原契約或模組。
