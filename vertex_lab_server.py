#!/usr/bin/env python3
"""
Vertex AI "Self-Mutating Web-Lab" Bridge Server
Infosys SP & DSE 37-Day Tactical Web-Lab Engine

Zero-dependency Python 3 HTTP & API server.
Fulfills Section 6 specifications:
1. Static web server on http://localhost:8080
2. POST /api/ask-doubt (Model router: gemini-4-argon -> gemini-3.8-flash -> gemini-2.5/1.5 fallback)
3. POST /api/mutate-website (replace_section, append_new_section, create_new_page with .bak backup)
4. POST /api/undo-mutation (1-click snapshot restore)
5. POST /api/run-judge (in-browser offline test execution)
6. GET /api/status & POST /api/save-config
"""

import os
import sys
import json
import time
import re
import shutil
import subprocess
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

PORT = 8080
BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"

# Default Model Routing Fallback Chain
MODEL_ALIASES = {
    "gemini-4-argon": ["gemini-2.5-pro", "gemini-1.5-pro", "gemini-2.5-flash"],
    "gemini-3.8-flash": ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.5-pro"],
    "gemini-3.1-pro-preview": ["gemini-2.5-pro", "gemini-1.5-pro"],
}

def load_config():
    cfg = {
        "api_key": os.environ.get("GEMINI_API_KEY", os.environ.get("VERTEX_API_KEY", "")),
        "gcp_project_id": os.environ.get("GCP_PROJECT_ID", ""),
        "preferred_model": "gemini-4-argon"
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                cfg.update(saved)
        except Exception:
            pass
    return cfg

def save_config(new_cfg):
    cfg = load_config()
    cfg.update(new_cfg)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    return cfg

def call_gemini_api(prompt: str, model_choice: str = "gemini-4-argon"):
    cfg = load_config()
    api_key = cfg.get("api_key", "").strip()
    
    if not api_key:
        return {
            "error": "API Key not configured. Please paste your Gemini API Key or GCP Vertex Key in the settings drawer.",
            "unconfigured": True
        }

    # Determine candidate model names
    candidates = [model_choice]
    if model_choice in MODEL_ALIASES:
        candidates.extend(MODEL_ALIASES[model_choice])
    else:
        candidates.extend(["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"])

    # Deduplicate while preserving order
    seen = set()
    models_to_try = []
    for m in candidates:
        if m not in seen:
            seen.add(m)
            models_to_try.append(m)

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 4096,
            "responseMimeType": "application/json"
        }
    }
    data = json.dumps(payload).encode("utf-8")

    last_error = None
    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                candidates_out = resp_data.get("candidates", [])
                if candidates_out:
                    parts = candidates_out[0].get("content", {}).get("parts", [])
                    if parts:
                        text = parts[0].get("text", "")
                        try:
                            parsed_json = json.loads(text)
                            parsed_json["model_used"] = model_name
                            return parsed_json
                        except json.JSONDecodeError:
                            return {
                                "explanation_markdown": text,
                                "python_code": "",
                                "proposed_html_js_patch": "",
                                "model_used": model_name
                            }
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            last_error = f"HTTP {e.code} on {model_name}: {err_body}"
            # Fallback to next model
            continue
        except Exception as e:
            last_error = f"Exception on {model_name}: {str(e)}"
            continue

    return {
        "error": f"All model fallbacks failed. Last error: {last_error}"
    }

class VertexLabHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def _send_json(self, status_code, data):
        response_body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/status":
            cfg = load_config()
            self._send_json(200, {
                "status": "online",
                "configured": bool(cfg.get("api_key")),
                "preferred_model": cfg.get("preferred_model", "gemini-4-argon"),
                "available_models": list(MODEL_ALIASES.keys()) + ["gemini-2.5-flash", "gemini-1.5-flash"]
            })
            return
        
        # Default static file server
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            req_data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON request body"})
            return

        if self.path == "/api/save-config":
            saved = save_config(req_data)
            self._send_json(200, {"success": True, "config": {"configured": bool(saved.get("api_key"))}})
            return

        elif self.path == "/api/ask-doubt":
            day = str(req_data.get("day", "01")).zfill(2)
            module_id = req_data.get("module_id", "general")
            current_html = req_data.get("current_module_html", "")[:2000]
            user_doubt = req_data.get("user_doubt", "")
            user_code = req_data.get("user_code", "")
            model_choice = req_data.get("model", "gemini-4-argon")

            system_prompt = f"""You are the Vertex AI Architect Co-Pilot for the Infosys SP & DSE 37-Day Web-Lab Engine.
Target Student Context:
- Aiming for Infosys Specialist Programmer (SP 200+ marks) and Digital Specialist Engineer (DSE 150 marks).
- Learning in Python 3.
- Wants visual intuition, zero dry theory, and the 3-Gear Escalator (Gear 1 Brute Force -> Gear 2 TLE X-Ray -> Gear 3 Optimal).

Current Context:
Day: Day {day}
Module ID: {module_id}
User Doubt: "{user_doubt}"
User Code (if any):
```python
{user_code}
```
Target Section HTML Context:
```html
{current_html}
```

Instructions:
1. Explain the doubt clearly using concrete mental models (e.g. memory boxes, number lines, array pointers).
2. If relevant, provide clean, optimal Python code with beginner-friendly comments.
3. Propose a self-contained, working HTML+JS visual interactive card or patch that can be rendered directly into the web-lab. Use dark mode Tailwind CSS styling (bg-dark-900, border-dark-700, cyan/emerald neon accents, buttons with onclick handlers).
4. Return ONLY a valid JSON object with the following schema:
{{
  "explanation_markdown": "Markdown explanation with formatting and bullet points",
  "python_code": "Python code snippet",
  "proposed_html_js_patch": "<div class='glass-panel p-4 rounded-xl ...'>Interactive visual card HTML + JS</div>"
}}
"""
            result = call_gemini_api(system_prompt, model_choice)
            self._send_json(200, result)
            return

        elif self.path == "/api/mutate-website":
            day = str(req_data.get("day", "01")).zfill(2)
            mode = req_data.get("mode", "append_new_section")
            module_id = req_data.get("module_id", "module-2")
            patch_content = req_data.get("patch_content", "")
            title = req_data.get("title", f"AI Custom Enhancement ({module_id})")

            dashboard_path = BASE_DIR / f"day_{day}" / f"day_{day}_dashboard.html"
            if not dashboard_path.exists():
                self._send_json(404, {"error": f"Dashboard file not found: {dashboard_path}"})
                return

            backup_path = dashboard_path.with_suffix(".html.bak")
            # Always save a backup before mutation
            shutil.copyfile(dashboard_path, backup_path)

            try:
                original_html = dashboard_path.read_text(encoding="utf-8")

                if mode == "replace_section":
                    # Replace <section id="module_id" ...> ... </section> or <div id="module_id" ...> ... </div>
                    pattern = rf'(<(?:section|div)[^>]*id=["\']{re.escape(module_id)}["\'][^>]*>)(.*?)(</(?:section|div)>)'
                    match = re.search(pattern, original_html, re.DOTALL)
                    if match:
                        new_html = (
                            original_html[:match.start(2)] +
                            f"\n<!-- AI MUTATION: Replaced {module_id} on {time.ctime()} -->\n" +
                            patch_content + "\n" +
                            original_html[match.end(2):]
                        )
                        dashboard_path.write_text(new_html, encoding="utf-8")
                        self._send_json(200, {
                            "success": True,
                            "mode": "replace_section",
                            "message": f"Successfully replaced {module_id} on disk.",
                            "backup": str(backup_path.name)
                        })
                        return
                    else:
                        self._send_json(400, {"error": f"Target section #{module_id} not found in HTML."})
                        return

                elif mode == "append_new_section":
                    # Find closing tag of target section and append
                    pattern = rf'(<(?:section|div)[^>]*id=["\']{re.escape(module_id)}["\'][^>]*>.*?</(?:section|div)>)'
                    match = re.search(pattern, original_html, re.DOTALL)
                    insert_html = f"""
<!-- AI MUTATION: Appended below {module_id} -->
<section id="ai-custom-{int(time.time())}" class="glass-panel rounded-2xl p-6 my-6 border border-cyan-500/30 glow-cyan">
  <div class="flex items-center justify-between mb-4 pb-3 border-b border-dark-700">
    <div class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-cyan-400 animate-pulse"></span>
      <h3 class="font-display font-bold text-base text-cyan-300">⚡ AI Custom Lab: {title}</h3>
    </div>
    <span class="text-xs font-mono text-slate-400">{time.strftime('%H:%M:%S')}</span>
  </div>
  {patch_content}
</section>
"""
                    if match:
                        pos = match.end(1)
                        new_html = original_html[:pos] + insert_html + original_html[pos:]
                    else:
                        # Append before closing </main> or </body>
                        pos = original_html.rfind("</main>")
                        if pos == -1:
                            pos = original_html.rfind("</body>")
                        new_html = original_html[:pos] + insert_html + original_html[pos:]

                    dashboard_path.write_text(new_html, encoding="utf-8")
                    self._send_json(200, {
                        "success": True,
                        "mode": "append_new_section",
                        "message": f"Successfully injected custom AI section below #{module_id}.",
                        "backup": str(backup_path.name)
                    })
                    return

                elif mode == "create_new_page":
                    timestamp = int(time.time())
                    new_file = BASE_DIR / f"day_{day}" / f"day_{day}_doubt_{timestamp}.html"
                    page_html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Day {day} Sub-Lab: {title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code&family=Inter:wght@400;600;800&family=Outfit:wght@600;800&display=swap" rel="stylesheet">
  <style>
    body {{ background: #07090e; color: #e2e8f0; font-family: 'Inter', sans-serif; }}
    .glass-panel {{ background: rgba(17, 23, 38, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); backdrop-filter: blur(12px); }}
  </style>
</head>
<body class="p-6 max-w-5xl mx-auto min-h-screen">
  <div class="flex items-center justify-between mb-8 pb-4 border-b border-slate-800">
    <div>
      <a href="day_{day}_dashboard.html" class="text-xs text-cyan-400 hover:underline">← Back to Day {day} Dashboard</a>
      <h1 class="text-2xl font-bold font-display text-white mt-1">⚡ Custom Sub-Lab: {title}</h1>
    </div>
    <span class="text-xs font-mono text-slate-400">{time.strftime('%Y-%m-%d %H:%M')}</span>
  </div>
  <div class="glass-panel p-6 rounded-2xl">
    {patch_content}
  </div>
</body>
</html>"""
                    new_file.write_text(page_html, encoding="utf-8")
                    self._send_json(200, {
                        "success": True,
                        "mode": "create_new_page",
                        "page_url": f"/day_{day}/{new_file.name}",
                        "message": f"Created standalone sub-lab at {new_file.name}"
                    })
                    return

            except Exception as e:
                self._send_json(500, {"error": f"Failed to mutate website: {str(e)}"})
                return

        elif self.path == "/api/undo-mutation":
            day = str(req_data.get("day", "01")).zfill(2)
            dashboard_path = BASE_DIR / f"day_{day}" / f"day_{day}_dashboard.html"
            backup_path = dashboard_path.with_suffix(".html.bak")
            if not backup_path.exists():
                self._send_json(404, {"error": f"No backup snapshot found for Day {day}."})
                return
            shutil.copyfile(backup_path, dashboard_path)
            self._send_json(200, {"success": True, "message": f"Restored Day {day} dashboard from {backup_path.name}."})
            return

        elif self.path == "/api/run-judge":
            day = str(req_data.get("day", "01")).zfill(2)
            judge_path = BASE_DIR / f"day_{day}" / f"day_{day}_judge.py"
            if not judge_path.exists():
                self._send_json(404, {"error": f"Offline judge not found at: {judge_path}"})
                return
            
            try:
                proc = subprocess.run(
                    [sys.executable, str(judge_path)],
                    capture_output=True,
                    text=True,
                    timeout=15,
                    cwd=str(judge_path.parent)
                )
                self._send_json(200, {
                    "success": True,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                    "exit_code": proc.returncode,
                    "passed": (proc.returncode == 0)
                })
            except subprocess.TimeoutExpired:
                self._send_json(200, {
                    "success": False,
                    "stdout": "Judge execution timed out after 15 seconds.",
                    "stderr": "TimeoutExpired",
                    "exit_code": 124,
                    "passed": False
                })
            except Exception as e:
                self._send_json(500, {"error": f"Failed to execute judge: {str(e)}"})
            return

        else:
            self._send_json(404, {"error": "API route not found"})

def run_server():
    server_address = ("", PORT)
    HTTPServer.allow_reuse_address = True
    httpd = HTTPServer(server_address, VertexLabHandler)
    print(f"\n========================================================")
    print(f"🚀 Vertex AI Self-Mutating Web-Lab Server Active!")
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"🎯 Status: Serving Web-Labs & Vertex AI Co-Pilot API")
    print(f"🛑 Press Ctrl+C to terminate server")
    print(f"========================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server stopped]")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
