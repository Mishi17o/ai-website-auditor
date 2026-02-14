def basic_rule_analysis(data: dict) -> dict:
    """Simple rule-based scores – will be used later by autonomous agent."""
    scores = {"SEO": 0, "UX": 0, "Accessibility": 0, "Performance": 0, "Content": 0}

    # SEO
    if data["title"] and 10 <= len(data["title"]) <= 60: scores["SEO"] += 30
    if data["meta_description"] and 50 <= len(data["meta_description"]) <= 160: scores["SEO"] += 30
    if any(h["level"] == 1 for h in data["headings"]): scores["SEO"] += 40

    # Accessibility
    alt_empty = sum(1 for img in data["images"] if not img["alt"])
    if data["num_images"] == 0 or alt_empty == 0: scores["Accessibility"] += 60

    # Performance
    if data["load_time_seconds"] < 3: scores["Performance"] += 50
    if data["num_images"] < 15: scores["Performance"] += 30

    # normalize
    for k in scores:
        scores[k] = min(100, scores[k])

    return scores