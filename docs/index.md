# Vibe Coding × GWAS

給公共衛生與生醫領域研究生的 14 小時課程。學生不需要任何程式基礎，課程用 AI 寫程式（vibe coding）的方式，帶大家從安裝工具開始，完整做完一次全基因體關聯研究（Genome-Wide Association Study, GWAS），再拆解近年頂尖期刊 GWAS 論文常用的後續分析方法。

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
- [L02 環境建置：終端機、Python、Git 與 AI 程式助理](chapters/L02.md)
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
