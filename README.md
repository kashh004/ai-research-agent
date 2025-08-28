# AI Research Assistant Agent

A production-ready AI research assistant that can find, analyze, and summarize academic papers from arXiv.

## 🎯 Features

- **Paper Discovery**: Search arXiv by topic, keywords, author, date range
- **Smart Ranking**: Combines recency with semantic relevance using BM25
- **PDF Processing**: Downloads and parses PDFs with section-aware extraction
- **Vector Search**: Builds local knowledge base using ChromaDB for semantic search
- **Critical Analysis**: Automated critique of methodology and reproducibility
- **Hypothesis Generation**: Suggests follow-up experiments and research directions
- **Report Generation**: Creates structured Markdown literature briefs

## 🚀 Quick Start

### Installation

```bash
cd ai-research-agent
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Basic Usage

```bash
# Search for papers on vision transformers
python main.py --query "vision transformers self-supervised" --max-results 5

# Search with date filter and save to file
python main.py \
  --query "large language models reasoning" \
  --max-results 10 \
  --since "2024-01-01" \
  --out reports/llm-reasoning-2024.md
```

## 📁 Project Structure

```
ai-research-agent/
├── agents/           # Core agent classes
├── tools/           # Utility modules
├── memory/          # Vector database storage
├── reports/         # Generated literature briefs
├── data/           # PDFs and cache
└── main.py         # CLI entry point
```

## 🔧 Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

## 📊 Example Output

The system generates structured reports with:
- Paper summaries and metadata
- Critical analysis notes
- Suggested follow-up experiments
- Links to downloaded PDFs

## 🛠️ Architecture

The system uses a multi-agent architecture:
- **Hunter**: Searches and ranks papers
- **Reader**: Downloads and processes PDFs
- **Critic**: Analyzes methodology and limitations
- **Hypothesis Generator**: Suggests research directions
- **Orchestrator**: Coordinates the workflow

## 📈 Future Enhancements

- Web UI interface
- Integration with Semantic Scholar API
- LLM-powered summaries
- Export to Notion/BibTeX
- Multi-agent planning loops
