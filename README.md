# 🌿 CarbonLens

**Carbon & cost analytics for the built environment**

CarbonLens is a web-based analytics dashboard that calculates embodied carbon and cost for construction projects. Input a bill of materials, instantly see your carbon footprint broken down by element and category, and get AI-powered recommendations for reducing it — all in one interface.

Built as a portfolio project demonstrating applied AI, data engineering, and software development skills for the built environment sector.

---

## Live Demo

> https://carbonlensicev3.streamlit.app/

---

## Features

- **Carbon calculation** — converts material quantities into kgCO₂e using ICE Database v3.0 carbon factors
- **Cost estimation** — calculates project cost per element using industry unit rates
- **Carbon/£ ratio** — identifies which elements deliver the worst carbon value for money
- **Interactive charts** — scatter, bar, donut, and carbon intensity heatmap built with Plotly
- **CSV import** — upload a full bill of materials and process it in one click, with live spinner and inline results preview
- **AI material swaps** — tell the AI to "replace steel with recycled steel" and get an instant before/after comparison table with apply/discard controls
- **AI assistant** — GPT-4o answers questions about your specific project data, referencing RIBA 2030 targets
- **23 materials** across 5 categories, all sourced from ICE Database v3.0

---

## Tech Stack

| Technology | Role |
|---|---|
| Python | Core language |
| Streamlit | Web interface |
| Pandas | Data processing and aggregation |
| Plotly | Interactive charts |
| OpenAI GPT-4o | AI assistant and swap detection |
| ICE Database v3.0 | Embodied carbon factors (University of Bath) |

---

## Project Structure

```
carbonLens/
├── app.py                  # Main Streamlit application
├── data/
│   ├── __init__.py
│   ├── materials.py        # Materials database (ICE Database v3.0)
│   └── calculator.py       # Carbon & cost calculation engine
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/amalykyarima/carbonLens.git
cd carbonLens
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

### 4. Add your OpenAI API key

Enter your OpenAI API key in the sidebar and click **Save key** to enable the AI assistant.

---

## Requirements

```
streamlit
pandas
plotly
openai
```

Create a `requirements.txt` with the above, or run:

```bash
pip freeze > requirements.txt
```

---

## Data Source

Carbon factors are sourced from the **[ICE Database v3.0](https://circularecology.com/embodied-carbon-footprint-database.html)** (Inventory of Carbon and Energy), published by the University of Bath. This is the industry standard reference for embodied carbon in the UK construction sector.

---

## Roadmap

- [ ] RIBA 2030 benchmark overlay — traffic-light compliance indicator against 350 kgCO₂e/m² office target
- [ ] PDF report export — formatted carbon assessment for planning submissions
- [ ] Scenario comparison — run two versions of a project side by side and quantify the delta
- [ ] Identity Consult data integration — extend with proprietary project benchmarks

---

## About

Built by **Abdulmalik Masud** — MSc Artificial Intelligence, Northumbria University (London campus).

This project was developed to demonstrate applied skills in AI integration, data engineering, and software development for the built environment — specifically in the context of the KTP Associate: Software & Analytics Specialist role at Identity Consult.

---

## Licence

MIT