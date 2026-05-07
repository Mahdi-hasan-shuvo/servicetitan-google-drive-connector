<div align="center">

<!-- HEADER BANNER -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:4285F4,50:FF6B35,100:0F9D58&height=200&section=header&text=ServiceTitan%20%E2%86%94%20Google%20Drive&fontSize=40&fontColor=ffffff&fontAlignY=38&desc=Bi-directional%20File%20Sync%20Automation&descAlignY=58&descColor=ffffffcc&animation=fadeIn" alt="Header Banner"/>

<!-- BADGES -->
<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google%20Drive-API%20v3-4285F4?style=for-the-badge&logo=googledrive&logoColor=white"/>
  <img src="https://img.shields.io/badge/ServiceTitan-Integration-FF6B35?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-BSD--3--Clause-0F9D58?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Threads-5%20Parallel-blueviolet?style=for-the-badge&logo=lightning"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square"/>
  <img src="https://img.shields.io/badge/Sync-Bi--Directional-orange?style=flat-square"/>
  <img src="https://img.shields.io/badge/Monitoring-24%2F7-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Retry-Auto%20Backoff-red?style=flat-square"/>
</p>
 
<br/>

> **🔄 Keep your ServiceTitan project files and Google Drive perfectly in sync — automatically, continuously, and reliably.**

<br/>

