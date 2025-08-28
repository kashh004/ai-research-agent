import argparse
from rich import print
from config import settings
from agents.orchestrator import Orchestrator
import os, json

parser = argparse.ArgumentParser()
parser.add_argument('--query', required=True)
parser.add_argument('--max-results', type=int, default=10)
parser.add_argument('--since', type=str, default=None)
parser.add_argument('--out', type=str, default=None)
args = parser.parse_args()

os.makedirs('reports', exist_ok=True)

orch = Orchestrator(settings.chroma_dir, settings.embedding_model)
results = orch.run(args.query, args.max_results, args.since)

md = [f"# Literature Brief — {args.query}\n"]
for r in results:
    if 'error' in r:
        md.append(f"\n## {r['title']}\n- ERROR: {r['error']}\n")
        continue
    md.append(f"\n## {r['title']}\n")
    md.append(f"**Authors:** {', '.join(r['authors'])}  ")
    md.append(f"**Published:** {r['published']}  ")
    md.append(f"**PDF:** {r['pdf_path']}  ")
    md.append(f"\n**Summary:**\n{r['summary']}\n")
    md.append("\n**Critique Notes:**")
    for k, v in r['review'].items():
        if k == 'checklist':
            md.append("\n- Heuristic checklist:")
            for ck, q in v.items():
                md.append(f"  - {ck}: {q}")
        else:
            md.append(f"- {k}: {v}")
    md.append("\n**Follow-up Ideas:**")
    for idea in r['ideas']:
        md.append(f"- {idea}")

report = "\n".join(md)

if args.out:
    with open(args.out, 'w') as f:
        f.write(report)
    print({"saved": args.out, "papers": len(results)})
else:
    print(report)
