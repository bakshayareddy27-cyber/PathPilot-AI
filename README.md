# 🧭 PathPilot AI

### *Don't just recommend what to learn. Decide what to learn next.*

PathPilot AI is an intelligent, personalized learning path system that analyzes a learner's **career goals, current skills, prerequisites, experience level, interests, available time, and learning constraints** to determine what they should learn next.

Unlike traditional learning platforms that simply provide a list of courses, PathPilot AI uses a **deterministic intelligence engine** to reason about skill gaps, prerequisite dependencies, learning feasibility, and career priorities.

## 🎯 The Problem

Learners often know where they want to go but struggle to answer:

> **What should I learn next?**

Learning resources are everywhere, but choosing the right sequence is difficult.

A learner might:

* Learn advanced topics before mastering prerequisites
* Spend time on skills that don't strongly support their career goal
* Follow generic roadmaps that ignore their existing knowledge
* Create unrealistic learning timelines
* Not realize what is blocking their progress

PathPilot AI is designed to solve this problem.

---

## 🧠 How PathPilot AI Thinks

PathPilot AI doesn't randomly generate recommendations.

Its core intelligence engine analyzes multiple signals:

```text
Career Goal
     ↓
Skill Gap Analysis
     ↓
Prerequisite Validation
     ↓
Career Priority + Skill Relevance
     ↓
Experience & Difficulty Matching
     ↓
Time Feasibility
     ↓
🎯 Next Best Action
```

The system combines deterministic decision-making with an optional AI explanation layer.

---

## ✨ Key Features

### 🎯 Next Best Action Engine

Instead of giving learners a massive list of things to study, PathPilot AI identifies:

> **The single most valuable skill to learn next.**

Recommendations are scored using factors such as:

* Career priority
* Career relevance
* Prerequisite unlocking value
* Interest alignment
* Difficulty compatibility
* Time feasibility

---

### 🧩 Recursive Prerequisite Intelligence

PathPilot AI analyzes skill dependencies recursively.

If a learner wants to learn an advanced skill but is missing foundational knowledge, the system identifies the **root blockers**.

Example:

```text
Machine Learning
        ↑
Linear Algebra
        ↑
Mathematics Fundamentals
```

Instead of simply saying:

> ❌ Learn Machine Learning

PathPilot AI can identify:

> ✅ Start with Mathematics Fundamentals.

---

### 📊 Skill Gap Analysis

The system compares:

```text
Current Skills
        VS
Career Requirements
```

and identifies:

* Skills already possessed
* Missing skills
* Prioritized skill gaps

---

### ❤️ Path Health Monitor

PathPilot AI evaluates whether a learner's overall path is:

🟢 **Healthy**

🟠 **At Risk**

🔴 **Critical**

The score considers factors such as:

* Current readiness
* Missing critical prerequisites
* Unrealistic timelines
* Difficulty mismatches

---

### ⚠️ Learning Risk Detection

The system detects potential problems before they become blockers.

Examples include:

* Missing critical prerequisites
* Unrealistic learning timelines
* Skills significantly above the learner's current experience level

---

### 🗺️ Personalized Learning Roadmap

PathPilot AI generates a prerequisite-aware roadmap that organizes skills in a logical learning sequence.

Each roadmap step includes:

* Skill
* Priority
* Difficulty
* Prerequisites
* Recommended learning resources
* Progress tracking

---

### 🔄 Adaptive Learning Feedback

Learners can provide feedback on recommendations:

* 👍 Too Easy
* 👌 Appropriate
* 😵 Too Difficult

The adaptive engine uses this feedback to adjust the learning path.

---

### 🤖 AI Explanation Layer

PathPilot AI includes an optional AI assistant powered by Groq.

Important design principle:

> **The AI explains decisions—it does not invent them.**

The deterministic intelligence engine remains the source of truth.

If an API key isn't available, PathPilot AI falls back to deterministic explanations.

---

## 🏗️ Architecture

```text
                ┌─────────────────────┐
                │   Streamlit UI      │
                │     PathPilot AI    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Learner Profiler   │
                │  Profile Creation   │
                └──────────┬──────────┘
                           │
                           ▼
        ┌─────────────────────────────────┐
        │     Intelligence Engine         │
        │                                 │
        │ • Skill Gap Analysis            │
        │ • Readiness Score               │
        │ • Prerequisite Validation       │
        │ • Next Best Action              │
        │ • Risk Detection                │
        │ • Path Health                   │
        │ • Roadmap Generation            │
        └──────────────┬──────────────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Adaptive Engine  │
              │ Feedback System  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ AI Explanation   │
              │ Layer (Groq)     │
              └──────────────────┘
```

---

## 🛠️ Tech Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| **Python**        | Core application logic          |
| **Streamlit**     | Interactive web application     |
| **Groq API**      | Optional AI explanations        |
| **Llama 3.3 70B** | Language model for explanations |
| **Plotly**        | Data visualization              |
| **JSON**          | Career and skill knowledge data |
| **CSV**           | Learning resource data          |

---

## 📁 Project Structure

```text
PathPilot-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── profiler.py
│   ├── intelligence_engine.py
│   ├── adaptive_engine.py
│   └── ai_assistant.py
│
├── data/
│   ├── career_paths.json
│   ├── skill_graph.json
│   └── learning_resources.csv
│
├── ui/
│   ├── __init__.py
│   ├── dashboard.py
│   └── roadmap.py
│
└── test_engine.py
```

---

## 🚀 Running Locally

Clone the repository:

```bash
git clone https://github.com/bakshayareddy27-cyber/PathPilot-AI.git
```

Move into the project:

```bash
cd PathPilot-AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 🔑 Environment Variables

Groq integration is optional.

Create a `.env` file or configure the environment variable:

```text
GROQ_API_KEY=your_api_key_here
```

⚠️ Never commit API keys to GitHub.

---

## 🎯 Design Philosophy

PathPilot AI follows a hybrid architecture:

### Deterministic Intelligence

Used for:

* Recommendations
* Skill scoring
* Prerequisite reasoning
* Risk detection
* Roadmap generation

### Generative AI

Used only for:

* Explaining recommendations
* Explaining path health
* Answering learner questions using deterministic results as ground truth

This ensures that the AI does not randomly invent learning paths or recommendations.

---

## 🔮 Future Improvements

* User authentication
* Persistent learner profiles
* Database integration
* More career paths
* Dynamic learning resource APIs
* Resume-based skill extraction
* Progress analytics
* Personalized milestone tracking

---

## 👩‍💻 Author

**Bhuma Akshaya Reddy**

B.Tech — Artificial Intelligence & Machine Learning

---

### 🌟 Final verdict: YES, ADD THIS.

But one thing, bro: **don't manually type this into GitHub's README editor right now.**

Since you already have the project locally, replace the contents of your existing:

```text
README.md
```

with the polished README, then run:

```bash
git add README.md
git commit -m "Add detailed project documentation"
git push
```
