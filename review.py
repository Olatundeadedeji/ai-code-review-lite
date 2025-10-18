import argparse, subprocess, json, pathlib, sys, re
from analyzers.run_tools import run_flake8, run_bandit, run_radon
from analyzers.aggregate import aggregate_findings, render_markdown

def sh(cmd:list[str], cwd:str|None=None)->str:
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.stdout

def changed_files(diff_range:str)->list[str]:
    out = sh(["git","diff","--name-only", diff_range])
    return [f for f in out.splitlines() if f.endswith(".py")]

def main():
    ap = argparse.ArgumentParser(description="AI Code Review Lite")
    ap.add_argument("--range", default="HEAD~1..HEAD", help="git diff range")
    ap.add_argument("--output", default="report.md")
    ap.add_argument("--max-issues", type=int, default=50)
    ap.add_argument("--llm", action="store_true", help="(stub) include LLM hints")
    args = ap.parse_args()

    files = changed_files(args.range)
    if not files:
        print("No changed Python files in range:", args.range)
        pathlib.Path(args.output).write_text("# Code Review Report\n\n_No python changes detected._\n")
        sys.exit(0)

    f8 = run_flake8(files)
    bd = run_bandit(files)
    rd = run_radon(files)

    findings = aggregate_findings(files, f8, bd, rd, max_issues=args.max_issues)
    md = render_markdown(findings, diff_range=args.range, llm=args.llm)
    pathlib.Path(args.output).write_text(md, encoding="utf-8")
    print(f"Wrote {args.output} with {len(findings)} issues")

if __name__ == "__main__":
    main()
