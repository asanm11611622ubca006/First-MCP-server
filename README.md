# 🏥 Patient Data MCP Server

Welcome to the **Patient Data MCP (Model Context Protocol) Server** project! 🚀 

This is a beginner-friendly project showing how to connect **Claude Desktop** to your own local Python data sources. It lets you chat with a synthetic patient dataset containing 200 health records. 🧑‍⚕️📊

If you are a student or developer wanting to learn how to bridge LLMs with real-world databases, this is a perfect starting point! 💡

---

## 🛠️ Features

This server currently provides **6 powerful tools** to Claude:
1. 🔍 **`get_patient_by_id`** — Look up a specific patient record.
2. 🎂 **`list_patients_above_age`** — Find older patients based on an age threshold.
3. 🦠 **`find_patients_by_disease`** — Search for patients by their diagnosis (e.g., Asthma, Diabetes).
4. 📋 **`list_all_diseases`** — See all unique diseases present in the dataset.
5. 👤 **`search_patients_by_name`** — Quickly find someone by their partial or full name.
6. 📈 **`get_patient_statistics`** — Receive a beautiful statistical breakdown of the dataset.

---

## 🖥️ Getting Started

### 1️⃣ Prerequisites
You will need a few things installed on your machine:
- **Python 3.10+** (🐍)
- **uv** (⚡ A blazing fast Python package runner). Install it via terminal:
  - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows: `irm https://astral.sh/uv/install.ps1 | iex`
- **Claude Desktop App** (🤖)

### 2️⃣ Clone the Repository
Download the code to your computer:
```bash
git clone https://github.com/asanm11611622ubca006/First-MCP-server.git
cd First-MCP-server
```

*(Optional)* Run `python generate_dataset.py` if you ever want to regenerate the randomized `patients.csv` file!

### 3️⃣ Connect to Claude Desktop! 🔌
You don't need to run the server in your terminal. Claude will automatically run it in the background!

1. Open your Claude Desktop config file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Add the following JSON configuration. Make sure to update the `--directory` path to where you saved the code on your computer!

```json
{
  "mcpServers": {
    "patient-data-server": {
      "command": "uv",
      "args": [
        "--directory",
        "YOUR_FULL_PATH_HERE\\First_MCP_server", 
        "run",
        "patient_server.py"
      ]
    }
  }
}
```
*(⚠️ Windows users: Remember to use double backslashes `\\` in path names!)*

### 4️⃣ Start Chatting! 💬
1. **Restart Claude Desktop** (fully quit from the system tray and reopen).
2. Look for the little 🔨 (Hammer) icon in the chat bar. You should see the `patient-data-server` features loaded!
3. Try asking:
   - *"What are the most common diseases in the patient database?"*
   - *"Can you find patients with Hypertension?"*
   - *"Get patient by ID 42"*

---

## 🌱 Learning & Contributing
This project is an awesome way to learn how the Model Context Protocol works. You can easily open `patient_server.py` and modify it. 

Try adding a new tool to find patients by `gender`, or swap out the CSV parsing for an SQL database! 👩‍💻👨‍💻

Happy coding! 🎉
