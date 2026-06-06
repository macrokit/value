/* app.js — boot Pyodide, load the REAL value_meter.py, run profiles in-browser.
 * No server, no upload: records are parsed and measured entirely client-side. */

const $ = (id) => document.getElementById(id);
const statusEl = $("status"), runBtn = $("run"), errEl = $("err"),
      inputEl = $("input"), noteEl = $("note"), resultEl = $("result");

let pyodide = null;
let driverReady = false;

function setStatus(msg, cls = "") {
  statusEl.textContent = msg;
  statusEl.className = "status" + (cls ? " " + cls : "");
}

// The tiny Python driver: parse records JSON -> value_profile -> JSON out.
// It calls the unmodified value_meter core (single source of truth).
const DRIVER = `
import json
import value_meter as vm

def run_profile(json_str, split):
    obj = json.loads(json_str)
    if isinstance(obj, dict) and "records" in obj:
        rows = obj["records"]; classes = obj.get("classes")
    elif isinstance(obj, list):
        rows = obj; classes = None
    else:
        raise ValueError("Expected a {\\"records\\": [...]} object or a bare list of records.")
    if not rows:
        raise ValueError("No records found.")
    prof = vm.value_profile(rows, classes=classes, split=float(split))
    return json.dumps({"profile": prof.to_dict(), "text": vm.format_profile(prof)})
`;

async function boot() {
  try {
    setStatus("loading Python runtime…");
    pyodide = await loadPyodide();
    setStatus("loading numpy…");
    await pyodide.loadPackage("numpy");
    setStatus("loading the value-meter…");
    // fetch the REAL source and mount it where Python can import it
    const [vsim, vmeter] = await Promise.all([
      fetch("py/value_sim.py").then((r) => r.text()),
      fetch("py/value_meter.py").then((r) => r.text()),
    ]);
    pyodide.FS.mkdirTree("/lib");
    pyodide.FS.writeFile("/lib/value_sim.py", vsim);
    pyodide.FS.writeFile("/lib/value_meter.py", vmeter);
    await pyodide.runPythonAsync("import sys; sys.path.insert(0, '/lib')");
    await pyodide.runPythonAsync(DRIVER);
    driverReady = true;
    setStatus("ready · runs in your browser", "ready");
    runBtn.disabled = false;
  } catch (e) {
    console.error(e);
    setStatus("failed to load runtime", "err");
    errEl.textContent = String(e);
  }
}

