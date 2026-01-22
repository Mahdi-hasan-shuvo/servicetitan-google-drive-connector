<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Google%20Drive-API%20v3-4285F4?style=for-the-badge&logo=googledrive&logoColor=white" alt="Google Drive">
  <img src="https://img.shields.io/badge/ServiceTitan-Integration-FF6B35?style=for-the-badge" alt="ServiceTitan">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

<h1 align="center">
  🔄 ServiceTitan ↔ Google Drive Sync
</h1>

<p align="center">
  <strong>Seamless bi-directional file synchronization between ServiceTitan projects and Google Drive</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-api-reference">API Reference</a>
</p>

---

## 🌟 Features

<table>
<tr>
<td width="50%">

### 🔄 Bi-Directional Sync
Automatically sync files **both ways**:
- ServiceTitan → Google Drive
- Google Drive → ServiceTitan

</td>
<td width="50%">

### ⚡ Multi-Threaded
Concurrent processing with **5 parallel workers** for blazing-fast synchronization

</td>
</tr>
<tr>
<td width="50%">

### 🛡️ Fault Tolerant
Built-in **retry mechanism** with exponential backoff for handling SSL errors and network issues

</td>
<td width="50%">

### 🔁 Continuous Monitoring
Runs in an **infinite loop** with configurable intervals to keep files in sync 24/7

</td>
</tr>
</table>

---

## 📁 Project Structure

```
📦 servicetitan-drive-sync
├── 📄 main.py              # Main synchronization engine
├── 📂 servicetitan/
│   └── 📄 API.py           # ServiceTitan API client
├── 📂 Google/
│   └── 📄 api.py           # Google Drive manager
├── 📄 config.json          # Configuration file
├── 📄 requirements.txt     # Dependencies
└── 📂 Downloads/           # Temporary download folder
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Cloud Console project with Drive API enabled
- ServiceTitan account with API access

### Installation

**1️⃣ Clone the repository**
```bash
git clone https://github.com/yourusername/servicetitan-drive-sync.git
cd servicetitan-drive-sync
```

**2️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

**3️⃣ Set up Google OAuth credentials**

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project (or select existing)
- Enable the **Google Drive API**
- Create OAuth 2.0 credentials
- Download the `client_secret.json` file

**4️⃣ Configure the application**

Create a `config.json` file:
```json
{
    "Cookies": "your_servicetitan_cookies_here",
    "TOKEN_FILE": "token.json",
    "CLIENT_SECRET_FILE": "client_secret.json"
}
```

**5️⃣ Run the sync**
```bash
python main.py
```

---

## ⚙️ Configuration

### config.json

| Key | Description | Example |
|-----|-------------|---------|
| `Cookies` | ServiceTitan session cookies | `"session=abc123..."` |
| `TOKEN_FILE` | Path to Google OAuth token | `"token.json"` |
| `CLIENT_SECRET_FILE` | Path to Google OAuth credentials | `"client_secret.json"` |

### Customization Options

```python
# In main.py - Adjust these values as needed

ThreadPoolExecutor(max_workers=5)  # Number of parallel threads
time.sleep(10)                      # Seconds between sync cycles
max_retries=3                       # Number of retry attempts
```

---

## 🔄 How It Works

```
┌─────────────────┐                      ┌─────────────────┐
│                 │                      │                 │
│  ServiceTitan   │◄────── SYNC ───────►│  Google Drive   │
│    Projects     │                      │    Folders      │
│                 │                      │                 │
└────────┬────────┘                      └────────┬────────┘
         │                                        │
         ▼                                        ▼
┌─────────────────┐                      ┌─────────────────┐
│  Get all        │                      │  Get all        │
│  project IDs    │                      │  folders        │
└────────┬────────┘                      └────────┬────────┘
         │                                        │
         └────────────────┬───────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   Match folders by    │
              │   name (case-insens.) │
              └───────────┬───────────┘
                          │
         ┌────────────────┴────────────────┐
         │                                 │
         ▼                                 ▼
