import subprocess, json, re

def _run(cmd:list[str])->str:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.stdout

def run_flake8(files:list[str])->list[dict]:
    # format: filename:line:col: code message
    out = _run(["flake8", *files])
    res=[]
    for line in out.splitlines():
        m = re.match(r"(.+?):(\d+):(\d+):\s+([A-Z]\d+)\s+(.*)", line)
        if m:
            res.append({"tool":"flake8","file":m.group(1),"line":int(m.group(2)),
                        "code":m.group(4),"msg":m.group(5)})
    return res

def run_bandit(files:list[str])->list[dict]:
    out = _run(["bandit","-f","json","-q","-r", *files])
    try:
        data = json.loads(out)
    except Exception:
        return []
    res=[]
    for i in data.get("results", []):
        res.append({"tool":"bandit","file":i.get("filename"),"line":i.get("line_number"),
                    "code":i.get("test_id"),"severity":i.get("issue_severity"),
                    "msg":i.get("issue_text")})
    return res

def run_radon(files:list[str])->list[dict]:
    # radon cc -j prints JSON with complexity by block
    out = _run(["radon","cc","-j",*files])
    try:
        data = json.loads(out)
    except Exception:
        return []
    res=[]
    for f, blocks in data.items():
        for b in blocks:
            res.append({"tool":"radon","file":f,"line":b["lineno"],
                        "rank":b["rank"],"name":b["name"],"complexity":b["complexity"]})
    return res
