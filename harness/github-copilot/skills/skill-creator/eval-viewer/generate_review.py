#!/usr/bin/env python3
"""Eval review viewer for skill-creator.

Renders an iteration workspace into a self-contained HTML review with two tabs:
"Outputs" (click through each run, leave feedback) and "Benchmark" (quantitative
comparison from benchmark.json). Works in two modes:

  * default: start a local server, open the browser, and write feedback.json to
    the workspace when the user submits.
  * --static <path>: write a standalone HTML file (feedback is downloaded by the
    browser as feedback.json; copy it back into the workspace afterward).

Stdlib only. See ../references/schemas.md for the JSON shapes consumed here.
"""

import argparse
import http.server
import json
import socketserver
import threading
import webbrowser
from pathlib import Path

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Eval Review - __SKILL__</title>
<style>
:root{color-scheme:light dark}*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;margin:0;background:#0d1117;color:#e6edf3}
header{padding:16px 24px;border-bottom:1px solid #30363d}
h1{font-size:18px;margin:0}
.tabs{display:flex;gap:8px;padding:12px 24px}
.tabs button{font:inherit;padding:8px 14px;border-radius:6px;border:1px solid #30363d;background:#21262d;color:#e6edf3;cursor:pointer}
.tabs button.active{background:#1f6feb;border-color:#1f6feb}
main{max-width:1000px;margin:0 auto;padding:0 24px 40px}
.run{border:1px solid #30363d;border-radius:8px;padding:16px;margin-bottom:14px;background:#161b22}
.run h3{margin:0 0 8px;font-size:15px}
.prompt{color:#8b949e;font-size:13px;white-space:pre-wrap;margin-bottom:10px}
pre{background:#010409;border:1px solid #30363d;border-radius:6px;padding:10px;overflow:auto;font-size:12px}
.pass{color:#3fb950}.fail{color:#f85149}
textarea{width:100%;min-height:64px;font:inherit;padding:8px;border-radius:6px;border:1px solid #30363d;background:#0d1117;color:#e6edf3;margin-top:8px}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border:1px solid #30363d;padding:8px;text-align:left}
th{background:#161b22}
.bar{display:flex;gap:8px;padding:16px 24px}
button.primary{font:inherit;padding:8px 16px;border-radius:6px;border:1px solid #2ea043;background:#238636;color:#fff;cursor:pointer}
.hidden{display:none}
</style></head>
<body>
<header><h1>Eval Review &mdash; __SKILL__</h1></header>
<div class="tabs">
  <button id="tabOutputs" class="active" onclick="show('outputs')">Outputs</button>
  <button id="tabBench" onclick="show('bench')">Benchmark</button>
</div>
<main>
  <section id="outputs"></section>
  <section id="bench" class="hidden"></section>
</main>
<div class="bar"><button class="primary" onclick="submit()">Submit All Reviews</button></div>
<script>
const DATA = __DATA__;
const STATIC = __STATIC__;
function esc(s){return (s||"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function show(t){
  document.getElementById('outputs').classList.toggle('hidden',t!=='outputs');
  document.getElementById('bench').classList.toggle('hidden',t!=='bench');
  document.getElementById('tabOutputs').classList.toggle('active',t==='outputs');
  document.getElementById('tabBench').classList.toggle('active',t==='bench');
}
function renderOutputs(){
  const el=document.getElementById('outputs');
  if(!DATA.runs.length){el.innerHTML='<p>No run directories found in this workspace.</p>';return;}
  DATA.runs.forEach((r,i)=>{
    const d=document.createElement('div');d.className='run';
    let grades='';
    if(r.expectations&&r.expectations.length){
      grades='<ul>'+r.expectations.map(e=>`<li class="${e.passed?'pass':'fail'}">${e.passed?'PASS':'FAIL'}: ${esc(e.text)} <em>${esc(e.evidence||'')}</em></li>`).join('')+'</ul>';
    }
    d.innerHTML=`<h3>${esc(r.run_id)}</h3>`+
      `<div class="prompt">${esc(r.prompt||'(no prompt found)')}</div>`+
      `<pre>${esc(r.output||'(no output captured)')}</pre>`+grades+
      `<textarea data-i="${i}" placeholder="Feedback (auto-saves)">${esc(r.feedback||'')}</textarea>`;
    el.appendChild(d);
  });
  el.addEventListener('input',e=>{if(e.target.dataset.i!==undefined)DATA.runs[e.target.dataset.i].feedback=e.target.value;});
}
function renderBench(){
  const el=document.getElementById('bench');
  if(!DATA.benchmark){el.innerHTML='<p>No benchmark.json provided.</p>';return;}
  const cfgs=DATA.benchmark.configurations||[];
  let rows=cfgs.map(c=>`<tr><td>${esc(c.name)}</td><td>${(c.pass_rate&&c.pass_rate.mean!=null)?(c.pass_rate.mean*100).toFixed(1)+'%':'-'}</td><td>${c.time_seconds&&c.time_seconds.mean!=null?c.time_seconds.mean.toFixed(1)+'s':'-'}</td><td>${c.tokens&&c.tokens.mean!=null?Math.round(c.tokens.mean):'-'}</td></tr>`).join('');
  el.innerHTML=`<table><thead><tr><th>Configuration</th><th>Pass rate</th><th>Time</th><th>Tokens</th></tr></thead><tbody>${rows}</tbody></table>`;
}
function submit(){
  const payload={reviews:DATA.runs.map(r=>({run_id:r.run_id,feedback:r.feedback||'',timestamp:new Date().toISOString()})),status:'complete'};
  if(STATIC){
    const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
    const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='feedback.json';a.click();
  }else{
    fetch('/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
      .then(()=>alert('Feedback saved. You can return to the assistant.'))
      .catch(()=>alert('Could not save feedback.'));
  }
}
renderOutputs();renderBench();
</script>
</body></html>
"""


def _read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None


def _load_prompts(workspace: Path):
    for candidate in (workspace / "evals" / "evals.json", workspace / "evals.json"):
        data = _read_json(candidate)
        if data and isinstance(data.get("evals"), list):
            return {str(e.get("id")): e.get("prompt", "") for e in data["evals"]}
    return {}


def _load_output(run_dir: Path):
    """Concatenate small text outputs found in a run directory."""
    chunks = []
    for p in sorted(run_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in {".md", ".txt", ".json", ".html", ".csv"}:
            if p.name in {"grading.json", "timing.json"}:
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                continue
            chunks.append(f"# {p.name}\n{text[:4000]}")
        if sum(len(c) for c in chunks) > 16000:
            break
    return "\n\n".join(chunks)


def _discover_runs(workspace: Path, prompts):
    runs = []
    if not workspace.is_dir():
        return runs
    for run_dir in sorted(p for p in workspace.iterdir() if p.is_dir()):
        name = run_dir.name
        if name in {"evals", "__pycache__"}:
            continue
        grading = _read_json(run_dir / "grading.json") or {}
        eval_id = "".join(ch for ch in name if ch.isdigit())
        runs.append({
            "run_id": name,
            "prompt": prompts.get(eval_id, ""),
            "output": _load_output(run_dir),
            "expectations": grading.get("expectations", []),
            "feedback": "",
        })
    return runs


def build_html(workspace: Path, skill_name: str, benchmark_path, static: bool):
    prompts = _load_prompts(workspace)
    runs = _discover_runs(workspace, prompts)
    benchmark = _read_json(benchmark_path) if benchmark_path else None
    data = {"runs": runs, "benchmark": benchmark}
    return (TEMPLATE
            .replace("__SKILL__", skill_name or workspace.name)
            .replace("__DATA__", json.dumps(data))
            .replace("__STATIC__", "true" if static else "false"))


def serve(html: str, workspace: Path, port: int):
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        def do_POST(self):
            if self.path == "/feedback":
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)
                (workspace / "feedback.json").write_bytes(body)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"ok")
            else:
                self.send_response(404)
                self.end_headers()

    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        url = f"http://127.0.0.1:{port}/"
        print(f"Eval viewer running at {url} (Ctrl+C to stop)")
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping viewer.")


def main():
    ap = argparse.ArgumentParser(description="Render an eval iteration workspace into an HTML review.")
    ap.add_argument("workspace", help="Path to the iteration-N workspace directory")
    ap.add_argument("--skill-name", default="", help="Skill name for the header")
    ap.add_argument("--benchmark", default=None, help="Path to benchmark.json")
    ap.add_argument("--previous-workspace", default=None, help="Previous iteration (reserved for diffing)")
    ap.add_argument("--static", default=None, help="Write a standalone HTML file to this path instead of serving")
    ap.add_argument("--port", type=int, default=8729, help="Server port (default 8729)")
    args = ap.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    html = build_html(workspace, args.skill_name, args.benchmark, static=bool(args.static))

    if args.static:
        out = Path(args.static).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print(f"Wrote static review to {out}")
    else:
        serve(html, workspace, args.port)


if __name__ == "__main__":
    main()