┌─────────────────┐               ┌─────────────────┐
│  Files missing  │               │  Files missing  │
│  in Drive?      │               │  in ServiceTitan│
│                 │               │                 │
│  Download from  │               │  Download from  │
│  ServiceTitan   │               │  Google Drive   │
│       ↓         │               │       ↓         │
│  Upload to      │               │  Upload to      │
│  Google Drive   │               │  ServiceTitan   │
└─────────────────┘               └─────────────────┘
```

---

## 📚 API Reference

### Google Drive Manager

```python
from Google.api import GoogleDriveManager

drive = GoogleDriveManager()
```

| Method | Description | Returns |
|--------|-------------|---------|
| `get_all_folders()` | Get all folders from Drive | `list[dict]` |
| `get_files_in_folder(folder_id)` | List files in a folder | `list[dict]` |
| `download_file(file_id, destination)` | Download a file | `str` (path) |
| `upload_file(local_path, folder_id)` | Upload a file | `dict` |
| `create_folder(name, parent_id)` | Create new folder | `dict` |
| `search_files(query)` | Search files by name | `list[dict]` |

### ServiceTitan API

```python
from servicetitan import API as webAPI
```

| Method | Description | Returns |
|--------|-------------|---------|
| `serch_project_id(coki)` | Get all project IDs | `set` |
| `get_all_folder_id(sourceId, coki)` | Get folders in project | `list[dict]` |
| `get_file_info(sourceId, file_id, coki)` | Get files in folder | `list[dict]` |
| `DownloadFile(url, output_file, coki)` | Download file | `str` (path) |
| `Uploads_file(file_path, sourceId, folder_id, coki)` | Upload file | `Response` |

---

## 📊 Example Output

```
[142] Syncing files... Source ID: 12345678
[14:32:15] Name: invoice_001.pdf | ID: 987654
✅ Uploaded: invoice_001.pdf
[14:32:18] Name: contract_draft.docx | ID: 456789
✅ Downloaded: Downloads/contract_draft.docx
[14:32:21] Cycle complete. Waiting...
```

---

## 🛠️ Troubleshooting

<details>
<summary><strong>🔴 SSL Error: Connection reset</strong></summary>

This usually happens when too many concurrent connections are made. Try:
- Reducing `max_workers` in `ThreadPoolExecutor`
- The built-in retry mechanism should handle temporary SSL issues

</details>

<details>
<summary><strong>🔴 Google OAuth token expired</strong></summary>

Delete your `token.json` file and run the script again. You'll be prompted to re-authenticate.

</details>

<details>
<summary><strong>🔴 ServiceTitan cookies expired</strong></summary>

1. Log into ServiceTitan in your browser
2. Open Developer Tools → Network tab
3. Copy the new cookie values to `config.json`

</details>

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 Video

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


https://github.com/user-attachments/assets/fefaef16-a73f-4589-985a-8d930efbc154


---

## 👨‍💻 Author
---

## 💼 Contact Me for Paid Projects

Have a project in mind or need expert help?  
I'm available for **freelance work and paid collaborations**.

### 📬 Get in Touch

- 📧 **Email**: [shuvobbhh@gmail.com](mailto:shuvobbhh@gmail.com)
- 💬 **Telegram**: [+8801616397082](https://t.me/+8801616397082)
- 📱 **WhatsApp**: [+8801616397082](https://wa.me/8801616397082)
- 🌐 **Portfolio**: [mahdi-hasan-shuvo.github.io](https://mahdi-hasan-shuvo.github.io/Mahdi-hasan-shuvo/)
- 💻 **GitHub**: [@Mahdi-hasan-shuvo](https://github.com/Mahdi-hasan-shuvo)

> *"Quality work speaks louder than words. Let's build something remarkable together."*


---

<p align="center">
  <sub>Built with ❤️ for seamless file synchronization</sub>
</p>
