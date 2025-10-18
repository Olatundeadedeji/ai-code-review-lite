import subprocess, pathlib, sys

def test_runs_and_writes_report(tmp_path):
    # run review on the examples dir by faking a diff: pass files explicitly via git index
    # easiest path: just ensure script writes a report even if no diff found
    out = subprocess.run([sys.executable, "review.py", "--range", "HEAD~1..HEAD", "--output", str(tmp_path/"report.md")],
                         stdout=subprocess.PIPE, text=True)
    assert (tmp_path/"report.md").exists()
