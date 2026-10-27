/**
 * Vertex AI Co-Pilot & UI Mutator Frontend Engine
 * Infosys SP & DSE 37-Day Web-Lab Engine
 * 
 * Injects:
 * 1. Slide-out Vertex AI Architect Drawer
 * 2. "[⚡ Ask AI / Redesign This Section]" buttons on all modules
 * 3. 4-Option Permission Prompt before applying mutations
 * 4. 1-Click Offline Judge Runner terminal modal
 * 5. Configuration modal for GCP / Gemini API key
 */

(function() {
  // Determine current day from URL or document
  const pathParts = window.location.pathname.split('/');
  let currentDay = "01";
  for (const part of pathParts) {
    const match = part.match(/day_(\d+)/i);
    if (match) {
      currentDay = match[1];
      break;
    }
  }

  let activeModuleId = "general";
  let lastGeneratedPatch = null;
  let lastGeneratedTitle = "";

  // Inject Styles for Copilot Drawer
  const styleEl = document.createElement('style');
  styleEl.innerHTML = `
    #vertex-drawer-overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
      z-index: 9998; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
    }
    #vertex-drawer-overlay.active { opacity: 1; pointer-events: auto; }
    #vertex-drawer {
      position: fixed; top: 0; right: -500px; width: 100%; max-width: 480px; height: 100vh;
      background: #0d111c; border-left: 1px solid #1f293d; z-index: 9999;
      box-shadow: -10px 0 30px rgba(0,0,0,0.8); transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex; flex-direction: column;
    }
    #vertex-drawer.active { right: 0; }
    .ai-btn-pulse {
      animation: aiPulse 2s infinite;
    }
    @keyframes aiPulse {
      0% { box-shadow: 0 0 0 0 rgba(6, 182, 212, 0.5); }
      70% { box-shadow: 0 0 0 10px rgba(6, 182, 212, 0); }
      100% { box-shadow: 0 0 0 0 rgba(6, 182, 212, 0); }
    }
  `;
  document.head.appendChild(styleEl);

  // Inject Drawer HTML
  const drawerContainer = document.createElement('div');
  drawerContainer.innerHTML = `
    <!-- OVERLAY -->
    <div id="vertex-drawer-overlay"></div>

    <!-- FLOATING LAUNCHER -->
    <div class="fixed bottom-6 right-6 z-50 flex items-center gap-2">
      <button id="btn-run-judge-float" class="flex items-center gap-1.5 px-3.5 py-2.5 rounded-full bg-dark-900 border border-emerald-500/40 text-emerald-400 font-mono text-xs font-semibold shadow-lg hover:bg-emerald-500/10 transition-all">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        Run Judge
      </button>
      <button id="btn-open-copilot" class="flex items-center gap-2 px-4 py-2.5 rounded-full bg-gradient-to-r from-accent-cyan via-accent-violet to-accent-emerald text-white font-display font-bold text-xs shadow-xl ai-btn-pulse hover:opacity-95 transition-all">
        <span>⚡ AI Co-Pilot</span>
      </button>
    </div>

    <!-- SLIDE-OUT DRAWER -->
    <div id="vertex-drawer" class="text-slate-200">
      <!-- HEADER -->
      <div class="p-4 border-b border-dark-700 bg-dark-950 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-cyan-400 animate-pulse"></span>
          <div>
            <h2 class="font-display font-bold text-sm text-white">Vertex AI Architect Co-Pilot</h2>
            <p class="text-[11px] text-slate-400">Self-Mutating Web-Lab Engine (Day ${currentDay})</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button id="btn-open-settings" title="API Configuration" class="p-1.5 rounded-lg bg-dark-850 hover:bg-dark-800 text-slate-400 hover:text-white border border-dark-700 text-xs">⚙️</button>
          <button id="btn-close-drawer" class="p-1.5 rounded-lg bg-dark-850 hover:bg-dark-800 text-slate-400 hover:text-white border border-dark-700 text-xs">✕</button>
        </div>
      </div>

      <!-- CONTROLS & MODEL SELECTOR -->
      <div class="p-3 bg-dark-900 border-b border-dark-700 flex items-center justify-between text-xs">
        <div class="flex items-center gap-1.5">
          <span class="text-slate-400">Model:</span>
          <select id="select-model" class="bg-dark-950 text-cyan-300 border border-dark-700 rounded px-2 py-1 font-mono text-xs focus:outline-none focus:border-cyan-500">
            <option value="gemini-4-argon">gemini-4-argon (Frontier)</option>
            <option value="gemini-3.8-flash">gemini-3.8-flash (Thinking)</option>
            <option value="gemini-3.1-pro-preview">gemini-3.1-pro-preview</option>
          </select>
        </div>
        <div id="connection-status" class="flex items-center gap-1 text-[11px] font-mono text-emerald-400">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
          <span>Online</span>
        </div>
      </div>

      <!-- ACTIVE CONTEXT BAR -->
      <div class="px-4 py-2 bg-dark-950/70 border-b border-dark-800 flex items-center justify-between text-[11px]">
        <div class="flex items-center gap-1.5 text-slate-400">
          <span>Target Context:</span>
          <span id="current-target-module" class="font-mono text-amber-400 font-semibold">General Context</span>
        </div>
        <button id="btn-undo-mutation" class="hidden text-xs text-rose-400 hover:underline">↺ Undo Redesign</button>
      </div>

      <!-- BODY CONTENT -->
      <div id="drawer-body" class="flex-1 overflow-y-auto p-4 space-y-4">
        <!-- Quick Starter Chips -->
        <div>
          <p class="text-[11px] uppercase tracking-wider text-slate-400 mb-2 font-semibold">Quick Actions</p>
          <div class="flex flex-wrap gap-1.5">
            <button class="quick-chip text-xs px-2.5 py-1 rounded-full bg-dark-850 hover:bg-dark-800 text-slate-300 border border-dark-700 transition-all">
              🎨 Make a visual pointer simulator
            </button>
            <button class="quick-chip text-xs px-2.5 py-1 rounded-full bg-dark-850 hover:bg-dark-800 text-slate-300 border border-dark-700 transition-all">
              ⚠️ Why does my code TLE on N=10^5?
            </button>
            <button class="quick-chip text-xs px-2.5 py-1 rounded-full bg-dark-850 hover:bg-dark-800 text-slate-300 border border-dark-700 transition-all">
              🧠 Explain in 10-Min Beginner Cushion
            </button>
            <button class="quick-chip text-xs px-2.5 py-1 rounded-full bg-dark-850 hover:bg-dark-800 text-slate-300 border border-dark-700 transition-all">
              🗡️ Strip the Infosys Story Fluff
            </button>
          </div>
        </div>

        <!-- Doubt / Request Input -->
        <div class="space-y-2">
          <label class="text-xs text-slate-300 font-semibold block">Ask Doubt or Describe Desired Visual Redesign:</label>
          <textarea id="ai-user-doubt" rows="3" class="w-full bg-dark-950 border border-dark-700 rounded-xl p-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 font-sans" placeholder="e.g., I don't understand how the sliding window left pointer contracts. Build me an interactive visual table to step through..."></textarea>
          <button id="btn-submit-doubt" class="w-full py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-dark-950 font-bold text-xs flex items-center justify-center gap-2 transition-all">
            <span>⚡ Send to Vertex AI Architect</span>
          </button>
        </div>

        <!-- RESPONSE CONTAINER -->
        <div id="ai-response-area" class="hidden space-y-4 pt-2 border-t border-dark-800">
          <div class="flex items-center justify-between text-xs text-slate-400">
            <span class="font-semibold text-white">Architect Solution:</span>
            <span id="response-model-tag" class="font-mono text-cyan-400 text-[10px]"></span>
          </div>

          <!-- Explanation Text -->
          <div id="ai-explanation" class="text-xs leading-relaxed text-slate-300 bg-dark-950 p-3 rounded-xl border border-dark-800 space-y-2"></div>

          <!-- Python Code (if any) -->
          <div id="ai-code-wrapper" class="hidden">
            <div class="flex items-center justify-between text-[11px] bg-dark-850 px-3 py-1.5 rounded-t-lg border-t border-x border-dark-700">
              <span class="font-mono text-emerald-400">Python 3 Solution</span>
              <button onclick="navigator.clipboard.writeText(document.getElementById('ai-python-code').innerText); alert('Code copied!')" class="text-slate-400 hover:text-white">Copy</button>
            </div>
            <pre class="bg-dark-950 p-3 rounded-b-lg border border-dark-700 overflow-x-auto text-[11px] font-mono text-cyan-300"><code id="ai-python-code"></code></pre>
          </div>

          <!-- PROPOSED MUTATION PERMISSION BOX -->
          <div id="ai-mutation-prompt" class="hidden bg-dark-950 p-4 rounded-xl border border-cyan-500/40 glow-cyan space-y-3">
            <div class="flex items-start gap-2">
              <span class="text-cyan-400 text-base">✨</span>
              <div>
                <h4 class="text-xs font-bold text-white">Interactive Visual Component Generated</h4>
                <p class="text-[11px] text-slate-300">How would you like to apply this to your Web-Lab?</p>
              </div>
            </div>

            <!-- The 4 Mandatory Permission Options (Section 6) -->
            <div class="grid grid-cols-1 gap-2 pt-1">
              <button id="btn-perm-replace" class="w-full text-left p-2.5 rounded-lg bg-dark-850 hover:bg-cyan-500 hover:text-dark-950 text-cyan-400 border border-dark-700 hover:border-cyan-400 text-xs font-semibold transition-all">
                🔄 Redesign & Replace Current Section
              </button>
              <button id="btn-perm-append" class="w-full text-left p-2.5 rounded-lg bg-dark-850 hover:bg-emerald-500 hover:text-dark-950 text-emerald-400 border border-dark-700 hover:border-emerald-400 text-xs font-semibold transition-all">
                ➕ Insert as a New Custom Section Below
              </button>
              <button id="btn-perm-page" class="w-full text-left p-2.5 rounded-lg bg-dark-850 hover:bg-violet-500 hover:text-white text-violet-400 border border-dark-700 hover:border-violet-400 text-xs font-semibold transition-all">
                🆕 Open as a Separate Mini-Lab Page
              </button>
              <button id="btn-perm-chat" class="w-full text-left p-2.5 rounded-lg bg-dark-850 hover:bg-dark-800 text-slate-300 border border-dark-700 text-xs transition-all">
                💬 Keep in Chat Only (No Website Mutation)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TERMINAL JUDGE MODAL -->
    <div id="judge-modal" class="hidden fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-dark-950 border border-dark-700 rounded-2xl w-full max-w-3xl overflow-hidden shadow-2xl flex flex-col max-h-[85vh]">
        <div class="p-4 border-b border-dark-800 bg-dark-900 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-emerald-400 animate-pulse"></span>
            <h3 class="font-mono text-sm text-white font-bold">Offline Judge Suite: day_${currentDay}_judge.py</h3>
          </div>
          <button id="btn-close-judge-modal" class="text-slate-400 hover:text-white text-xs px-2 py-1 rounded bg-dark-800">✕ Close</button>
        </div>
        <div id="judge-modal-output" class="p-4 font-mono text-xs overflow-y-auto bg-black text-emerald-300 leading-relaxed whitespace-pre-wrap flex-1">
          Running automated test cases...
        </div>
      </div>
    </div>

    <!-- SETTINGS MODAL -->
    <div id="settings-modal" class="hidden fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-dark-900 border border-dark-700 rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-4">
        <div class="flex items-center justify-between border-b border-dark-800 pb-3">
          <h3 class="font-display text-sm font-bold text-white flex items-center gap-2">
            <span>⚙️ Vertex AI / Gemini API Settings</span>
          </h3>
          <button id="btn-close-settings" class="text-slate-400 hover:text-white text-xs">✕</button>
        </div>
        <div class="space-y-3 text-xs">
          <div>
            <label class="text-slate-300 font-semibold block mb-1">Gemini API Key or Vertex Express Key:</label>
            <input type="password" id="input-api-key" placeholder="AIzaSy..." class="w-full bg-dark-950 border border-dark-700 rounded-lg p-2.5 font-mono text-xs text-white focus:outline-none focus:border-cyan-500">
            <p class="text-[11px] text-slate-500 mt-1">Free tier or ₹28,000 GCP Trial billing key.</p>
          </div>
          <div>
            <label class="text-slate-300 font-semibold block mb-1">GCP Project ID (Optional):</label>
            <input type="text" id="input-gcp-project" placeholder="my-gcp-project-12345" class="w-full bg-dark-950 border border-dark-700 rounded-lg p-2.5 font-mono text-xs text-white focus:outline-none focus:border-cyan-500">
          </div>
          <button id="btn-save-settings" class="w-full py-2.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-dark-950 font-bold text-xs transition-all">
            Save Configuration
          </button>
        </div>
      </div>
    </div>
  `;
  document.body.appendChild(drawerContainer);

  // In-Dashboard Section Hook: Add "[⚡ Ask AI / Redesign This Section]" to each module
  function injectModuleRedesignButtons() {
    const modules = document.querySelectorAll('section[id^="module-"], div[id^="module-"]');
    modules.forEach(mod => {
      const header = mod.querySelector('h2, h3, .module-header');
      if (header && !mod.querySelector('.btn-redesign-hook')) {
        const btn = document.createElement('button');
        btn.className = 'btn-redesign-hook ml-3 px-2.5 py-1 rounded-lg bg-dark-850 hover:bg-cyan-500 hover:text-dark-950 text-cyan-400 border border-cyan-500/30 text-[11px] font-sans font-semibold transition-all inline-flex items-center gap-1';
        btn.innerHTML = '⚡ Ask AI / Redesign';
        btn.onclick = (e) => {
          e.stopPropagation();
          openDrawer(mod.id);
        };
        header.appendChild(btn);
      }
    });
  }

  // Event handlers
  const overlay = document.getElementById('vertex-drawer-overlay');
  const drawer = document.getElementById('vertex-drawer');
  const btnOpen = document.getElementById('btn-open-copilot');
  const btnClose = document.getElementById('btn-close-drawer');
  const targetLabel = document.getElementById('current-target-module');
  const userDoubtInput = document.getElementById('ai-user-doubt');
  const btnSubmitDoubt = document.getElementById('btn-submit-doubt');
  const responseArea = document.getElementById('ai-response-area');
  const explanationEl = document.getElementById('ai-explanation');
  const codeWrapper = document.getElementById('ai-code-wrapper');
  const codeEl = document.getElementById('ai-python-code');
  const mutationPrompt = document.getElementById('ai-mutation-prompt');
  const modelTag = document.getElementById('response-model-tag');
  const btnUndo = document.getElementById('btn-undo-mutation');

  function openDrawer(moduleId = "general") {
    activeModuleId = moduleId;
    targetLabel.innerText = moduleId === "general" ? "General Page Context" : `#${moduleId}`;
    drawer.classList.add('active');
    overlay.classList.add('active');
  }

  function closeDrawer() {
    drawer.classList.remove('active');
    overlay.classList.remove('active');
  }

  btnOpen.onclick = () => openDrawer("general");
  btnClose.onclick = closeDrawer;
  overlay.onclick = closeDrawer;

  // Quick Chips
  document.querySelectorAll('.quick-chip').forEach(chip => {
    chip.onclick = () => {
      userDoubtInput.value = chip.innerText.trim();
      btnSubmitDoubt.click();
    };
  });

  // Submit Doubt to Local Server
  btnSubmitDoubt.onclick = async () => {
    const doubt = userDoubtInput.value.trim();
    if (!doubt) return;

    btnSubmitDoubt.disabled = true;
    btnSubmitDoubt.innerHTML = `<span class="animate-spin inline-block mr-1">⌛</span> Consulting Vertex AI...`;

    let currentModuleHtml = "";
    if (activeModuleId !== "general") {
      const modEl = document.getElementById(activeModuleId);
      if (modEl) currentModuleHtml = modEl.outerHTML;
    }

    try {
      const resp = await fetch('/api/ask-doubt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          day: currentDay,
          module_id: activeModuleId,
          current_module_html: currentModuleHtml,
          user_doubt: doubt,
          model: document.getElementById('select-model').value
        })
      });

      const data = await resp.json();
      btnSubmitDoubt.disabled = false;
      btnSubmitDoubt.innerHTML = `<span>⚡ Send to Vertex AI Architect</span>`;

      if (data.unconfigured) {
        alert(data.error);
        document.getElementById('settings-modal').classList.remove('hidden');
        return;
      }
      if (data.error) {
        alert(`AI Error: ${data.error}`);
        return;
      }

      // Display response
      responseArea.classList.remove('hidden');
      modelTag.innerText = `Served by ${data.model_used || 'Vertex AI'}`;
      explanationEl.innerHTML = (data.explanation_markdown || '').replace(/\n/g, '<br>');

      if (data.python_code) {
        codeWrapper.classList.remove('hidden');
        codeEl.innerText = data.python_code;
      } else {
        codeWrapper.classList.add('hidden');
      }

      if (data.proposed_html_js_patch) {
        lastGeneratedPatch = data.proposed_html_js_patch;
        lastGeneratedTitle = doubt.slice(0, 35) + "...";
        mutationPrompt.classList.remove('hidden');
      } else {
        mutationPrompt.classList.add('hidden');
      }

    } catch (e) {
      btnSubmitDoubt.disabled = false;
      btnSubmitDoubt.innerHTML = `<span>⚡ Send to Vertex AI Architect</span>`;
      alert(`Could not connect to vertex_lab_server.py.\nMake sure the local server is running: python3 vertex_lab_server.py`);
    }
  };

  // Permission Buttons Implementation (The 4 Modes)
  async function applyMutation(mode) {
    if (!lastGeneratedPatch) return;

    if (mode === "chat_only") {
      alert("Kept in chat only. Web-lab page was not modified.");
      return;
    }

    try {
      const resp = await fetch('/api/mutate-website', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          day: currentDay,
          mode: mode,
          module_id: activeModuleId,
          patch_content: lastGeneratedPatch,
          title: lastGeneratedTitle
        })
      });

      const res = await resp.json();
      if (res.success) {
        if (mode === "create_new_page") {
          const proceed = confirm(`Created standalone page at ${res.page_url}!\nWould you like to open it now?`);
          if (proceed) window.open(res.page_url, '_blank');
        } else {
          btnUndo.classList.remove('hidden');
          alert(`Success! ${res.message}\nThe page will now reload with your new custom component.`);
          window.location.reload();
        }
      } else {
        alert(`Mutation error: ${res.error}`);
      }
    } catch(e) {
      alert("Failed to communicate with mutation engine on server.");
    }
  }

  document.getElementById('btn-perm-replace').onclick = () => applyMutation('replace_section');
  document.getElementById('btn-perm-append').onclick = () => applyMutation('append_new_section');
  document.getElementById('btn-perm-page').onclick = () => applyMutation('create_new_page');
  document.getElementById('btn-perm-chat').onclick = () => applyMutation('chat_only');

  // Undo Handler
  btnUndo.onclick = async () => {
    if (!confirm("Are you sure you want to revert to the previous snapshot?")) return;
    try {
      const resp = await fetch('/api/undo-mutation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ day: currentDay })
      });
      const res = await resp.json();
      if (res.success) {
        alert(res.message);
        window.location.reload();
      } else {
        alert(res.error);
      }
    } catch(e) {
      alert("Failed to contact undo engine.");
    }
  };

  // Run Judge In-Browser
  async function runJudgeInBrowser() {
    const modal = document.getElementById('judge-modal');
    const out = document.getElementById('judge-modal-output');
    modal.classList.remove('hidden');
    out.innerText = `⚡ Executing: python3 day_${currentDay}/day_${currentDay}_judge.py ...\n`;

    try {
      const resp = await fetch('/api/run-judge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ day: currentDay })
      });
      const data = await resp.json();
      if (data.success) {
        out.innerText = data.stdout || "Judge passed with no output.";
      } else {
        out.innerText = (data.stdout || "") + "\n" + (data.stderr || "") + `\n[Exit Code: ${data.exit_code}]`;
      }
    } catch(e) {
      out.innerText = `Error contacting local judge engine.\nPlease check if vertex_lab_server.py is running on http://localhost:8080!`;
    }
  }

  document.getElementById('btn-run-judge-float').onclick = runJudgeInBrowser;
  document.getElementById('btn-close-judge-modal').onclick = () => document.getElementById('judge-modal').classList.add('hidden');

  // Settings Modal Handlers
  const settingsModal = document.getElementById('settings-modal');
  document.getElementById('btn-open-settings').onclick = () => settingsModal.classList.remove('hidden');
  document.getElementById('btn-close-settings').onclick = () => settingsModal.classList.add('hidden');
  document.getElementById('btn-save-settings').onclick = async () => {
    const key = document.getElementById('input-api-key').value.trim();
    const gcp = document.getElementById('input-gcp-project').value.trim();
    if (!key && !gcp) {
      alert("Please enter an API Key or GCP Project ID.");
      return;
    }
    try {
      const resp = await fetch('/api/save-config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: key, gcp_project_id: gcp })
      });
      const res = await resp.json();
      if (res.success) {
        alert("Configuration saved successfully!");
        settingsModal.classList.add('hidden');
        document.getElementById('connection-status').innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span><span>Connected</span>`;
      }
    } catch(e) {
      alert("Could not save settings to local server.");
    }
  };

  // Run initial hook injection
  window.addEventListener('DOMContentLoaded', injectModuleRedesignButtons);
  // Also run immediately if DOM is already ready
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    injectModuleRedesignButtons();
  }
})();
