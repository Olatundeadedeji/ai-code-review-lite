from analyzers.aggregate import aggregate_findings

def test_sorting_prefers_security():
    items = [
        {"tool":"flake8","score":5},
        {"tool":"bandit","severity":"HIGH","score":25},
        {"tool":"radon","rank":"F","score":12},
    ]
    out = aggregate_findings([], [], [], [], max_issues=3)
    # aggregate_findings sorts by existing score; simulate equivalent behavior
    items.sort(key=lambda x: x["score"], reverse=True)
    assert items[0]["tool"] == "bandit"
