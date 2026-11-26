# Vibe coding 操作技巧

這一頁整理在 VS Code 裡用 Claude Code 做研究分析時最常用的技巧。每一條都附上 GWAS 的例子，以及出處。

!!! info "本頁資料來源"
    技巧整理自 Claude Code 官方文件 [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)、[Use Claude Code in VS Code](https://code.claude.com/docs/en/vs-code) 與 [How Claude remembers your project](https://code.claude.com/docs/en/memory)（皆為 2026-11-19 擷取）。「研究情境」欄位是本課程依 GWAS 實作改寫的例子。

<div class="grid cards" markdown>

-   **1. 說清楚它看不到的事**

    ---

    檔名、症狀、「做完」長什麼樣子，一開始就講。

-   **2. 給它一個能自己跑的檢查**

    ---

    讓 Claude 跑完自己對答案，並把指令和輸出貼給你看。

-   **3. 先規劃、再動手**

    ---

    用 Plan 模式或 `/plan`，先看計畫再同意。

-   **4. 盯住第一分鐘**

    ---

    方向不對就按 ++esc++；改兩次還錯就 `/clear` 重來。

</div>

!!! tip "想直接動手"
    [第 9 節](#demo)用一份可下載的公開健康資料（189 位產婦）把這些技巧走一遍。

## 1. 寫具體的提示詞

官方文件的原則是：**點名檔案、描述症狀、說清楚「完成」是什麼樣子**，通常可以省下一輪修正。手上已經有的東西就直接交給它，不要用描述的。

| 不要這樣 | 改成這樣 |
|---|---|
| 「幫我做 QC」 | 「讀 `@data/1KG.EAS...missing.bim` 和 `.fam`，用 PLINK 1.9 算樣本與變異的缺失率，結果放 `results/qc/`，檔名前綴 `plink_results`。執行後告訴我 `.imiss` 和 `.lmiss` 各有幾列、F_MISS 最大值。」 |
| 「圖怪怪的」 | 把 Manhattan plot 截圖直接貼進提示框，再說「X 軸染色體順序跳號，第 10 號排在第 1 號後面，請修正排序」 |
| 「程式壞了」 | 「執行 `@scripts/03_gwas.sh` 出錯，錯誤在 `@terminal:bash`，請先解釋原因，先不要改檔案」 |

把資料交給它的三種方式（VS Code 版）：

- 檔案：輸入 `@` 加路徑。
- 截圖：直接貼進提示框。
- 終端機輸出：輸入 `@terminal:終端機名稱`。

!!! tip "想要完整版本時，說出來"
    官方文件提到，Claude 傾向用最小的方式完成要求，因為它不知道你期待多少。想要它把邊界情況也處理好時，可以直接說 `be ambitious`，或在中文提示裡說清楚要包含哪些部分，例如「除了 Manhattan plot，也要 QQ plot、λGC、以及標出 5 個模擬致病 SNP」。

## 2. 不確定要什麼時，請它先訪問你

還沒想清楚分析設計時，不必自己先寫好規格。請它問你問題：

```text
我想對 1kgeas_binary.txt 的 B1 表現型做 GWAS，但還沒決定共變數和模型。
請一題一題問我，直到你能寫出分析計畫，然後把計畫寫進 PLAN.md。
```

計畫寫好後，官方建議開一個新對話照著 `PLAN.md` 做，讓實作從乾淨的上下文開始。

## 3. 給它一個能自己跑的檢查，並要證據

官方文件說，Claude 會在「看起來做完」時停下。如果你給它一個會回傳「通過或失敗」的檢查，它就能自己做完、自己檢查、自己修。

研究分析最好用的檢查是**對照已知答案**。本課程每章的「驗證清單」都可以直接變成提示詞：

```text
跑完 QC 後，請檢查：
1. sample_data.clean.fam 的列數是否和 GWASTutorial 頁面寫的樣本數一致；
2. .bim 的列數是否和頁面寫的變異數一致。
不一致就找原因，一致就把你執行的指令和輸出原文貼給我。
```

!!! warning "「都通過了」不算證據"
    官方文件建議請 Claude 交出**它執行的指令和輸出**。「全部正確」這句話本身沒有資訊量，讀輸出比你自己重跑還快。

## 4. 先規劃再動手：Plan 模式

點提示框下方的權限模式切到 **Plan**，或輸入：

```text
/plan 用 PLINK 2 做 PCA，要排除高 LD 區域和親屬
```

Claude 會先寫出計畫，VS Code 把計畫開成 Markdown 文件，你可以在上面加註解（例如「KING 門檻用 0.0884」），確認後它才開始改檔案。

## 5. 掌握方向盤：Esc、/rewind、/clear

官方文件的建議是：**看第一分鐘，一偏離就按 Esc；同一件事糾正兩次還錯，就 `/clear` 然後寫一個更好的提示詞**，不要糾正第三次。

| 操作 | 作用 |
|---|---|
| ++esc++ | 立刻停下目前動作，已完成的部分保留 |
| `/rewind`，或在空白提示框連按兩次 ++esc++ | 把程式碼、對話或兩者退回到之前某個提示詞 |
| `/clear` | 清空對話重新開始。換到不相關的任務時也用它 |
| `/compact 保留 QC 的指令與數字` | 指定重點，壓縮長對話 |
| `/btw 問題` | 問一個小問題，不加進對話歷史 |

!!! danger "rewind 救不回 Bash 改的檔案"
    官方文件提醒，檢查點只涵蓋 Claude 用自己的檔案工具編輯的檔案，單純由 Bash 指令改動的檔案不會被還原。所以 PLINK 輸出、`rm` 掉的檔案都救不回來，**原始資料一定要另外備份，並用 Git 保存腳本（L04）**。

## 6. CLAUDE.md 寫短、只寫它找不到的事

`CLAUDE.md` 每次對話都會載入。官方建議只寫 Claude 讀程式碼也找不到的資訊。一個好的判斷方法：

1. 它讀檔案就能知道嗎？
2. 它真的會去讀嗎？

兩題都是「會」，就不用寫。GWAS 專案值得寫進去的通常是：

```markdown
# 專案規則
- data/ 是原始資料，不可修改或刪除。
- 座標版本是 hg19（GRCh37）。
- QC 門檻：--maf 0.01 --geno 0.02 --mind 0.02 --hwe 1e-6。
- 每一步完成後回報樣本數與變異數。
```

官方文件也說明，CLAUDE.md 是背景資訊，不是強制設定。真正不能違反的規則（例如不能刪 `data/`），要靠權限設定或 hook 來擋，並且自己檢查。

## 7. 研究情境的額外守則

以下是本課程針對研究分析加的規則，不是官方文件內容：

- **數字一律回到原始輸出核對。** Claude 摘要的樣本數、P 值，都要在 `.log` 或結果檔裡找到同一個數字。
- **每一步一支腳本。** `01_qc.sh`、`02_pca.sh`……出錯時容易定位，也方便寫進方法段落。
- **先問「為什麼」再問「怎麼改」。** 出錯時先請它解釋原因，你判斷合理再讓它改。
- **不要把個人可識別的健康資料丟進對話。** 本課程用的是 1000 Genomes 公開資料；換成自己的研究資料時，先確認機構的資料使用規範。

## 8. 熟悉後可以加快的設定

| 想做的事 | 怎麼做 |
|---|---|
| 不想每次都按同意 | 切到 **Edit automatically** 或 **Auto** 模式（建議先用 Git 存檔） |
| 同時做兩件事 | 命令選擇區選 **Open in New Tab**，例如一個分頁跑 GWAS、一個分頁查文獻 |
| 重複做同一套步驟 | 做成 skill，見[建立與安裝 Skill](skills.md) |
| 請另一個 AI 審查 | 在終端機版輸入 `/code-review`，它會用沒看過這段對話的子代理審查修改 |

## 9. 實作示範：吸菸與低出生體重 { #demo }

用一份小型公開健康資料，把前面的技巧走一遍。約 30 分鐘。

### 9.1 資料下載

| 項目 | 內容 |
|---|---|
| 下載資料 | [birthwt.csv](https://vincentarelbundock.github.io/Rdatasets/csv/MASS/birthwt.csv)（約 6 KB） |
| 欄位說明 | [birthwt 說明頁](https://vincentarelbundock.github.io/Rdatasets/doc/MASS/birthwt.html) |
| 來源 | R 套件 MASS 的 `birthwt`，經 [Rdatasets](https://vincentarelbundock.github.io/Rdatasets/) 提供 CSV。1986 年美國麻州 Baystate Medical Center 收集；原始出處 Hosmer & Lemeshow (1989) *Applied Logistic Regression* |
| 大小 | 189 位產婦；10 個變數，另有一欄原始列號 `rownames` |

| 變數 | 意義 |
|---|---|
| `low` | 出生體重低於 2.5 公斤（1 = 是） |
| `bwt` | 出生體重（公克） |
| `smoke` | 懷孕期間吸菸（1 = 是） |
| `age` | 母親年齡（歲） |
| `lwt` | 母親最後一次月經時的體重（磅） |
| `race` | 1 = 白人、2 = 黑人、3 = 其他 |
| `ptl`、`ht`、`ui`、`ftv` | 早產次數、高血壓病史、子宮刺激性、第一孕期看診次數 |

建立資料夾、下載、啟動：

=== "Windows（PowerShell）"

    ```powershell
    mkdir birthwt-lab\data; cd birthwt-lab
    curl.exe -L -o datairthwt.csv https://vincentarelbundock.github.io/Rdatasets/csv/MASS/birthwt.csv
    claude
    ```

=== "macOS / Linux"

    ```bash
    mkdir -p birthwt-lab/data && cd birthwt-lab
    curl -L -o data/birthwt.csv https://vincentarelbundock.github.io/Rdatasets/csv/MASS/birthwt.csv
    claude
    ```

也可以點上面的連結用瀏覽器下載，再放進 `data/`。

### 9.2 跟著做

**步驟 1：先認識資料（技巧 1：說清楚它看不到的事）**

```text
讀 @data/birthwt.csv。先不要分析。
回報列數、欄位、每欄缺失值個數、low 和 smoke 的次數分布。
欄位意義：low = 出生體重低於 2.5 公斤，smoke = 懷孕期間吸菸，rownames 是原始列號不要用。
```

**步驟 2：還沒想清楚就讓它訪問你（技巧 2）**

```text
我想研究懷孕期間吸菸和低出生體重的關係。
一題一題問我，直到能寫出分析計畫，寫進 PLAN.md。
```

**步驟 3：先看計畫（技巧 4：Plan 模式）**

```text
/plan 依 PLAN.md 寫 analysis.py：2x2 表、粗勝算比與 95% 信賴區間、
控制 age、lwt、race（類別變數）的 logistic 迴歸。結果寫到 results/。
```

看過計畫沒問題再同意。需要的 Python 套件讓它先告訴你，再決定要不要安裝。

**步驟 4：給它能自己檢查的答案（技巧 3）**

```text
執行 analysis.py 後檢查：
1. 總人數 189
2. 不吸菸：低體重 29、非低體重 86；吸菸：低體重 30、非低體重 44
3. 粗勝算比約 2.02
不一致就找原因；一致就貼出你執行的指令和輸出原文。
```

**步驟 5：看圖、改圖（技巧 1、5）**

```text
畫一張長條圖比較吸菸與不吸菸的低出生體重比例，標出人數與百分比，存成 results/low_by_smoke.png。
```

圖不對就截圖貼回去，具體說哪裡要改。方向錯了按 ++esc++。

**步驟 6：把規則寫下來（技巧 6）**

```text
建立 CLAUDE.md：data/ 不可修改；rownames 欄不分析；race 是類別變數；
每次報告勝算比都要附 95% 信賴區間與樣本數。
```

### 9.3 對答案

| 指標 | 結果 |
|---|---|
| 低出生體重比例 | 不吸菸 29/115（25.2%）；吸菸 30/74（40.5%） |
| 平均出生體重 | 不吸菸約 3056 g；吸菸約 2772 g |
| 粗勝算比（95% CI） | 2.02（1.08–3.78） |
| 調整 age、lwt、race 後（95% CI） | 2.87（1.36–6.05） |

信賴區間用 Wald 法（係數 ± 1.96 × 標準誤）。

### 9.4 討論

- 調整後勝算比從 2.02 變成 2.87。可能是哪個變數造成的？請 Claude 一次只加一個共變數來比較，再分 `race` 各層看 2x2 表。
- 這是觀察性資料，只能說「有關聯」，不能直接說吸菸「造成」低出生體重。Claude 寫的結論有沒有講過頭？
- 勝算比 2.02 可以說成「風險是 2 倍」嗎？低出生體重在這份資料中很常見（59/189），請算風險比來比較。
