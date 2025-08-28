TEMPL = (
    "Given the following summary, propose 2-3 concrete follow-up experiments,"
    " datasets, and evaluation protocols. Keep suggestions practical.\n\nSUMMARY:\n{summary}\n"
)

class Hypothesis:
    def propose(self, summary: str) -> list[str]:
        # Placeholder: rule-based suggestions when LLM not configured
        ideas = []
        if "transformer" in summary.lower():
            ideas.append("Ablate attention head counts and measure sample efficiency on small-data regimes.")
            ideas.append("Evaluate robustness under corruptions (ImageNet-C or equivalent).")
        if "neural network" in summary.lower() or "deep learning" in summary.lower():
            ideas.append("Test generalization across different architectures and hyperparameter settings.")
        if "dataset" in summary.lower():
            ideas.append("Validate findings on additional datasets from different domains.")
        ideas.append("Replicate main result on at least one out-of-domain dataset with strong baselines.")
        return ideas
