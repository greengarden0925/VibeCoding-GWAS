---
description: 檢查剛跑完的 PLINK 步驟是否正常：讀 .log 檔，整理樣本數、變異數、警告與錯誤，並和講義的預期數字對照。Use when the user finished a PLINK or PLINK 2 command and asks whether it worked, or asks to check a .log file.
argument-hint: "[.log 檔路徑] [預期樣本數] [預期變異數]"
---

## 要檢查的檔案

- log 檔：$0
- 預期樣本數：$1
- 預期變異數：$2

## 步驟

1. 用 Read 工具讀取 $0。檔案不存在就停下來，告訴使用者，並列出 results/ 底下有哪些 .log 檔。
2. 從 log 原文找出：
   - 執行的完整指令（log 開頭 `Options in effect` 之後的參數）
   - 讀入與保留下來的樣本數、變異數
   - 每個 QC 條件移除了多少樣本或變異（如果有）
   - 所有含 `Warning` 或 `Error` 的行
3. 如果使用者有給預期樣本數或變異數，逐項比對，寫「一致」或「不一致（差多少）」。
4. 用下面的格式回覆，每個數字後面附上它在 log 裡的原文那一行：

| 項目 | log 中的數字 | 預期 | 結果 |
|---|---|---|---|

5. 最後用一兩句話說明這一步是否可以進入下一步。有不一致或錯誤時，先解釋可能原因，不要修改任何檔案。

## 規則

- 只引用 log 裡真的出現的數字，找不到就寫「log 中沒有」，不要推算。
- 不刪除、不覆寫任何檔案。
