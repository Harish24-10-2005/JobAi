# 🚀 JobAI - Career Command Center

> **Autonomous Job Research & Auto-Apply Agent**

An intelligent multi-agent system that automates your job search workflow - from discovering opportunities to filling out applications automatically.

![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Smart Job Discovery** | Searches major ATS platforms (Greenhouse, Lever, Ashby) using SerpAPI |
| 🧠 **AI-Powered Analysis** | Analyzes job postings against your resume using Groq LLM |
| 🎯 **Match Scoring** | Calculates compatibility score (0-100) with skills breakdown |
| 🚀 **Auto-Apply** | Browser automation fills forms and uploads resume automatically |
| 👤 **Human-in-the-Loop** | Prompts for input when encountering unknown fields |
| 📊 **Rich Terminal Output** | Beautiful, colorful progress tracking and summaries |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    JobApplicationWorkflow                        │
│                    (Orchestration Layer)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ 🔍 ScoutAgent │───▶│ 🧠 AnalystAgent│───▶│ 🚀 ApplierAgent│    │
│  │              │    │              │    │              │       │
│  │  SerpAPI     │    │  Groq LLM    │    │ Browser-Use  │       │
│  │  Google      │    │  llama-3.3   │    │  Chrome      │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

| Agent | Purpose | Technology |
|-------|---------|------------|
| **ScoutAgent** | Find job listings on ATS platforms | SerpAPI + Google Search |
| **AnalystAgent** | Analyze job-resume match & score | Groq LLM (llama-3.3-70b) |
| **ApplierAgent** | Automate form filling & submission | browser-use + Chrome |

---

## 📁 Project Structure

```
JobAI/
├── 📄 main.py                    # Entry point
├── 📄 requirements.txt           # Dependencies
├── 📄 pyproject.toml             # UV package config
├── 📄 .env                       # API keys (create from .env.example)
│
├── 📂 src/
│   ├── 📄 main.py                # Async workflow runner
│   │
│   ├── 📂 automators/            # AI Agents
│   │   ├── base.py               # Abstract base agent
│   │   ├── scout.py              # Job search agent
│   │   ├── analyst.py            # Job analysis agent
│   │   └── applier.py            # Application agent
│   │
│   ├── 📂 core/                  # Infrastructure
│   │   ├── config.py             # Settings management
│   │   ├── logger.py             # Logging setup
│   │   └── console.py            # Rich terminal output
│   │
│   ├── 📂 models/                # Data models
│   │   ├── job.py                # JobAnalysis model
│   │   └── profile.py            # UserProfile model
│   │
│   ├── 📂 workflows/             # Business logic
│   │   └── job_manager.py        # Main workflow
│   │
│   └── 📂 data/                  # User data
│       ├── user_profile.yaml     # Your profile
│       └── Resume_ATS_friendly.pdf
│
└── 📂 test/                      # Test scripts
    └── agenttest.py              # Agent testing
```

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.12+
- Google Chrome installed
- UV package manager (recommended)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/JobAI.git
cd JobAI

# Create virtual environment
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
uv sync
# or: pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Add your API keys:

```env
# Required
GROQ_API_KEY=your_groq_api_key
SERPAPI_API_KEY=your_serpapi_key
OPENROUTER_API_KEY=your_openrouter_key
```

### 4. Setup Your Profile

Edit `src/data/user_profile.yaml` with your information:

```yaml
personal_information:
  first_name: "Your"
  last_name: "Name"
  email: "your.email@example.com"
  phone: "1234567890"
  # ... more fields

files:
  resume: "D:\\path\\to\\your\\Resume.pdf"
```

### 5. Run the Workflow

```bash
# Basic usage
python src/main.py "Software Engineer" "Remote"

# Custom search
python src/main.py "Data Scientist" "San Francisco"
```

---

## 🔑 API Keys

| Service | Purpose | Get Key |
|---------|---------|---------|
| **Groq** | LLM for job analysis | [console.groq.com](https://console.groq.com) |
| **SerpAPI** | Google job search | [serpapi.com](https://serpapi.com) |
| **OpenRouter** | Browser agent LLM | [openrouter.ai](https://openrouter.ai) |

---

## 📊 Sample Output

```
╔══════════════════════════════════════════════════════════════════╗
║           🚀 JobAI - Career Command Center 🚀                    ║
║           Autonomous Job Research & Auto-Apply Agent             ║
╚══════════════════════════════════════════════════════════════════╝

  Configuration:
    🔍 Query:    Software Engineer
    🌍 Location: Remote
    🕐 Started:  2026-01-17 14:20:00

🔍 SCOUT AGENT ─────────────────────────────────────────────────────
  ✅ Found 15 job listings

  🔗 Job Listings
  ╭────┬─────────────────┬──────────────────────────────╮
  │ #  │    Platform     │          Job Path            │
  ├────┼─────────────────┼──────────────────────────────┤
  │ 1  │ greenhouse.io   │ example-company/jobs/123...  │
  │ 2  │ lever.co        │ another-company/software...  │
  ╰────┴─────────────────┴──────────────────────────────╯

🧠 ANALYST AGENT ───────────────────────────────────────────────────

╭─────────────────────── 🎯 JOB DETAILS ────────────────────────╮
│ 👤 Role: Senior Software Engineer                              │
│ 🏢 Company: TechCorp Inc                                       │
│ 💰 Salary: $150,000 - $200,000                                 │
│ 🛠️ Tech: Python, FastAPI, React, Docker                       │
╰────────────────────────────────────────────────────────────────╯

  Match Score: 85% ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░ 🟢 EXCELLENT

╭───────────────────── 📊 SKILLS ANALYSIS ──────────────────────╮
│ ✓ Matching: Python, FastAPI, React, Docker                     │
│ ✗ Missing: Kubernetes                                          │
╰────────────────────────────────────────────────────────────────╯

🚀 APPLIER AGENT ───────────────────────────────────────────────────
  [14:21:15] → Initializing browser - Chrome automation starting...
  [14:21:18] → Running browser agent - Navigating and filling forms...
  ✅ Application process completed! 🎉

════════════════════════════════════════════════════════════════════

  📊 Session Summary
  ╭────────────────────────┬───────┬────╮
  │        Metric          │ Count │    │
  ├────────────────────────┼───────┼────┤
  │ Total Jobs Found       │ 15    │ 🔍 │
  │ Jobs Analyzed          │ 15    │ 🧠 │
  │ Applications Submitted │ 8     │ 🚀 │
  │ Jobs Skipped           │ 7     │ ⏭️ │
  ╰────────────────────────┴───────┴────╯
```

---

## ⚙️ Configuration Options

### Browser Settings (in `src/core/config.py`)

```python
chrome_path: str = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data_dir: str = r"C:\Users\YOUR_USER\AppData\Local\Google\Chrome\User Data"
profile_directory: str = "Profile 1"  # Your Chrome profile
headless: bool = False  # Set True for background execution
```

### Match Score Threshold

In `job_manager.py`, adjust minimum score for auto-apply:

```python
await workflow.run(query, location, min_match_score=70)  # Default: 70
```

---

## 🛠️ Development

### Run Tests

```bash
# Test individual agents
python test_applier.py

# Test with specific job
python test/agenttest.py
```

### Project Commands

```bash
# Sync dependencies
uv sync

# Add new package
uv add package_name

# Run linter
uv run ruff check .
```

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

This tool is for educational purposes. Always review applications before final submission. Respect job posting terms of service and rate limits.

---

<p align="center">
  Built with ❤️ using LangChain, Groq, and browser-use
</p>
