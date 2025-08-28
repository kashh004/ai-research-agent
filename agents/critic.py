HEURISTICS = [
    ("claims_vs_evidence", "Does the paper provide quantitative evidence supporting major claims?"),
    ("data_leakage", "Any risk of data leakage or test-set overfitting?"),
    ("baselines", "Are baselines strong and fairly tuned?"),
    ("reproducibility", "Is code/data available? Enough detail to reproduce?"),
]

class Critic:
    def review(self, sections: dict) -> dict:
        notes = {}
        full = sections.get("full_text", "")
        lower = full.lower()
        notes["code_available"] = ("github" in lower) or ("code available" in lower)
        notes["dataset_named"] = ("dataset" in lower) or ("data set" in lower)
        notes["limitations_present"] = ("limitation" in lower) or ("future work" in lower)
        notes["checklist"] = {k: q for k, q in HEURISTICS}
        return notes
