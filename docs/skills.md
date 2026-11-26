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

### 1.1 SKILL.md 的內容架構

一個寫得好的 skill 資料夾通常長這樣：

```text
my-skill/
├── SKILL.md          ← 必要：說明與步驟
├── scripts/          ← 選用：要執行的程式（例如檢查腳本）
├── references/       ← 選用：比較長的參考文件，需要時才讀
└── assets/           ← 選用：範本、範例檔
```

`SKILL.md` 本身分成上下兩段：

```markdown
---
name: gwas-qc-check                  # ① 名稱：小寫英文與連字號，就是 /指令名稱
description: 檢查 PLINK QC 步驟的輸出是否合理。
  在跑完 --maf、--geno、--hwe、--mind 之後使用。  # ② 何時使用：Claude 靠這段決定要不要自動載入
argument-hint: <plink 輸出前綴>        # ③ 選用欄位（見第 4 節表格）
---

# GWAS QC 檢查                       # ④ 標題：一句話說目的

## 什麼時候用                         # ⑤ 使用時機與「不該用」的情況
- 每跑完一個 PLINK 篩選步驟後

## 步驟                               # ⑥ 編號步驟：具體到檔名、指令
1. 讀 $ARGUMENTS.log，抓出前後的樣本數與變異數
2. 執行 scripts/check_counts.py 比對數字

## 規則                               # ⑦ 一定要守的事
- 數字一律從 log 原文抄，附上原文那一行
- 不可修改 data/

## 回報格式                           # ⑧ 輸出長什麼樣子
| 步驟 | 前 | 後 | 移除 | log 原文 |
```

| 區塊 | 寫作重點 |
|---|---|
| ① `name` | 和資料夾同名；短、好記 |
| ② `description` | **最重要**。寫「做什麼」加「什麼時候用」，Claude 只看這段決定是否載入 |
| ④–⑥ 內文 | 用編號步驟，指定檔名與指令，不要寫「適當處理」這種模糊字 |
| ⑦ 規則 | 放不能違反的事，例如「數字要附 log 原文」，這是確保正確性的關鍵 |
| ⑧ 回報格式 | 固定格式，你檢查起來快，也容易發現缺漏 |
| `scripts/`、`references/` | 長內容拆出去，`SKILL.md` 保持在幾百行內；Claude 需要時才讀，省 context |

!!! tip "好 skill 的判斷方法"
    把 `SKILL.md` 給一個沒看過專案的同學看。他照著做能不能得到一樣的結果？可以，就是寫得夠清楚。

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

## 7. 推薦：有助於資料分析正確性的熱門 skill

挑選標準：**來源可追溯**（官方或大量使用者的公開 repo）、**開源授權**、**最近仍有維護**、內容是「要求驗證與證據」的流程。以下資訊於 2026-11-26 從 GitHub 查詢；星數只代表熱門，不代表內容一定正確，安裝前仍要自己讀過。

| skill | 來源 | 對資料分析的幫助 |
|---|---|---|
| `verification-before-completion` | [obra/superpowers](https://github.com/obra/superpowers)（MIT，約 32 萬星，也在官方 marketplace） | 說「完成」之前一定要實際跑過檢查並附上輸出，避免「應該沒問題」 |
| `systematic-debugging` | 同上 | 出錯時先找根本原因再改，不亂試參數 |
| `test-driven-development` | 同上 | 先寫測試再寫程式，例如先寫「189 人、粗 OR 約 2.02」的檢查 |
| `statistical-analysis` | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)（MIT，約 5.8 萬星） | 依資料選檢定、檢查統計假設、報告效果量與信賴區間 |
| `exploratory-data-analysis`、`statsmodels`、`statistical-power` | 同上 | 分析前先看資料分布與缺失值；迴歸模型；樣本數估計 |
| `xlsx`、`pdf` | [anthropics/skills](https://github.com/anthropics/skills)（Anthropic 官方） | 正確讀寫 Excel／CSV、從 PDF 擷取表格，減少讀錯欄位 |

### 7.1 安裝

=== "Superpowers（官方 marketplace）"

    ```text
    /plugin install superpowers@claude-plugins-official
    ```

=== "Anthropic 官方 skills"

    ```text
    /plugin marketplace add anthropics/skills
    /plugin install document-skills@anthropic-agent-skills
    ```

=== "K-Dense 科學分析（只裝需要的）"

    這個 repo 有上百個 skill，建議只裝要用的幾個（需要 GitHub CLI 2.90 以上）：

    ```bash
    gh skill install K-Dense-AI/scientific-agent-skills statistical-analysis --agent claude-code
    gh skill install K-Dense-AI/scientific-agent-skills exploratory-data-analysis --agent claude-code
    ```

裝完在 Claude Code 輸入 `/reload-plugins` 或重新啟動，再輸入 `/` 確認清單裡看得到。

### 7.2 搭配使用的範例

用[操作技巧頁](tips.md#demo)的 `birthwt` 資料：

```text
用 exploratory-data-analysis 先檢查 data/birthwt.csv 的分布與缺失值，
再用 statistical-analysis 分析吸菸與低出生體重的關係（列出檢定的假設是否成立、效果量與 95% 信賴區間）。
最後依 verification-before-completion：重新執行程式，貼出輸出原文，確認粗勝算比約 2.02 才算完成。
```

!!! warning "skill 不能取代你的判斷"
    - 安裝前照[終端機頁第七節](terminal.md#skill)的清單檢查，尤其看 `scripts/` 裡的程式會不會連網或刪檔。
    - 統計 skill 只會依它寫的流程做，研究設計、變數選擇與結果解讀仍要你負責。
    - 裝太多 skill 會互相搶著被載入，只留常用的。