[🚀 Quick Start](#-quick-start) &nbsp;•&nbsp;
[⚙️ Configuration](#%EF%B8%8F-configuration) &nbsp;•&nbsp;
[🏗️ Architecture](#%EF%B8%8F-architecture) &nbsp;•&nbsp;
[📚 API Reference](#-api-reference) &nbsp;•&nbsp;
[🛠️ Troubleshooting](#%EF%B8%8F-troubleshooting)

</div>

---

## 🌟 What Is This?

**ServiceTitan ↔ Google Drive Connector** is a Python-powered automation tool that bridges your **ServiceTitan project management platform** and **Google Drive** — keeping files perfectly mirrored between both systems with zero manual effort.

Whether a file is added in ServiceTitan or Google Drive, this tool automatically detects it, downloads it, and uploads it to the other platform — running continuously in the background with multi-threaded speed and built-in fault tolerance.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔄 **Bi-Directional Sync** | Files sync both ways: ServiceTitan → Drive **and** Drive → ServiceTitan |
| ⚡ **Multi-Threaded** | 5 parallel workers process files concurrently for maximum speed |
| 🛡️ **Fault Tolerant** | Exponential backoff retry on SSL errors and network hiccups |
| 🔁 **Continuous Monitoring** | Runs in an infinite loop — always watching, always syncing |
| 📁 **Smart Folder Matching** | Matches folders by name (case-insensitive) across both platforms |
| 🧩 **Modular Design** | Clean separation of ServiceTitan API, Google Drive API, and sync logic |

---

## 📁 Project Structure

```
📦 servicetitan-google-drive-connector/
│
├── 📄 main.py                  ← 🧠 The brain — orchestrates all sync logic
│
├── 📂 servicetitan/
│   └── 📄 API.py               ← 🔌 ServiceTitan API client (auth, projects, files)
│
├── 📂 Google/
│   └── 📄 api.py               ← ☁️ Google Drive manager (OAuth2, upload/download)
│
├── 📂 Downloads/               ← 📥 Temporary staging folder for transferred files
│
├── 📄 config.json              ← 🔑 Your credentials and settings (never commit this!)
├── 📄 requirements.txt         ← 📦 Python dependencies
├── 📄 .gitignore               ← 🚫 Keeps secrets and temp files out of git
└── 📄 LICENSE                  ← 📜 BSD-3-Clause
```

> **💡 Tip:** The `Downloads/` folder is just a temporary staging area — files are moved there briefly during transfer and cleaned up automatically.

---

## 🚀 Quick Start

### Step 0 — Prerequisites

Before you begin, make sure you have:

- ✅ **Python 3.10+** installed ([Download here](https://python.org))
- ✅ A **Google Cloud project** with Drive API enabled
- ✅ A **ServiceTitan account** with API/web access

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Mahdi-hasan-shuvo/servicetitan-google-drive-connector.git
cd servicetitan-google-drive-connector
```

---

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 3 — Set Up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select an existing one)
3. Navigate to **APIs & Services → Library**
4. Search for **"Google Drive API"** and click **Enable**
5. Go to **APIs & Services → Credentials**
6. Click **Create Credentials → OAuth 2.0 Client ID**
7. Choose **Desktop App**, give it a name, and click **Create**
8. Download the JSON file and rename it to `client_secret.json`
9. Place `client_secret.json` in the project root

---

### Step 4 — Get Your ServiceTitan Cookies

ServiceTitan uses session-based authentication. Here's how to grab your cookies:

1. Log in to your ServiceTitan account in your browser
2. Open **Developer Tools** (`F12` or `Ctrl+Shift+I`)
3. Go to the **Network** tab and refresh the page
4. Click on any request to `*.servicetitan.com`
5. Under **Request Headers**, find and copy the `Cookie:` value

---

### Step 5 — Configure the App

Create a `config.json` file in the project root:

```json
{
    "Cookies": "your_full_servicetitan_cookie_string_here",
    "TOKEN_FILE": "token.json",
    "CLIENT_SECRET_FILE": "client_secret.json"
}
```

> ⚠️ **Never commit `config.json` to git!** It contains sensitive credentials. It's already in `.gitignore` — keep it that way.

---

### Step 6 — Run the Sync!

```bash
python main.py
```

On the **first run**, a browser window will open asking you to authorize Google Drive access. After authorization, a `token.json` file is saved for future runs.

**Expected output:**
```
[142] Syncing files... Source ID: 12345678
[14:32:15] Name: invoice_001.pdf | ID: 987654
✅ Uploaded: invoice_001.pdf → Google Drive
[14:32:18] Name: contract_draft.docx | ID: 456789
✅ Downloaded: Downloads/contract_draft.docx → ServiceTitan
[14:32:21] Sync cycle complete. Waiting 10 seconds...
```

---

## ⚙️ Configuration

### `config.json` Reference

| Key | Required | Description |
|---|---|---|
| `Cookies` | ✅ Yes | ServiceTitan session cookie string |
| `TOKEN_FILE` | ✅ Yes | Path to save/load Google OAuth token |
| `CLIENT_SECRET_FILE` | ✅ Yes | Path to your Google OAuth credentials file |

---

### Tunable Parameters in `main.py`

```python
# ─── Performance ────────────────────────────────────────
ThreadPoolExecutor(max_workers=5)   # ↑ Increase for faster sync on good connections
                                    # ↓ Decrease if you hit rate limits

# ─── Monitoring Interval ────────────────────────────────
time.sleep(10)                      # Seconds to wait between sync cycles
                                    # Set higher (e.g. 60) to reduce API calls

# ─── Retry Logic ────────────────────────────────────────
max_retries=3                       # How many times to retry a failed operation
```

---

## 🏗️ Architecture

### How the Sync Works

```
┌───────────────────────────────────────────────────────────────┐
│                        main.py (Orchestrator)                 │
│                                                               │
│  1. Load config.json credentials                              │
│  2. Initialize ServiceTitan + Google Drive clients            │
│  3. Start infinite sync loop:                                 │
│                                                               │
│     ┌─────────────────┐              ┌──────────────────────┐ │
│     │  ServiceTitan   │◄────SYNC────►│    Google Drive      │ │
│     │    Projects     │              │      Folders         │ │
│     └────────┬────────┘              └──────────┬───────────┘ │
│              │                                  │             │
│              └──────────┬───────────────────────┘             │
│                         │                                     │
│              ┌──────────▼──────────────┐                      │
│              │  Match folders by name  │                      │
│              │  (case-insensitive)     │                      │
│              └──────────┬──────────────┘                      │
│                         │                                     │
│           ┌─────────────┴─────────────┐                       │
│           │                           │                       │
│  ┌────────▼────────┐         ┌────────▼────────┐              │
│  │ File missing    │         │ File missing    │              │
│  │ in Drive?       │         │ in ServiceTitan?│              │
│  │                 │         │                 │              │
│  │ ① Download from │         │ ① Download from │              │
│  │   ServiceTitan  │         │   Google Drive  │              │
│  │ ② Upload to     │         │ ② Upload to     │              │
│  │   Google Drive  │         │   ServiceTitan  │              │
│  └─────────────────┘         └─────────────────┘              │
│                                                               │
│  4. Wait N seconds → Repeat forever                           │
└───────────────────────────────────────────────────────────────┘
```

### Retry & Fault Tolerance

```
Attempt 1 → Fails (SSL Error)
    ↓ wait 1s
Attempt 2 → Fails (Timeout)
    ↓ wait 2s
Attempt 3 → ✅ Success!
```

The retry mechanism uses **exponential backoff**, meaning each retry waits progressively longer — preventing thundering herd issues and respecting API rate limits.

---

## 📚 API Reference

### `Google/api.py` — Google Drive Manager

```python
from Google.api import GoogleDriveManager

drive = GoogleDriveManager()
```

| Method | Parameters | Returns | Description |
|---|---|---|---|
| `get_all_folders()` | — | `list[dict]` | Retrieve all folders from Drive |
| `get_files_in_folder()` | `folder_id: str` | `list[dict]` | List all files inside a folder |
| `download_file()` | `file_id: str, destination: str` | `str` (path) | Download a file to local disk |
| `upload_file()` | `local_path: str, folder_id: str` | `dict` | Upload a local file to Drive |
| `create_folder()` | `name: str, parent_id: str` | `dict` | Create a new folder in Drive |
| `search_files()` | `query: str` | `list[dict]` | Search files by name/query |

---

### `servicetitan/API.py` — ServiceTitan Client

```python
from servicetitan import API as webAPI
```

| Method | Parameters | Returns | Description |
|---|---|---|---|
| `serch_project_id()` | `coki: str` | `set` | Get all project IDs from ServiceTitan |
| `get_all_folder_id()` | `sourceId: str, coki: str` | `list[dict]` | Get all folders inside a project |
| `get_file_info()` | `sourceId: str, file_id: str, coki: str` | `list[dict]` | Get files within a folder |
| `DownloadFile()` | `url: str, output_file: str, coki: str` | `str` (path) | Download a file from ServiceTitan |
| `Uploads_file()` | `file_path: str, sourceId: str, folder_id: str, coki: str` | `Response` | Upload a file to ServiceTitan |

---

## 🛠️ Troubleshooting

### 🔴 `SSLError: Connection reset by peer`

This happens when too many concurrent connections overwhelm the server.

**Fix:**
```python
# In main.py, reduce the thread count:
ThreadPoolExecutor(max_workers=2)  # Try 2 instead of 5
```
The built-in retry mechanism will also handle temporary SSL failures automatically.

---

### 🔴 `Google OAuth token expired`

Your `token.json` has expired or been revoked.

**Fix:**
```bash
# Delete the old token and re-authenticate
rm token.json
python main.py  # Browser will open for fresh login
```

---

### 🔴 `ServiceTitan cookies expired`

Session cookies typically expire after a few hours of inactivity.

**Fix:**
1. Log into ServiceTitan in your browser
2. Open DevTools → **Network** tab → refresh page
3. Click any `servicetitan.com` request
4. Copy the full `Cookie:` header value
5. Update `"Cookies"` in your `config.json`

---

### 🔴 `File not syncing / being skipped`

Possible causes:
- Folder names don't match between ServiceTitan and Drive (check capitalization — matching is case-insensitive but must otherwise be identical)
- File already exists on the destination (sync skips duplicates)
- API rate limit hit — try increasing `time.sleep()` value

---

## 📦 Dependencies

```txt
# requirements.txt
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
requests
```

Install all at once:
```bash
pip install -r requirements.txt
```
# Damo Vide 
https://github.com/user-attachments/assets/1b10dd43-0de2-476a-a4ff-c4d14522a497





---





## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a **Pull Request** — describe what you changed and why

Please follow clear commit messages and test your changes before submitting.

---

## 📄 License

This project is licensed under the **BSD-3-Clause License** — see the [LICENSE](./LICENSE) file for details.

---

## 👨‍💻 Author & Contact

<div align="center">

**Mahdi Hasan Shuvo**
*Python Developer • Automation Engineer • API Integration Specialist*

| Platform | Link |
|---|---|
| 📧 Email | [shuvobbhh@gmail.com](mailto:shuvobbhh@gmail.com) |
| 💬 Telegram | [@+8801616397082](https://t.me/+8801616397082) |
| 📱 WhatsApp | [+8801616397082](https://wa.me/8801616397082) |
| 🌐 Portfolio | [mahdi-hasan-shuvo.github.io](https://mahdi-hasan-shuvo.github.io/Mahdi-hasan-shuvo/) |
| 💻 GitHub | [@Mahdi-hasan-shuvo](https://github.com/Mahdi-hasan-shuvo) |

> *"Quality work speaks louder than words. Let's build something remarkable together."*

💼 **Available for freelance work and paid collaborations!**

</div>

---

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0F9D58,50:FF6B35,100:4285F4&height=120&section=footer&animation=fadeIn" alt="Footer Banner"/>

**Built with ❤️ for seamless, automated file synchronization**

⭐ If this project helped you, please give it a star!

</div>
