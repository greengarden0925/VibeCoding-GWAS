---
hide:
  - navigation
  - toc
---

<div class="vg-hero" markdown>
<svg class="vg-helix" viewBox="0 0 120 400" aria-hidden="true">
  <g fill="none" stroke-width="3">
    <path d="M20 0 C100 50 100 50 20 100 C-60 150 100 150 20 200 C-60 250 100 250 20 300 C-60 350 100 350 20 400" stroke="#5eead4"/>
    <path d="M100 0 C20 50 20 50 100 100 C180 150 20 150 100 200 C180 250 20 250 100 300 C180 350 20 350 100 400" stroke="#c4b5fd"/>
  </g>
  <g stroke="#ffffff" stroke-opacity="0.5" stroke-width="2">
    <line x1="35" y1="25" x2="85" y2="25"/><line x1="45" y1="75" x2="75" y2="75"/>
    <line x1="35" y1="125" x2="85" y2="125"/><line x1="45" y1="175" x2="75" y2="175"/>
    <line x1="35" y1="225" x2="85" y2="225"/><line x1="45" y1="275" x2="75" y2="275"/>
    <line x1="35" y1="325" x2="85" y2="325"/><line x1="45" y1="375" x2="75" y2="375"/>
  </g>
</svg>
<span class="vg-kicker">研究所課程 · 14 小時 · 零程式基礎</span>

# Vibe Coding × GWAS

在 VS Code 裡開啟 Claude Code，從安裝工具開始，一步一步完成一次全基因體關聯研究（Genome-Wide Association Study, GWAS），再拆解頂尖期刊常用的後續分析。

[從 L01 開始](chapters/L01.md){ .md-button .md-button--primary }
[VS Code 操作畫面導覽](vscode.md){ .md-button }
[實跑結果](results.md){ .md-button }
</div>

<div class="grid cards" markdown>

-   **第一部分　Vibe coding 基礎**

    ---

    安裝 VS Code 與 Claude Code、學會拆解任務與下指令、用 Git 保存每一步。

    [L01–L04 →](chapters/L01.md)

-   **第二部分　GWAS 觀念與資料**

    ---

    理解 GWAS 的統計邏輯，看懂 PLINK 的基因型資料格式。

    [L05–L06 →](chapters/L05.md)

-   **第三部分　完成一次 GWAS**

    ---

    品質控制、族群結構、關聯分析、Manhattan plot 與 clumping，每一步都有對照答案。

    [L07–L10 →](chapters/L07.md)

-   **第四部分　頂尖期刊的後續分析**

    ---

    統合分析、遺傳力、精細定位、共定位、孟德爾隨機化、多基因風險分數。

    [L11–L14 →](chapters/L11.md)

</div>

<div class="grid cards" markdown>

-   **VS Code 操作畫面導覽**

    ---

    從安裝擴充套件、登入、到送出第一個提示詞，每個按鈕在哪裡。

    [前往 →](vscode.md)

-   **Vibe coding 操作技巧**

    ---

    具體提示詞、Plan 模式、要證據、Esc 與 /rewind。

    [前往 →](tips.md)

-   **建立與安裝 Skill**

    ---

    把「跑完一步就檢查 log」做成 `/gwas-step-check` 一鍵指令。

    [前往 →](skills.md)

</div>

## 這門課要解決的問題

公衛與生醫研究生常遇到同一個困境：研究問題很清楚，但分析需要寫 Linux 指令、Python 或 R，光是學工具就耗掉一個學期。AI 程式助理讓這個門檻大幅降低，可是也帶來新的風險：程式看起來能跑，結果卻是錯的。

這門課的立場是：**讓 AI 寫程式，但由你負責驗證。** 每一章都會同時教「怎麼請 AI 寫」和「怎麼確認 AI 寫對了」。

## 課程結構

| 部分 | 章節 | 時數 | 你會做到的事 |
|---|---|---|---|
| 第一部分　Vibe coding 基礎 | [L01](chapters/L01.md)–[L04](chapters/L04.md) | 4 小時 | 安裝 AI 程式助理、學會拆解任務與下指令、用 Git 保存每一步 |
| 第二部分　GWAS 觀念與資料 | [L05](chapters/L05.md)–[L06](chapters/L06.md) | 2 小時 | 理解 GWAS 的統計邏輯，看懂基因型資料格式 |
| 第三部分　用 vibe coding 完成一次 GWAS | [L07](chapters/L07.md)–[L10](chapters/L10.md) | 4 小時 | 品質控制、族群結構、關聯分析、畫出 Manhattan plot 並解讀 |
| 第四部分　頂尖期刊的後續分析方法 | [L11](chapters/L11.md)–[L14](chapters/L14.md) | 4 小時 | 統合分析、遺傳力、精細定位、共定位、孟德爾隨機化、多基因風險分數，以及期末專題 |

詳細時程見 [14 小時課程時程](syllabus.md)。

## 各章連結

**第一部分　Vibe coding 基礎**

- [L01 什麼是 vibe coding：在研究中使用 AI 寫程式的機會與風險](chapters/L01.md)
- [L02 環境建置：VS Code、Claude Code、Python、Git 與 PLINK](chapters/L02.md)
- [L03 與 AI 協作的工作流程：規劃、下指令、驗證](chapters/L03.md)
- [L04 可重現研究：版本控制、環境紀錄與 AI 程式碼審查](chapters/L04.md)

**第二部分　GWAS 觀念與資料**

- [L05 GWAS 的核心觀念](chapters/L05.md)
- [L06 基因型資料格式與練習資料集](chapters/L06.md)

**第三部分　用 vibe coding 完成一次 GWAS**

- [L07 品質控制（QC）](chapters/L07.md)
- [L08 族群結構與主成分分析](chapters/L08.md)
- [L09 關聯分析：從 logistic regression 到混合模型](chapters/L09.md)
- [L10 結果視覺化與解讀](chapters/L10.md)

**第四部分　頂尖期刊的後續分析方法**

- [L11 統合分析、多族群分析與 LD score regression](chapters/L11.md)
- [L12 從訊號到基因：精細定位、共定位與基因優先排序](chapters/L12.md)
- [L13 因果推論與風險預測：孟德爾隨機化與多基因風險分數](chapters/L13.md)
- [L14 期末專題：拆解一篇頂尖期刊 GWAS 論文並重現部分分析](chapters/L14.md)

## 本課程的資料來源

- **練習資料與指令**：實作章節以東京大學 Laboratory of Complex Trait Genomics 公開的 [GWASTutorial](https://cloufield.github.io/GWASTutorial/) 為基礎，使用其 1000 Genomes Project 東亞族群 504 人的範例資料與模擬表現型。
- **頂尖期刊方法**：從 Europe PMC 檢索 2024–2026 年 Nature Genetics 等期刊的 GWAS 論文，逐篇讀取方法段落，整理成[頂尖期刊方法盤點](methods-survey.md)。
- **影片**：[影片總表](videos.md)收錄 51 支 YouTube 影片，觀看次數與上架日都直接取自影片頁。
- **工具原始文獻**：全部列在[參考文獻](references.md)，每筆附 DOI 與 PubMed 編號。
