# 維護指南

## 檔案結構

```text
.
├── mkdocs.yml                 # 網站設定與左側選單（nav）
├── requirements.txt           # 建站套件：zensical
├── README.md
├── .github/workflows/docs.yml # 推送到 main 後自動發布
└── docs/
    ├── index.md               # 首頁
    ├── usage.md               # 使用說明
    ├── syllabus.md            # 14 小時課程時程
    ├── videos.md              # 影片總表
    ├── methods-survey.md      # 頂尖期刊方法盤點
    ├── glossary.md            # 名詞全寫
    ├── references.md          # 參考文獻
    ├── maintenance.md         # 本頁
    └── chapters/L01.md … L14.md
```

## 本機預覽

```bash
pip install -r requirements.txt
zensical serve          # 開啟 http://localhost:8000 預覽，存檔即自動重新整理
zensical build --clean  # 產生正式網站到 site/，應顯示 No issues found
```

## 修改內容

1. 直接編輯 `docs/` 裡的 Markdown 檔，或在網站上按每頁右上角的鉛筆圖示，到 GitHub 編輯。
2. 本機用 `zensical serve` 確認版面。
3. commit 並推送到 `main`，GitHub Actions 會在幾分鐘內更新網站。

## 新增一章要改三處

1. **章檔：** 新增 `docs/chapters/L15.md`，第一行是 `# L15 章名`，小節用 `##`。
2. **選單：** 在 `mkdocs.yml` 的 `nav` 對應部分加一行 `- chapters/L15.md`。選單上的章名會自動取自檔案第一行，不必在 `nav` 重寫。
3. **首頁與時程：** 在 `docs/index.md` 的「各章連結」與 `docs/syllabus.md` 加上連結。

若新章引用影片，請一併更新 `docs/videos.md`，並寫上取得觀看次數的日期。

## 練習題格式

題目與可收合的答案：

```markdown
??? question "題目寫在這裡"

??? success "查看答案"

    答案內容，前面空 4 格。
```

## 撰寫慣例

- 縮寫第一次出現時附英文全寫，並加入 `glossary.md`。
- 清單與表格的前一行必須是空行，否則不會顯示成清單或表格。
- 巢狀清單、收合區塊內的內容一律縮排 4 個空格。
- 指令與參數盡量引用官方文件或公開教學，並在章末附來源。
- 引用頂尖期刊論文的方法時，以 PubMed Central 全文的 Methods 段落為準，不要只看摘要。
- 軟體安裝方式與期刊影響係數會變動，寫上查詢日期，並請讀者以官方最新資訊為準。

## 發布設定

第一次使用需要在 GitHub repo 設定一次：**Settings → Pages → Build and deployment → Source 選 GitHub Actions**。之後每次推送到 `main` 都會自動發布到 `https://greengarden0925.github.io/VibeCoding-GWAS/`。

若 Actions 失敗，到 repo 的 **Actions** 分頁點開失敗的那次，看錯誤訊息；修正後按 **Re-run all jobs**。
