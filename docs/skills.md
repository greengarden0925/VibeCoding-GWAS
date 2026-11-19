# 建立與安裝 Skill

做 GWAS 時，同一套檢查會重複很多次：每跑完一個 PLINK 步驟，就要看 log、核對樣本數和變異數。把這套步驟寫成 **skill**，之後只要輸入 `/skill名稱` 就能叫出來，也能讓 Claude 在適合的時候自己用。

!!! info "本頁資料來源"
    Skill 的格式、存放位置與指令取自 Claude Code 官方文件 [Extend Claude with skills](https://code.claude.com/docs/en/skills)；plugin 的安裝方式取自 [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins) 與 [Use Claude Code in VS Code](https://code.claude.com/docs/en/vs-code)（皆為 2026-11-19 擷取）。本頁的 `gwas-step-check` 是本課程自己寫的範例 skill。

## 1. Skill 是什麼

一個 skill 就是一個資料夾，裡面放一個 `SKILL.md`。`SKILL.md` 有兩部分：

```mermaid
flowchart LR
  A["--- 開頭的 YAML 前置資料<br/>description：什麼時候用"] --> B["Markdown 內文<br/>Claude 要照著做的步驟"]
```

- **資料夾名稱**（或前置資料裡的 `name`）就是你要輸入的指令名稱。
- **`description`** 讓 Claude 判斷什麼時候該自動載入這個 skill，所以要把主要用途寫在最前面。

## 2. 放在哪裡

| 種類 | 位置 | 誰能用 |
|---|---|---|
| 個人 | `~/.claude/skills/<skill名稱>/SKILL.md` | 你在這台電腦上的所有專案 |
| 專案 | `<專案資料夾>/.claude/skills/<skill名稱>/SKILL.md` | 這個專案；提交到 Git 後，合作者也能用 |
| Plugin | 由 plugin 安裝 | 有啟用該 plugin 的地方，指令名稱是 `/plugin名稱:skill名稱` |

本課程建議放在**專案**位置（`~/vibegwas/.claude/skills/`），跟著 Git 一起保存，方便重現。

## 3. 實作：安裝本課程的 `gwas-step-check`

這個 skill 會讀一個 PLINK `.log` 檔，整理樣本數、變異數、警告，並和你給的預期數字對照。

<span class="vg-step">1</span> 在 VS Code 打開 `vibegwas` 資料夾，開啟 Claude Code 面板。

<span class="vg-step">2</span> 在提示框輸入（Manual 模式下它會先問你能不能建立檔案，看過內容再按同意）：

```text
請在這個專案建立 .claude/skills/gwas-step-check/SKILL.md，
內容從下面網址下載後原樣存入，不要修改：
https://raw.githubusercontent.com/greengarden0925/VibeCoding-GWAS/main/course-skills/gwas-step-check/SKILL.md
存好後把檔案內容完整顯示給我看。
```

也可以自己動手：在檔案總管的 `vibegwas` 底下建立 `.claude/skills/gwas-step-check/` 資料夾，新增 `SKILL.md`，把[這個檔案](https://github.com/greengarden0925/VibeCoding-GWAS/blob/main/course-skills/gwas-step-check/SKILL.md)的內容貼進去。

<span class="vg-step">3</span> 檢查有沒有載入：在提示框輸入 `/skills`，清單裡應該看得到 `gwas-step-check`。

!!! note "改了 SKILL.md 不用重開"
    官方文件說明，Claude Code 會監看 `~/.claude/skills/` 和專案的 `.claude/skills/`，新增或修改 skill 會在目前對話裡生效。如果 `.claude/skills/` 這個資料夾是對話開始後才建立的，要執行一次 `/reload-skills`。

<span class="vg-step">4</span> 使用：跑完 L07 的第一步 QC 後，輸入

```text
/gwas-step-check results/qc/plink_results.log
```

如果手上有講義給的預期數字，接在後面當第二、第三個參數（樣本數、變異數）。

### 這個 skill 的內容

````markdown title="SKILL.md"
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
````

重點欄位：

| 寫法 | 意思 |
|---|---|
| `description:` | 用途寫在最前面，讓 Claude 判斷「使用者問某步驟跑得對不對」時自動用它 |
| `argument-hint:` | 在 `/` 選單自動完成時提示要輸入哪些參數 |
| `$0`、`$1`、`$2` | 依序代入你輸入的第 1、2、3 個參數 |

## 4. 自己寫一個 skill

照官方「第一個 skill」範例的三步驟：建資料夾、寫 `SKILL.md`、測試。可以直接請 Claude 幫你寫：

```text
我每次做完 GWAS 都要畫 Manhattan plot 和 QQ plot、算 λGC。
請幫我在 .claude/skills/gwas-plots/SKILL.md 寫一個 skill：
- description 寫清楚什麼時候用
- 參數是 GWAS 結果檔路徑
- 步驟：讀檔、檢查欄位、畫兩張圖存到 figures/、回報 λGC 與顯著 SNP 數
- 規則：不覆寫已存在的圖，改用新檔名
寫好先給我看，不要執行。
```

常用的前置資料欄位：

| 欄位 | 用途 |
|---|---|
| `description` | 什麼時候用（建議一定要寫） |
| `argument-hint` | 自動完成時顯示的參數提示 |
| `disable-model-invocation: true` | 只讓你手動用 `/名稱` 叫出，Claude 不會自己載入。會改動檔案的流程適合這樣設 |
| `allowed-tools` | 叫出這個 skill 的那一輪，哪些工具不用再問你 |
| `paths` | 只在處理符合檔名規則的檔案時才自動載入 |

!!! tip "把即時資訊塞進 skill"
    在 `SKILL.md` 裡寫 `` !`指令` ``，Claude Code 會先執行指令、把輸出放進內容，Claude 讀到的就是最新結果。官方範例用 `` !`git diff HEAD` `` 把目前的修改帶進 skill。

**移除 skill**：刪掉那個 skill 的資料夾即可。

## 5. 內建的 skill

Claude Code 內建幾個 skill，不用安裝就能用，例如：

| 指令 | 用途 |
|---|---|
| `/doctor` | 檢查 Claude Code 的安裝與設定 |
| `/verify` | 實際建置並執行，確認修改真的有效 |
| `/run` | 啟動並操作你的程式，看修改的效果 |

## 6. 安裝別人做好的 plugin

Plugin 是打包好的一組 skill、指令或工具。Anthropic 有官方 marketplace（`claude-plugins-official`）。

=== "VS Code 圖形介面"

    1. 在提示框輸入 `/plugins`，打開 **Manage plugins**。
    2. 在 **Plugins** 分頁搜尋，例如 `commit-commands`，按 **Install**。
    3. 選安裝範圍：**Install for you**（你的所有專案）、**Install for this project**（和專案合作者共用）、**Install locally**（只有你、只在這個 repo）。
    4. 如果 Plugins 分頁是空的，先到 **Marketplaces** 分頁加入 `anthropics/claude-plugins-official`。

=== "在對話裡輸入指令"

    ```text
    /plugin install commit-commands@claude-plugins-official
    ```

    這個指令會先打開 plugin 的詳細資訊，讓你看過並選範圍後才安裝。

=== "在終端機（shell）"

    ```bash
    claude plugin install commit-commands@claude-plugins-official
    ```

    在還沒開過互動式 Claude Code 的新電腦上，要先執行
    `claude plugin marketplace add anthropics/claude-plugins-official`。

!!! warning "安裝前先看內容"
    Skill 與 plugin 會讓 Claude 照著裡面的指示做事，有些還能執行指令。只安裝來源可信的，安裝前打開 `SKILL.md` 讀過一遍。
