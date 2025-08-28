#!/usr/bin/env python3
"""
Demo script for AI Research Assistant Agent
Shows various usage patterns and capabilities
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def show_demo():
    console.print(Panel.fit("🤖 AI Research Assistant Agent - Demo", style="bold blue"))
    
    console.print("\n📚 Available Commands:\n")
    
    examples = [
        {
            "title": "Basic Search",
            "cmd": "python main.py --query 'transformer attention mechanisms' --max-results 5",
            "desc": "Search for recent papers on transformer attention"
        },
        {
            "title": "Date Filtered Search", 
            "cmd": "python main.py --query 'self-supervised learning' --since '2024-01-01' --max-results 10",
            "desc": "Find papers from 2024 onwards"
        },
        {
            "title": "Save Report",
            "cmd": "python main.py --query 'large language models reasoning' --out reports/llm-reasoning.md",
            "desc": "Generate and save a literature brief"
        },
        {
            "title": "Computer Vision Focus",
            "cmd": "python main.py --query 'vision transformers object detection' --max-results 8",
            "desc": "Search for ViT papers in object detection"
        }
    ]
    
    for i, ex in enumerate(examples, 1):
        console.print(f"[bold cyan]{i}. {ex['title']}[/bold cyan]")
        console.print(f"   [dim]{ex['desc']}[/dim]")
        console.print(f"   [green]{ex['cmd']}[/green]\n")
    
    console.print(Panel("💡 Tip: The system will download PDFs, extract text, and generate structured reports with summaries, critiques, and research suggestions!", style="yellow"))

if __name__ == "__main__":
    show_demo()
    
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        console.print("\n🚀 Running demo search...")
        os.system("python main.py --query 'attention mechanisms neural networks' --max-results 3")
