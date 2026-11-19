# 實跑結果

這一頁放本課程**實際執行** GWASTutorial 流程得到的圖與表，讓你在自己動手前先知道「做對了大概長什麼樣子」，做完後也能逐項對照。

## 怎麼產生的

- **流程**：repo 裡的 [`analysis/run_gwas.sh`](https://github.com/greengarden0925/VibeCoding-GWAS/blob/main/analysis/run_gwas.sh)，指令照抄 [GWASTutorial](https://cloufield.github.io/GWASTutorial/) 的 QC、PCA、關聯分析、clumping 頁面，只改了輸入與輸出路徑。
- **畫圖與整理表格**：[`analysis/make_figures.py`](https://github.com/greengarden0925/VibeCoding-GWAS/blob/main/analysis/make_figures.py)。
- **精細定位**：[`analysis/finemap.R`](https://github.com/greengarden0925/VibeCoding-GWAS/blob/main/analysis/finemap.R)，用 susieR 的 `susie_rss()`。
- **執行環境**：GitHub Actions 的 Ubuntu 機器，流程檔是 [`.github/workflows/gwas-analysis.yml`](https://github.com/greengarden0925/VibeCoding-GWAS/blob/main/.github/workflows/gwas-analysis.yml)。

!!! warning "結果尚未產生"
    流程已寫好，正在等待第一次在 GitHub Actions 上執行。執行完成後，這裡會放上 QC、PCA、Manhattan plot、QQ plot、clumping 與 SuSiE 精細定位的實際圖表，並和 GWASTutorial 公布的數字逐項對照。在那之前，本站不放任何非實跑的數字或圖。

<!--RESULTS-->