async function measure() {
  errEl.textContent = "";
  if (!driverReady) return;
  let raw = inputEl.value.trim();
  if (!raw) { errEl.textContent = "Paste some records JSON first (or load an example)."; return; }
  // client-side JSON sanity check for a friendly error
  try { JSON.parse(raw); }
  catch (e) { errEl.textContent = "Invalid JSON: " + e.message; return; }

  runBtn.disabled = true;
  const prevStatus = statusEl.textContent;
  setStatus("measuring…");
  try {
    const split = parseFloat($("split").value) || 0.5;
    const fn = pyodide.globals.get("run_profile");
    const out = fn(raw, split);
    fn.destroy();
    const { profile, text } = JSON.parse(out);
    render(profile, text);
    resultEl.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (e) {
    console.error(e);
    errEl.textContent = "Could not compute: " + (e.message || e).toString().split("\n").slice(-2).join(" ");
  } finally {
    runBtn.disabled = false;
    setStatus(prevStatus, "ready");
  }
}

const f = (x, d = 4) => (x === null || x === undefined || Number.isNaN(x)) ? "n/a" : Number(x).toFixed(d);

function render(p, text) {
  const sat = Math.max(0, Math.min(1, p.saturation || 0));
  const chancePill = p.I_above_chance
    ? `<span class="pill ok">above chance</span>`
    : `<span class="pill chance">≈ null — not above chance</span>`;
  const [lo, hi] = p.dG_oos_ci_nats;
  const degradedWarn = p.degraded_rate > 0.5
    ? `<div class="row" style="color:var(--chance)">⚠ ${(p.degraded_rate*100).toFixed(0)}% unparseable preds — likely plumbing failure, not capability</div>` : "";

  const vpc_tok = p.I_per_1k_tokens === null ? "n/a"
    : `${f(p.I_per_1k_tokens)} <span class="unit">nats / 1k tok</span>`;
  const vpc_lat = p.I_per_sec_median_latency === null ? "n/a"
    : `${f(p.I_per_sec_median_latency)} <span class="unit">nats / s</span>`;

  resultEl.innerHTML = `
    <h2>Value profile</h2>
    <p class="rsub">n=${p.n} items · K=${p.n_classes} classes · H(X)=${f(p.H_X_nats,3)} nats
       (${f(p.H_X_nats/Math.log(2),3)} bits)</p>
    ${degradedWarn}
    <div class="cards">
      <div class="card">
        <h3>1 · Value ceiling I(X;Y)</h3>
        <div class="metric"><span class="big">${f(p.I_nats)}</span><span class="unit">nats
          (${f(p.I_bits)} bits)</span>${chancePill}</div>
        <div class="row"><span class="lab">permutation null:</span> mean ${f(p.I_null_mean_nats)},
          p95 ${f(p.I_null_p95_nats)} · perm p=${(p.I_perm_p_value).toPrecision(2)}</div>
        <div class="row"><span class="lab">saturation I/H(X):</span> ${f(sat,3)}</div>
        <div class="bar"><span style="width:${(sat*100).toFixed(1)}%"></span></div>
        <div class="tag-line">→ 1.0 means more compute can't add value on this task</div>
      </div>

      <div class="card">
        <h3>2 · Realized rate ΔG</h3>
        <div class="metric"><span class="big">${f(p.dG_out_of_sample_nats)}</span>
          <span class="unit">nats · out-of-sample</span></div>
        <div class="row"><span class="lab">95% CI:</span> [${f(lo)}, ${f(hi)}] ·
          ${p.n_holdout} holdout items, ${(p.split_frac*100).toFixed(0)}% fit</div>
        <div class="row"><span class="lab">in-sample:</span> ${f(p.dG_in_sample_nats)}
          <span class="pill def">= I · definitional</span></div>
        <div class="tag-line">the out-of-sample number is the empirical one; in-sample = I is an identity</div>
      </div>

      <div class="card">
        <h3>3 · Dissipation D(q‖p)</h3>
        <div class="metric"><span class="big">${f(p.dissipation_nats)}</span><span class="unit">nats lost</span></div>
        <div class="row"><span class="lab">belief:</span> ${p.dissipation_belief}</div>
        <div class="tag-line">${p.dissipation_note}</div>
      </div>

      <div class="card">
        <h3>4 · Value per compute</h3>
        <div class="metric"><span class="sm">${vpc_tok}</span></div>
        <div class="row"><span class="lab">primary, load-free</span>${p.mean_tokens!==null?` · mean ${p.mean_tokens.toFixed(0)} tok/item`:""}</div>
        <div class="metric" style="margin-top:8px"><span class="sm">${vpc_lat}</span></div>
        <div class="row"><span class="lab">secondary, median latency</span>${p.median_latency_s!==null?` · ${f(p.median_latency_s,3)}s`:""}</div>
      </div>
    </div>

    <div class="caveats">
      <h3>Caveats (printed with every run — honesty is the instrument)</h3>
      <ul>${p.caveats.map((c) => `<li>${escapeHtml(c)}</li>`).join("")}</ul>
    </div>

    <details class="raw">
      <summary>Show the raw command-line output</summary>
      <pre class="rawout">${escapeHtml(text)}</pre>
    </details>
  `;
  resultEl.classList.remove("hidden");
}

function escapeHtml(s) {
  return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

// example loaders
document.querySelectorAll(".chip").forEach((btn) => {
  btn.addEventListener("click", async () => {
    errEl.textContent = "";
    try {
      const obj = await fetch(btn.dataset.ex).then((r) => r.json());
      noteEl.textContent = obj.note || "";
      inputEl.value = JSON.stringify(obj, null, 1);
    } catch (e) {
      errEl.textContent = "Could not load example: " + e.message;
    }
  });
});

runBtn.addEventListener("click", measure);
boot();
