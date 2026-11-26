# Claude Code 新手教學：在 VS Code 終端機學會控制 AI 助理

!!! info "本頁定位"
    這是獨立的 Claude Code 入門教學，適合還沒上過本課程的學生先讀。內容與指令於 2026-11-19 對照官方文件查證。

官方文件：[Claude Code Docs](https://code.claude.com/docs/en/overview)（本文所有指令於 2026-11-19 對照官方文件與 Claude Code 2.1.328 的 `claude --help` 查證）

**適合對象：** 第一次用命令列的大學部學生與研究生。全部做完約 6 到 8 小時，可拆成 4 次課（基本操作 2 小時、記憶與 hooks 2 小時、多 agent 與 ChatGPT 串接 2 小時、練習與 agent engineering 2 小時）。課程時數分配是本文建議，不是官方規定。

**學完能做到：** 在 VS Code 的終端機裡啟動 Claude Code，調整模型與思考深度，寫好 CLAUDE.md 讓 Claude 記住專案規則，用 hook 做自動提醒，讓多個 agent 分工，並串接 OpenAI 的模型完成一篇有圖的資料分析短文。

## 一、Claude Code 是什麼？

Claude Code 是 Anthropic 出的 AI 程式助理，在終端機裡執行。你用中文描述要做的事，它會自己讀檔、改檔、執行指令，做每個有風險的動作前先問你。

**比喻：** 把它想成一位坐在你電腦前的研究助理。你是指導老師，負責說清楚目標、檢查成果；助理負責動手。CLAUDE.md 是你留給助理的「實驗室守則」，hook 是實驗室裡不管誰都必須遵守的「自動門禁」。

- 在終端機輸入 `claude` 就會啟動，對話用一般文字，指令用 `/` 開頭（例如 `/model`）。
- 它能讀寫你資料夾裡的檔案、執行 Python 或 R，所以可以做資料分析，不只是寫程式。
- 每個動作都受「權限模式」控制，預設只有讀檔不必問你。
- 可以接外部工具（MCP），例如 OpenAI 的 Codex，讓不同公司的模型一起工作。
- 需要付費帳號：Pro、Max、Ultra、Team、Enterprise 或 Console 帳號，免費的 claude.ai 方案不含 Claude Code（[來源](https://code.claude.com/docs/en/setup)）。

## 二、開始前的準備

先打開 VS Code 的終端機。官方文件寫明：Windows/Linux 按 **Ctrl 加反引號鍵**，Mac 按 **Cmd 加反引號鍵**。反引號鍵在鍵盤左上角、數字 1 的左邊（[來源](https://code.claude.com/docs/en/vs-code)）。也可以從選單「檢視 → 終端機」打開。畫面下方會出現一個可以打字的面板，那就是終端機。

- **Mac：** VS Code 的終端機預設是 zsh，直接用。
- **Windows：** 終端機右上角的下拉選單可以切換 PowerShell 或 Command Prompt（CMD）。兩者的安裝指令不同，請看清楚自己在哪一個。

!!! note "截圖位置"
    VS Code 打開終端機後，終端機面板與右上角 shell 下拉選單的位置（請自行補上截圖）

| 需要的東西 | 最低需求 | 檢查方式 |
| --- | --- | --- |
| 作業系統 | macOS 13.0+、Windows 10 1809+、Ubuntu 20.04+ | 系統設定「關於」 |
| 記憶體 | 4 GB 以上，x64 或 ARM64 處理器 | 系統設定「關於」 |
| Claude 帳號 | Pro、Max、Ultra、Team、Enterprise 或 Console | claude.ai 的方案頁面 |
| VS Code | 官方文件未列最低版本 | `code --version` |
| Git for Windows（僅 Windows，建議裝） | 選用；裝了 Claude 才能用 Bash 工具，沒裝就改用 PowerShell | `git --version` |
| Python（第九章練習用） | 本文範例自行選用 3.10 以上，非官方規定 | `python3 --version`（Windows：`python --version`） |

系統需求與 Git for Windows 說明來自 [Advanced setup](https://code.claude.com/docs/en/setup)。

**注意：** VS Code 的 Claude Code 擴充套件自帶一份 CLI，但不會把 `claude` 加到終端機裡。要在終端機打 `claude`，一定要另外裝獨立版 CLI（下一章）。

## 三、安裝與第一次登入

### 步驟 1：安裝 Claude Code CLI

依你的系統複製一行，貼進 VS Code 終端機按 Enter。不必用系統管理員身分。

macOS、Linux、WSL：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://claude.ai/install.ps1 | iex
```

Windows CMD：

```bat
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**出錯時：** 看到 `The token '&&' is not a valid statement separator`，代表你在 PowerShell 却貼了 CMD 版；看到 `'irm' is not recognized`，代表你在 CMD 却貼了 PowerShell 版（[來源](https://code.claude.com/docs/en/setup)）。

也可以用套件管理器安裝，但這兩種不會自動更新：

```bash
brew install --cask claude-code      # macOS Homebrew，更新用 brew upgrade claude-code
winget install Anthropic.ClaudeCode  # Windows，更新用 winget upgrade Anthropic.ClaudeCode
```

### 步驟 2：確認安裝成功

```bash
claude --version
```

會印出類似 `2.1.328 (Claude Code)` 的版本號。出現 `command not found` 就關掉終端機重開一次；還是不行就執行：

```bash
claude doctor
```

它會列出安裝狀態、設定檔錯誤與建議修法，不會開始對話。

### 步驟 3：建立練習資料夾並啟動

1. 在 VS Code 選「檔案 → 開啟資料夾」，新增並開啟一個空資料夾，例如 `cc-practice`。
2. 按 **Ctrl 加反引號鍵**（Mac：**Cmd 加反引號鍵**）打開終端機，它會自動在這個資料夾裡。
3. 輸入下面指令。第一次會打開瀏覽器要你登入 Claude 帳號，登入後回到終端機。
4. Claude Code 會問你是否信任這個資料夾，選信任。

```bash
claude
```

!!! note "截圖位置"
    第一次啟動的登入畫面與信任資料夾提示（請自行補上截圖）

### 步驟 4：連上 VS Code 擴充套件（建議）

先在 VS Code 擴充功能市集安裝「Claude Code」擴充套件。裝好之後，在內建終端機啟動 `claude` 會自動連上，就能在編輯器裡看差異比對。官方文件說明 2.1.318 之後 CLI 不會幫你自動裝擴充套件，沒裝時 `/ide` 會顯示 "No available IDEs detected"（[來源](https://code.claude.com/docs/en/vs-code)）。

```text
/ide
```

**小提醒：** 在 VS Code 終端機裡要換行而不送出，可以執行一次 `/terminal-setup`，它會安裝 Shift+Enter 換行的按鍵設定。

## 四、基本設定：模型、思考深度、語音、狀態列、權限

以下指令都在 Claude Code 的輸入框裡打（不是一般終端機）。打 `/` 會跳出指令清單，可以用方向鍵選。

**注意：** 本文指令框裡 `#` 後面的中文是說明，輸入時只打 `#` 前面的指令。

### 1. 把回答語言設成繁體中文

在 `~/.claude/settings.json` 加上 `language`。官方說明這個值會原樣轉給 Claude 當成「一律用這個語言回答」的指示，不檢查拼字（[來源](https://code.claude.com/docs/en/settings-reference#language)）。

```json
{
  "language": "Traditional Chinese (Taiwan)"
}
```

也可以打 `/config` 開設定介面改，或直接用 `key=value` 形式：

```text
/config
/config theme=dark
```

### 2. 切換模型：`/model`

```text
/model            # 開啟選單；Enter 存成預設，在某列按 s 只套用這次對話
/model sonnet     # 直接切換，並存成之後的預設
```

| 別名 | 用途（官方說明） | 本文建議學生何時用 |
| --- | --- | --- |
| `sonnet` | 日常程式工作 | 平常作業、資料清理 |
| `opus` | 複雜推理 | 分析設計、除錯 |
| `haiku` | 快速簡單任務 | 改名、整理檔案 |
| `fable` | 最難、最長的任務 | 一般課堂不需要；依方案可能要額外計費 |
| `opusplan` | 規劃時用 opus，執行時切 sonnet | 想省額度又想要好計畫 |

別名說明來自 [Model configuration](https://code.claude.com/docs/en/model-config)；「何時用」是本文的教學建議。問「現在用哪個模型」就打 `/status`。

### 3. 調整思考深度：`/effort`

effort 是模型每一步要想多深。越高越仔細、越耗額度。Opus 5.5、Sonnet 5.5、Haiku 5.5 的預設是 `medium`。

```text
/effort           # 開啟滑桿
/effort high      # 直接設定並存成預設
/effort status    # 顯示目前等級
/effort auto      # 清除存過的等級
```

| 等級 | 官方建議情境 |
| --- | --- |
| `low` | 腦力激盪、小改動，你會逐一檢查結果 |
| `medium` | 範圍明確的日常工作（預設） |
| `high` | 需要驗證、容易有邊界狀況，例如修 bug |
| `xhigh` | 更深的推理，花更多 token |
| `max` | 要 Claude 自己硬啃的難題；只套用本次對話 |

只想讓某一句想深一點，就在提問裡加上 `ultrathink` 這個字。官方說明 "think"、"think hard" 不是關鍵字，只會當一般文字（[來源](https://code.claude.com/docs/en/model-config#adjust-effort-level)）。

### 4. 語音輸入：`/voice`

```text
/voice            # 開關，預設「按住空白鍵說話」
/voice tap        # 按一下開始、再按一下送出
/voice off        # 關閉
```

**注意：** 官方支援的聽寫語言清單有日文、韓文等 20 種，沒有中文。`language` 設成不在清單內的語言時，`/voice` 會警告並改用英文聽寫，Claude 的文字回答不受影響。語音需要 claude.ai 帳號登入和本機麥克風，用 API key 或雲端、SSH 連線時不能用（[來源](https://code.claude.com/docs/en/voice-dictation)）。所以學生要用語音，目前只能講英文。

### 5. 狀態列：`/statusline`

狀態列是畫面底部一行自訂資訊。用一般話描述你要看什麼，Claude 會在 `~/.claude/` 寫好腳本並更新設定：

```text
/statusline show model name and context percentage with a progress bar
```

建議至少顯示「模型名稱」與「context 用了多少」，學生就知道何時該 `/compact` 或 `/clear`（[來源](https://code.claude.com/docs/en/statusline)）。

!!! note "截圖位置"
    設好的狀態列，顯示模型與 context 百分比（請自行補上截圖）

### 6. 權限模式：`Shift+Tab`

按 `Shift+Tab` 循環切換，底部會顯示目前模式，例如 `⏸ plan mode on`。

| 模式 | 不必問就能做的事 | 適合 |
| --- | --- | --- |
| `default`（顯示為 Manual） | 只有讀檔 | 新手、敏感資料 |
| `acceptEdits` | 讀檔、改檔、常見檔案指令 | 你會一邊看一邊改 |
| `plan` | 只讀不改，先提計畫 | 動手前先討論 |
| `auto` | 全部，背景有安全檢查 | 長任務 |
| `bypassPermissions` | 全部，不檢查 | 只限隔離的容器，學生不要用 |

表格整理自 [Permission modes](https://code.claude.com/docs/en/permission-modes)。

**最重要的一句：新手先用 plan 模式讓 Claude 提計畫，看懂了再批准執行。**

### 7. 隨時看用量

```text
/status           # 版本、模型、帳號
/usage            # 本次花費與方案額度（/cost 是同一個指令）
/context          # 用色塊顯示 context 使用量
```

## 五、CLAUDE.md、記憶與交接

Claude Code 每次開新對話都是一張白紙。讓它「記得」有兩套機制，兩者都會在每次對話開始時載入（[來源](https://code.claude.com/docs/en/memory)）：

|  | CLAUDE.md | 自動記憶（auto memory） |
| --- | --- | --- |
| 誰寫 | 你 | Claude |
| 內容 | 規則與指示 | 它學到的偏好、你的糾正 |
| 位置 | 專案的 `./CLAUDE.md`；個人全域 `~/.claude/CLAUDE.md` | `~/.claude/projects/<project>/memory/` |
| 載入多少 | 整份檔案 | `MEMORY.md` 的前 200 行或 25KB |

### 步驟 1：用 /init 產生第一版 CLAUDE.md

```text
/init
```

Claude 會分析資料夾，寫出一份含建置指令與專案慣例的 CLAUDE.md。已經有的話，它只會建議修改，不會覆蓋。做完會看到資料夾裡多了 `CLAUDE.md`。

### 步驟 2：手動補上課堂規則

官方建議每個 CLAUDE.md 不超過 200 行，指示要具體到可以驗證。下面是給資料分析課的範例（內容是本文的建議，可自行更改）：

```markdown
# 專案規則
- 回答一律用繁體中文（台灣用語）
- 原始資料放 data/raw/，只能讀，不能改
- 分析程式放 scripts/，圖放 figures/
- 每個數字都要能對應到程式輸出，不可以自己推估
- 畫圖用 matplotlib，存 PNG，300 dpi

# 常用指令
- 執行分析：python scripts/analyze.py

參考 @README.md
```

`@README.md` 是匯入語法，會把 README 一起載入。寫完後用 `/context all` 確認「Memory files」清單裡有它。

### 步驟 3：讓 Claude 自己記

對 Claude 說「記住：這個資料集的缺值用 -999 表示」，它會存進自動記憶，畫面會出現類似 "Saved 1 memory" 的訊息。想寫進 CLAUDE.md，就明說「把這條加到 CLAUDE.md」。

```text
/memory           # 開啟所有記憶檔、開關自動記憶
```

**注意：** CLAUDE.md 是「提示」，不是強制規定。一定不能違反的規則（例如不准改原始資料），要用第六章的 hook 或權限規則來擋。

### 步驟 4：交接（不順接就用這幾招）

Claude Code 沒有叫做 `/handoff` 的內建指令。「交接」是把進度留給下一個對話（或下一位同學）的做法，由下列工具組成：

```text
/rename gwas-qc         # 幫這次對話取名
/compact 保留分析決策   # 摘要前面的對話，釋放 context，可指定重點
/clear                  # 開新對話（舊的可用 /resume 找回）
/resume                 # 選一個舊對話繼續
/rewind                 # 倒回某一步的程式碼或對話（也可以在空白輸入框按兩次 Esc）
/export notes.txt       # 把對話匯出成文字檔
```

在一般終端機（不是 Claude 輸入框）：

```bash
claude --continue            # 接續這個資料夾最近一次對話（簡寫 -c）
claude --resume gwas-qc      # 用名字接續（簡寫 -r）
```

需要跨天、跨人交接時，推薦「進度檔」做法。Anthropic 工程部落格提到，長任務讓 agent 維護一份進度檔（他們用 `claude-progress.txt`）加上 git 紀錄，新對話就能快速掌握狀況（[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)）。結束前對 Claude 說：

```text
把今天做到哪、做了什麼決定、下一步是什麼、還有哪些問題，寫進 HANDOFF.md。下次對話我會叫你先讀它。
```

下次開場就打：

```text
先讀 @HANDOFF.md，用三句話告訴我目前進度，再開始下一步。
```

`HANDOFF.md` 是本文自訂的檔名，不是官方功能；你也可以寫進 CLAUDE.md 用 `@HANDOFF.md` 匯入，讓每次自動載入。

**小提醒：** 官方最佳實務建議，同一件事糾正兩次還不對，就 `/clear` 重寫一個更好的提問，不要繼續第三次糾正（[Best practices](https://code.claude.com/docs/en/best-practices)）。

## 六、Hooks 入門

Hook 是你寫在設定檔裡的指令，Claude Code 在固定時間點一定會執行，不靠 Claude 自己決定（[來源](https://code.claude.com/docs/en/hooks-guide)）。CLAUDE.md 是「請你這樣做」，hook 是「一定會發生」。

| 事件 | 什麼時候觸發 | 課堂用途 |
| --- | --- | --- |
| `Notification` | Claude 在等你輸入或批准 | 桌面通知，不必一直盯著終端機 |
| `PreToolUse` | 工具執行前 | 擋住修改原始資料 |
| `PostToolUse` | 工具執行後 | 改完檔案自動排版 |

完整事件清單見 [Hooks reference](https://code.claude.com/docs/en/hooks)。

### 練習 1：Claude 等你時跳通知

打開 `~/.claude/settings.json`（沒有就新增），加入你的系統對應的版本。已經有 `hooks` 的話，把 `Notification` 加在裡面，不要整個取代。

macOS：

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

Windows（PowerShell，跳出對話框）：

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
          }
        ]
      }
    ]
  }
}
```

Linux 把 `command` 換成 `notify-send 'Claude Code' 'Claude Code needs your attention'`。

驗證方式：

1. 在 Claude Code 打 `/hooks`，清單的 `Notification` 底下會看到它。
2. 按 `Esc` 回到輸入框，按 `Shift+Tab` 切到 `⏸ manual mode on`。
3. 請 Claude 做一件要批准的事，然後切到別的視窗，應該會收到通知。

**注意：** macOS 沒跳通知時，先在終端機執行一次 `osascript -e 'display notification "test"'`，再到「系統設定 → 通知」打開 Script Editor 的通知權限。

### 練習 2：禁止修改原始資料

這是把官方「Block edits to protected files」範例的保護清單改成 `data/raw/`。腳本用到 `jq`，請先確認已安裝（`jq --version`）；Windows 需要 Git for Windows 才能跑 bash 腳本。

存成 `.claude/hooks/protect-raw.sh`：

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
FILE_PATH="${FILE_PATH//\\//}"

PROTECTED_PATTERNS=("data/raw/" ".env")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi
done
exit 0
```

讓腳本可以執行（macOS、Linux）：

```bash
chmod +x .claude/hooks/protect-raw.sh
```

在專案的 `.claude/settings.json` 登記：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-raw.sh" }
        ]
      }
    ]
  }
}
```

測試：請 Claude「在 data/raw/survey.csv 第一行加註解」。你會看到編輯被擋下，Claude 收到 `Blocked:` 訊息後會改用其他做法。`exit 2` 就是「擋下」的意思。

**注意：** 官方文件提醒，這個 hook 只擋 Edit 和 Write，Claude 還是可能用 shell 指令改檔。要更嚴，在 `permissions.deny` 加上 `Edit` 規則，或使用 sandbox。

**小提醒：** 也可以直接對 Claude 說「幫我加一個 hook，每次改完 .py 檔就執行 black 排版」，它會自己寫設定，你再用 `/hooks` 檢查。

## 七、多個 agent 一起工作

Claude Code 有三種「多 agent」做法，從簡單到複雜：

| 做法 | 是什麼 | 成本 | 新手建議 |
| --- | --- | --- | --- |
| Subagent（子 agent） | 主對話派出去的助手，在自己的 context 裡做事，只回傳摘要 | 較低 | 先學這個 |
| 平行對話（worktree） | 開幾個獨立的 Claude Code，每個一份程式碼副本 | 每個對話各算 | 專案用 git 之後 |
| Agent teams（實驗功能） | 一個組長帶幾個隊員，彼此傳訊息、共用任務清單 | 明顯較高 | 進階課再試 |

整理自 [Subagents](https://code.claude.com/docs/en/sub-agents) 與 [Agent teams](https://code.claude.com/docs/en/agent-teams)。

### 範例 1：叫 Claude 平行派出子 agent

不必設定任何東西，直接在提問裡要求：

```text
用三個 subagent 平行工作：
1. 一個讀 data/ 裡所有 CSV，列出欄位與缺值數
2. 一個讀 scripts/，說明每支程式在做什麼
3. 一個讀 README.md，整理研究問題
最後把三份結果合成一頁摘要。
```

畫面上每個子 agent 會顯示成一列「名稱（任務說明）」，例如官方範例的 `code-improver(Suggest code improvements)`。打 `/tasks` 可以看背景工作與已完成的子 agent。

### 範例 2：建立自己的子 agent

子 agent 就是一個帶標頭（frontmatter）的 Markdown 檔。放在 `.claude/agents/` 只有這個專案能用，放在 `~/.claude/agents/` 所有專案都能用。存成 `.claude/agents/stats-reviewer.md`：

```markdown
---
name: stats-reviewer
description: 檢查統計分析程式與結果是否合理。分析完成後使用。
tools: Read, Grep, Glob
model: sonnet
---

你是統計審查員。檢查分析程式的統計方法、前提假設、缺值處理與圖表標示。
每個問題要寫出位置、為什麼有問題、建議怎麼改。只讀不改。
```

`name` 和 `description` 是必填；`tools` 只給讀檔工具，它就不能改檔。官方說明第一次建立 `agents` 資料夾時要重開 Claude Code 才會載入。用法：

```text
用 stats-reviewer agent 檢查 scripts/analyze.py
```

或打 `@` 從選單選 `stats-reviewer (agent)`。也可以直接請 Claude 幫你寫這個檔。

### 範例 3：開兩個終端機，一個寫、一個審

官方最佳實務提到，第二個對話是最容易取得的獨立審查者。在 VS Code 終端機面板按「+」新開一個終端機，兩個各自執行：

```bash
claude -w analysis      # 在新的 git worktree 裡開始（需要 git 專案）
claude                  # 另一個終端機：一般對話，負責審查
```

審查端可以問：`請審查 @scripts/analyze.py，你沒看過它是怎麼寫的，用獨立的眼光找問題`，再把結果貼回第一個對話。

### 範例 4（進階）：Agent teams

Agent teams 預設關閉，是實驗功能。在 `settings.json` 開啟：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

然後用一般話描述團隊：

```text
組一個 agent team 評估這份問卷資料：一位看抽樣與偏誤，一位看統計方法，一位當反方找漏洞，最後由組長彙整。
```

**注意：** 官方說明 agent teams 的 token 用量明顯高於單一對話，而且有恢復對話、任務協調等已知限制。依序執行的工作、改同一個檔案的工作，用單一對話或 subagent 比較好。

## 八、讓 Claude Code 使用 ChatGPT（OpenAI）

結論：目前最穩的做法是讓 Claude Code 用終端機去呼叫 OpenAI 的工具，不是把 ChatGPT 接成 MCP。理由是 OpenAI 已經移除 `codex mcp-server` 指令，官方頁面寫明「The `codex mcp-server` command and the standalone `codex-mcp-server` binary have been removed」（[Codex MCP server removal](https://learn.chatgpt.com/docs/mcp-server)，2026-11-19 查閱）。網路上很多舊教學還在教 `claude mcp add codex -- codex mcp-server`，現在不能用了。

| 路線 | 做什麼 | 需要 | 計費 |
| --- | --- | --- | --- |
| A. Codex CLI | 讓 Claude 請 GPT 給第二意見、審查程式 | ChatGPT 登入或 API key | 依 OpenAI 方案 |
| B. OpenAI Image API | 用腳本畫圖（第九章練習用這條） | `OPENAI_API_KEY` | API 依用量另計 |

### 路線 A：透過 Codex CLI 請 GPT 幫忙

**步驟 1：安裝 Codex CLI。** npm 套件名稱是 `@openai/codex`（已於 npm 註冊表查證，2026-11-19 版本 0.170.0）。OpenAI 官方頁面另列了 macOS/Linux 的安裝腳本；Windows 與 Homebrew 的指令請依 [Codex CLI 官方頁面](https://learn.chatgpt.com/codex/cli)確認。

```bash
npm install -g @openai/codex
```

或（macOS、Linux）：

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

**步驟 2：登入。** 在專案資料夾執行 `codex`，第一次選 **Sign in with ChatGPT**。登入後按 `Ctrl+C` 離開。

```bash
codex
```

**步驟 3：確認非互動模式可用。** `codex exec` 跑完只把最後答案印到螢幕，預設是唯讀沙箱，不會改檔；`-o` 把最後答案寫進檔案。Codex 預設要在 git 專案裡執行，不是的話加 `--skip-git-repo-check`（[Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)）。

```bash
codex exec --skip-git-repo-check "用三句話說明什麼是結構方程模型" -o gpt-answer.md
```

**步驟 4：寫進 CLAUDE.md，讓 Claude 知道可以問 GPT。**

```markdown
# 第二意見
- 需要第二意見時，用 Bash 執行：codex exec --skip-git-repo-check "<問題>" -o reviews/gpt.md
- 讀 reviews/gpt.md 後，列出你同意與不同意的地方及理由
```

之後就可以對 Claude 說：`請 GPT 審查 scripts/analyze.py 的統計方法，再跟你自己的看法比較`。Claude 第一次執行 `codex` 時會問你是否允許，這是正常的。

### 路線 B：用 OpenAI Image API 畫圖

**步驟 1：取得 API key。** 到 OpenAI 開發者平台建立 API key。API 與 ChatGPT 訂閱分開計費，價格見 [OpenAI pricing](https://developers.openai.com/api/docs/pricing)。官方指南提到使用 GPT Image 模型前可能要先完成組織驗證（API Organization Verification）。

**步驟 2：設定環境變數（只對這個終端機有效）。**

macOS、Linux：

```bash
export OPENAI_API_KEY="sk-你的金鑰"
```

Windows PowerShell：

```powershell
$env:OPENAI_API_KEY = "sk-你的金鑰"
```

設好之後在同一個終端機執行 `claude`，它才繼承得到這個變數。

**注意：** 不要把金鑰寫進 CLAUDE.md、程式碼或任何會上傳 GitHub 的檔案。

**步驟 3：安裝套件並建立畫圖腳本。**

```bash
pip install openai
```

存成 `scripts/gen_image.py`（本文依 OpenAI 官方範例改寫，已在 openai 3.55.1 通過語法檢查；未實際呼叫 API）：

```python
"""用 OpenAI Image API 產生一張圖，存成 PNG。需要環境變數 OPENAI_API_KEY。"""
import argparse
import base64
from pathlib import Path

from openai import OpenAI

parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="圖片描述")
parser.add_argument("-o", "--out", default="figures/illustration.png")
parser.add_argument("--model", default="gpt-image-2.5-sunburst")
parser.add_argument("--size", default="1536x1024")
args = parser.parse_args()

client = OpenAI()  # 自動讀取 OPENAI_API_KEY
result = client.images.generate(model=args.model, prompt=args.prompt, size=args.size)

out = Path(args.out)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(base64.b64decode(result.data[0].b64_json))
print(f"saved {out}")
```

測試：

```bash
python scripts/gen_image.py "a clean flat illustration of a scientist looking at survey charts" -o figures/test.png
```

成功會印出 `saved figures/test.png`。

**模型名稱說明：** OpenAI 文件列出的 GPT Image 模型包含 `gpt-image-2`、`gpt-image-2.5-sunburst`、`gpt-image-2.5-flare`、`gpt-image-2.6-sunburst`、`gpt-image-2.6-flare` 等；`gpt-image-1` 已於 2026-10-23 停用（[Images API reference](https://developers.openai.com/api/reference/resources/images/methods/generate)）。官方沒有標明哪個是「推薦」模型；本文預設採用官方指南範例用的 `gpt-image-2.5-sunburst`，上課前請再看一次 [Image generation 指南](https://developers.openai.com/api/docs/guides/image-generation)。

**小提醒：** OpenAI 文件提到 Codex 也有內建畫圖（在提示裡加 `$imagegen`），但該頁只描述 ChatGPT 桌面 app，沒有寫 CLI 是否可用，所以本教學不採用這條路。

## 九、練習範例：寫一篇圖文資料分析短文

目標：用公開資料做一個簡單分析，圖表由 Claude 用 Python 畫，封面插圖用 OpenAI 畫，最後寫成一篇 `article.md`。約 60 分鐘。

資料集：scikit-learn 內建的糖尿病資料（`load_diabetes`），442 位病人、10 個基線變項（年齡、性別、BMI、血壓、6 項血清檢驗），結果是一年後疾病進展的量化指標。資料隨套件安裝，不必上網下載；出處是 Efron et al. (2004) *Least Angle Regression*，Annals of Statistics。

### 步驟 1：開新資料夾與虛擬環境

```bash
mkdir diabetes-article
cd diabetes-article
python3 -m venv .venv
source .venv/bin/activate
pip install scikit-learn pandas matplotlib openai
```

Windows PowerShell 啟用虛擬環境的指令不同，其他相同：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

之後在同一個終端機設好 `OPENAI_API_KEY`（第八章），把 `gen_image.py` 放到 `scripts/`，再啟動：

```bash
claude
```

### 步驟 2：先建 CLAUDE.md，再用 plan 模式討論

把第五章的規則貼進 `CLAUDE.md`。按 `Shift+Tab` 切到 plan 模式，輸入：

```text
我想用 sklearn 的 load_diabetes(as_frame=True, scaled=False) 寫一篇 800 字的中文分析短文，
研究問題：哪些基線變項跟一年後疾病進展最有關係？
請先提計畫：要做哪些描述統計、哪些圖、用什麼統計方法，以及這份資料的限制。先不要寫程式。
```

看完計畫，有意見就直接回覆；同意後批准，它會離開 plan 模式開始做。

### 步驟 3：執行分析與畫圖

```text
照計畫寫 scripts/analyze.py：輸出描述統計表 results/summary.csv、
各變項與 target 的相關係數 results/corr.csv、BMI 對 target 的散佈圖 figures/bmi.png、
相關係數長條圖 figures/corr.png。執行它，每個數字都要來自輸出檔。
```

**自我檢查用的參考值：** 本文用 scikit-learn 實際跑過，與 target 相關最高的是 `bmi`（Pearson r = 0.586）與 `s5`（r = 0.566），`s3`（HDL）是負相關（r = −0.395）。學生的結果跟這些不一樣，就要請 Claude 查原因。

### 步驟 4：請子 agent 審查、請 GPT 給第二意見

```text
用 stats-reviewer agent 檢查 scripts/analyze.py 與 results/。
另外用 codex exec 請 GPT 評論「用相關係數回答這個研究問題」有什麼限制，結果存 reviews/gpt.md。
最後列出兩邊意見的異同。
```

### 步驟 5：用 OpenAI 畫封面插圖

```text
執行 python scripts/gen_image.py，幫文章畫一張封面插圖，存成 figures/cover.png。
風格：簡潔的扁平插畫，主題是「生活習慣與血糖健康」，圖上不要有文字或數字。
```

**注意：** AI 插圖只當裝飾。數據圖一定用程式畫，不要讓圖片模型畫圖表，它畫出來的數字不可信。

### 步驟 6：寫成文章

```text
把結果寫成 article.md：標題、封面圖、前言、資料與方法、結果（嵌入 figures/bmi.png 與 figures/corr.png）、
討論與限制、參考資料。每個數字要寫出來自哪個輸出檔；封面圖下方註明「本圖由 AI 生成」。
```

在 VS Code 右鍵 `article.md` 選「開啟預覽」就能看到圖文成品。

!!! note "截圖位置"
    article.md 的 Markdown 預覽，含封面與兩張分析圖（請自行補上截圖）

| 輸出檔 | 用途 | 怎麼看 |
| --- | --- | --- |
| `scripts/analyze.py` | 分析程式 | VS Code 開啟 |
| `results/summary.csv`、`results/corr.csv` | 描述統計與相關係數 | VS Code 或 Excel |
| `figures/bmi.png`、`figures/corr.png` | 分析圖 | 點兩下預覽 |
| `figures/cover.png` | AI 封面插圖 | 點兩下預覽 |
| `reviews/gpt.md` | GPT 的第二意見 | Markdown 預覽 |
| `article.md` | 圖文分析短文 | Markdown 預覽 |

**作業繳交建議：** 除了 `article.md`，也請學生用 `/export prompts.txt` 交出對話紀錄，老師可以看他們怎麼下指令、有沒有檢查結果。

## 十、進階：agent engineering 與 harness

Harness（馬具、外掛架構）是包在模型外面、讓它能用工具反覆工作的那一層程式。Anthropic 自己把 Claude Agent SDK 稱為「general-purpose agent harness」（[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)）。你前面學到的 CLAUDE.md、hook、權限、子 agent，其實就是在調整 Claude Code 這個 harness。Agent engineering 就是有意識地設計這一層。

建議的學習階梯（這個分級是本文的教學安排，不是官方分類）：

1. **提示**：把目標、限制、完成條件寫清楚。
2. **脈絡**：CLAUDE.md、skill、交接檔，決定它知道什麼。
3. **工具**：MCP、腳本（例如 `codex exec`、`gen_image.py`），決定它能做什麼。
4. **管控**：權限模式、hook、檢查關卡，決定它不能做什麼、何時算做完。
5. **編排**：子 agent、agent teams、平行對話。
6. **自建 harness**：用 `claude -p` 寫腳本，或用 Agent SDK 寫程式。

### 練習 1：把重複流程包成 skill

Skill 是一個資料夾加 `SKILL.md`，資料夾名稱就是指令名稱（[來源](https://code.claude.com/docs/en/skills)）。例如把第九章的流程包起來：

```bash
mkdir -p .claude/skills/data-article
```

存成 `.claude/skills/data-article/SKILL.md`：

```markdown
---
description: 把一份資料集做成圖文分析短文。使用者要寫分析文章、資料報告時使用。
---

1. 先提分析計畫，等使用者同意
2. 分析程式放 scripts/，結果放 results/，圖放 figures/
3. 用 stats-reviewer agent 審查
4. 用 python scripts/gen_image.py 畫封面，圖上不要有數字
5. 寫成 article.md，每個數字標出來源檔案
```

之後打 `/data-article` 就會照這個流程走。`/skills` 可以列出所有 skill。

### 練習 2：給 Claude 一個「做完」的檢查

官方最佳實務強調：給 Claude 一個會回傳通過或失敗的檢查，它就能自己修到過（[Best practices](https://code.claude.com/docs/en/best-practices)）。三種強度：

第一種，寫在提問裡，由 Claude 自己判斷：

```text
寫完後執行 pytest，直到全部通過為止
```

第二種，用 `/goal` 設定目標，另一個模型每輪檢查是否達成：

```text
/goal tests/ 全部通過且 article.md 每個數字都有來源
```

最嚴格的是 Stop hook：腳本以 exit code 2 結束時，Claude 不能結束這一輪。以下是把官方範例的 `pnpm tsc` 換成 pytest：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "python -m pytest -q 1>&2 || exit 2" }
        ]
      }
    ]
  }
}
```

官方說明，若連續擋下 8 次且中間沒有任何工具呼叫，Claude Code 會放行結束，不會無限迴圈。

### 練習 3：用腳本批次執行（非互動模式）

`claude -p` 跑一次就結束，可以放進 shell 迴圈。下面是本文的例子，參數都已對照 `claude --help`：

```bash
for f in data/raw/*.csv; do
  claude -p "讀 $f，寫一段 100 字的資料描述到 notes/$(basename $f .csv).md，完成回覆 OK" \
    --allowedTools "Read,Write" \
    --permission-mode dontAsk \
    --max-budget-usd 0.5
 done
```

`--permission-mode dontAsk` 會拒絕所有沒有事先允許的動作；`--max-budget-usd` 官方說明只在 `-p` 模式有效。先拿兩三個檔試跑，沒問題再跑全部。

### 練習 4：用 Agent SDK 寫自己的 agent

Agent SDK 是把 Claude Code 的工具、agent 迴圈、context 管理做成 Python 或 TypeScript 函式庫（[Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)）。官方說明 SDK 要用 API key 認證，不能用 claude.ai 登入。

```bash
pip install claude-agent-sdk
export ANTHROPIC_API_KEY=your-api-key
```

存成 `agent.py`（取自官方 [Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)，只改了 prompt）：

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def main():
    async for message in query(
        prompt="檢查 scripts/analyze.py 會造成程式中斷的 bug，並修正。",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")


asyncio.run(main())
```

```bash
python agent.py
```

### 練習 5：設計一個長任務 harness（小組專題）

Anthropic 工程部落格的兩篇文章可以當設計范本：

- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（2025-11-26）：第一個「初始化 agent」建好環境、一份 JSON 格式的功能清單（每項都先標 `"passes": false`）、`claude-progress.txt` 進度檔與第一個 git commit；之後每個「寫程式 agent」一次只做一個功能、測試、commit、寫進度。文中提到用 JSON 是因為模型比較不會亂改 JSON。
- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)（2026-03-24）：規劃者（planner）、產生者（generator）、評分者（evaluator）三個 agent。文中指出 agent 評自己的作品時傾向過度稱讚，把「做的人」跟「評的人」分開效果更好；也比較了 compaction 與「清空 context 加交接檔」的差別。

小組作業：把第九章改成三個角色。`planner` 寫 `features.json`（每張圖、每個段落一項），`generator` 一次完成一項並更新 `progress.md`，`evaluator`（只讀的子 agent）依評分標準打分，沒過就退回。最後比較：這個版本跟「一句話叫 Claude 寫完」的品質差在哪裡。

## 十一、常見問題排解

| 狀況 | 原因 | 解法 |
| --- | --- | --- |
| VS Code 終端機打 `claude` 出現 command not found | 只裝了擴充套件，沒裝 CLI；或終端機沒重開 | 裝第三章的 CLI，關掉終端機重開，再跑 `claude doctor` |
| Windows 安裝時出現 `'irm' is not recognized` | 在 CMD 貼了 PowerShell 指令 | 改用 CMD 版，或切到 PowerShell |
| 登入後說沒有權限 | 免費 claude.ai 方案不含 Claude Code | 改用 Pro 以上方案或 Console 帳號 |
| `/ide` 顯示 No available IDEs detected | 沒裝 VS Code 擴充套件 | 從擴充功能市集安裝 Claude Code，重開 `claude` |
| `/voice` 聽不懂中文 | 官方支援清單沒有中文 | 講英文，或改用打字 |
| Claude 沒照 CLAUDE.md 做 | CLAUDE.md 是提示不是強制；或檔案太長、有矛盾 | 用 `/context all` 確認有載入；縮到 200 行內；必守規則改用 hook |
| `/compact` 後之前交代的規則不見了 | 只在對話裡講過，沒寫進檔案 | 寫進專案根目錄的 CLAUDE.md，它在 compact 後會重新載入 |
| `/hooks` 看不到新的 hook | JSON 格式錯誤（例如多了逗號或 `//` 註解） | 設定檔是嚴格 JSON；跑 `claude doctor` 看錯誤 |
| 新建的子 agent 叫不出來 | `agents` 資料夾是這次對話開始後才建的 | 重開 Claude Code |
| 網路教學的 `codex mcp-server` 跑不起來 | OpenAI 已移除這個指令 | 改用第八章的 `codex exec` |
| `codex exec` 說不在 git 專案裡 | Codex 預設要求 git 專案 | 加 `--skip-git-repo-check`，或先 `git init` |
| `gen_image.py` 出現認證錯誤 | 沒設 `OPENAI_API_KEY`，或設在另一個終端機 | 在同一個終端機設定後重開 `claude` |
| `gen_image.py` 說模型不存在或沒有權限 | 模型已更名，或組織尚未驗證 | 查 OpenAI Images 文件換 `--model`；完成 Organization Verification |
| 額度下降很快 | effort 太高、開太多子 agent 或 agent teams | `/usage` 看用量；降到 `/effort medium`；不相關的任務之間 `/clear` |
| Claude 往錯誤方向改了一堆 | 提問不夠具體 | 按 `Esc` 停止；`/rewind` 倒回；兩次糾正無效就 `/clear` 重問 |

## 十二、一頁速查與教學建議

### 速查表

| 在哪裡打 | 指令 | 用途 |
| --- | --- | --- |
| 終端機 | `curl -fsSL https://claude.ai/install.sh | bash` | 安裝（macOS/Linux） |
| 終端機 | `irm https://claude.ai/install.ps1 | iex` | 安裝（Windows PowerShell） |
| 終端機 | `claude --version`、`claude doctor` | 確認安裝、診斷 |
| 終端機 | `claude`、`claude -c`、`claude -r <名稱>` | 啟動、接續最近、接續指定對話 |
| 終端機 | `claude -w <名稱>` | 在新 worktree 開對話 |
| 終端機 | `claude -p "<任務>"` | 非互動執行一次 |
| Claude 輸入框 | `/model`、`/effort`、`/config` | 模型、思考深度、設定 |
| Claude 輸入框 | `/voice`、`/statusline` | 語音（僅英文等）、狀態列 |
| Claude 輸入框 | `Shift+Tab`、`/plan` | 切換權限模式、進 plan 模式 |
| Claude 輸入框 | `/init`、`/memory` | 建 CLAUDE.md、管記憶 |
| Claude 輸入框 | `/compact`、`/clear`、`/resume`、`/rewind`、`/rename`、`/export` | 交接與對話管理 |
| Claude 輸入框 | `/hooks`、`/skills`、`/tasks`、`/mcp` | 檢查 hook、skill、背景工作、MCP |
| Claude 輸入框 | `/status`、`/usage`、`/context` | 帳號模型、用量、context |
| Claude 輸入框 | `/goal <條件>` | 設定完成條件 |
| Claude 輸入框 | `Esc`；空白輸入框按兩次 `Esc` | 停止；打開倒回選單 |
| 終端機 | `npm install -g @openai/codex`、`codex exec "<問題>" -o out.md` | 安裝 Codex、請 GPT 回答 |
| 終端機 | `python scripts/gen_image.py "<描述>" -o figures/x.png` | 用 OpenAI 畫圖 |

### 給老師的教學建議

以下是本文的建議，不是官方規定。

1. **前兩堂只用 Manual 與 plan 模式。** 讓學生看清楚每個批准在批什麼，再開放 acceptEdits。auto 與 bypassPermissions 留到進階課。
2. **統一一份課程用 CLAUDE.md。** 寫進「繁體中文回答」「原始資料唯讀」「每個數字要有來源」，每位學生複製一份，教學助教比較好除錯。
3. **先教「檢查」再教「生產」。** 每次作業都要求學生交出 Claude 執行的指令與輸出作證據，而不是只交「它說測試都過了」。官方最佳實務也建議要 Claude 拿出證據。
4. **用第九章的參考值做小測驗。** 例如問「BMI 與 target 的相關係數是多少、在哪個輸出檔」，答不出來就代表沒有驗證 AI 的結果。
5. **API 金鑰與費用事先規劃。** OpenAI API 依用量計費，建議由老師統一產生封面圖，或設好帳號花費上限後再發給學生；金鑰絕不寫進檔案或上傳 GitHub。
6. **教「交接」當成基本功。** 每堂課結束都要學生讓 Claude 寫 HANDOFF.md，下堂課從它開始。這是後面 harness 設計的前身。
7. **開課前重新查證一次。** Claude Code 與 OpenAI 工具更新很快，本文就遇到 `codex mcp-server` 被移除、`gpt-image-1` 停用。上課前用 `claude --version` 與官方文件再對一次指令。
8. **可以接回 VibeCoding-GWAS 課程。** 學完本教學的學生，可以直接進 [Vibe Coding × GWAS](index.md) 的實作，第十章的 skill 與檢查關卡都能套用在 GWAS 流程。

### 查不到官方來源、需要你確認的地方

- Codex CLI 的 Windows 與 Homebrew 安裝指令：OpenAI 頁面有分頁但未能讀取內容；npm 套件名稱已由 npm 註冊表確認。
- 哪些 ChatGPT 方案包含 Codex：OpenAI 頁面未寫明。
- Codex 內建畫圖（`$imagegen`）是否能在 CLI 使用：官方頁面只提到桌面 app。
- `gen_image.py` 與第九章流程未實際呼叫 OpenAI API（這個環境沒有金鑰），已通過語法檢查。第九章的相關係數已實際計算。

### 參考資料（2026-11-19 查閱）

- [Advanced setup](https://code.claude.com/docs/en/setup)、[Use Claude Code in VS Code](https://code.claude.com/docs/en/vs-code)
- [Model configuration](https://code.claude.com/docs/en/model-config)、[Voice dictation](https://code.claude.com/docs/en/voice-dictation)、[Status line](https://code.claude.com/docs/en/statusline)、[Permission modes](https://code.claude.com/docs/en/permission-modes)、[Commands](https://code.claude.com/docs/en/commands)
- [Memory](https://code.claude.com/docs/en/memory)、[Hooks guide](https://code.claude.com/docs/en/hooks-guide)、[Subagents](https://code.claude.com/docs/en/sub-agents)、[Agent teams](https://code.claude.com/docs/en/agent-teams)、[Skills](https://code.claude.com/docs/en/skills)
- [Best practices](https://code.claude.com/docs/en/best-practices)、[Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)、[Agent SDK quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)
- [Codex MCP server removal](https://learn.chatgpt.com/docs/mcp-server)、[Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)、[Codex CLI](https://learn.chatgpt.com/codex/cli)
- [OpenAI Image generation](https://developers.openai.com/api/docs/guides/image-generation)、[Images API reference](https://developers.openai.com/api/reference/resources/images/methods/generate)
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)、[Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Efron, B., Hastie, T., Johnstone, I., & Tibshirani, R. (2004). Least angle regression. *Annals of Statistics, 32*(2), 407–499.
