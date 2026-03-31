# 🤖 Smart Support Triage Agent
### *An AI-Powered Micro-Service for Intelligent Ticket Routing*

Built with the **Google Agent Development Kit (ADK)** and **Gemini 2.5 Flash**, this agent automates the first line of customer support by instantly categorizing and prioritizing incoming user messages.



---

## 🚀 Overview
Traditional support systems rely on static keyword matching. The **Smart Support Triage Agent** uses LLM-driven reasoning to understand user intent and sentiment, providing a structured JSON response ready for any CRM or backend integration.

### **Core Capabilities**
* **Semantic Categorization:** Sorts tickets into 7+ business-critical categories (Billing, Tech Support, etc.).
* **Urgency Assessment:** Analyzes sentiment to assign a priority level from `low` to `urgent`.
* **Structured Output:** Guaranteed JSON format for seamless machine-to-machine communication.
* **Stateless & Scalable:** Hosted on **Google Cloud Run** as a lightweight, callable HTTP endpoint.

---

## 🛠️ Technical Architecture
This project utilizes a **Sequential Agent Pattern** to ensure deterministic execution and data integrity.

1.  **Categorizer Agent:** Analyzes the raw input and identifies the primary intent.
2.  **Prioritizer Agent:** Inherits the context from the Categorizer, assesses the urgency, and synthesizes the final state.
3.  **Sequential Orchestrator:** Manages the "Assembly Line" flow and state persistence between inferences.

### **Tech Stack**
* **LLM:** Gemini 2.5 Flash
* **Orchestration:** Google ADK (Agent Development Kit)
* **Infrastructure:** Google Cloud Run (Serverless)
* **Language:** Python / ADK CLI

---

## 📂 Project Structure
```text
.
├── agent.py          # Main ADK Agent definitions (Sequential Logic)
├── app.py            # Flask/FastAPI wrapper for HTTP Cloud Run deployment
├── Dockerfile        # Containerization for Cloud Run
├── requirements.txt  # Dependencies (google-adk, etc.)
└── README.md         # You are here!
```

---

## ⚡ Quick Start

### **Prerequisites**
* Python 3.10+
* Google Cloud Project with Gemini API enabled
* ADK CLI installed

### **Installation**
1. **Clone the repo:**
   ```bash
   git clone https://github.com/your-username/smart-triage-agent.git
   cd smart-triage-agent
   ```
2. **Install dependencies:**
   ```bash
   uv pip install google-adk
   ```
3. **Run the agent locally:**
   ```bash
   adk web --allow_origins="*"
   ```

---

## 📊 Sample Input/Output

**Input:**
> "My dashboard is showing a 404 error and I have a client demo in 10 minutes! Please help!"

**Final Output:**
```json
{
  "category": "technical_support",
  "priority": "urgent"
}
```

---

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.

