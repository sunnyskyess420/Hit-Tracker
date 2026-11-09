# 1) edit from the day modal + time, 2) validate edited grams, 3) clarify quick buttons, 4) lock fallback
import sys

PATH = "index.html"
raw = open(PATH, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
src = raw.replace("\r\n", "\n")

def rep(old, new, label, expect=1):
    global src
    n = src.count(old)
    if n != expect:
        print("FAIL [%s]: %d (expected %d)" % (label, n, expect)); sys.exit(1)
    src = src.replace(old, new)

# ---------------------------------------------------------------- edit modal: time field
rep("""    <input type="hidden" id="editHitId">""",
"""    <input type="hidden" id="editHitId">
    <label>When</label>
    <input type="datetime-local" id="editHitTime">""",
label="time field")

rep("""  document.getElementById("editHitAmount").value = e.amount != null ? e.amount : "";""",
"""  const d = new Date(e.time);
  const p2 = n => String(n).padStart(2, "0");
  document.getElementById("editHitTime").value =
    d.getFullYear() + "-" + p2(d.getMonth() + 1) + "-" + p2(d.getDate())
    + "T" + p2(d.getHours()) + ":" + p2(d.getMinutes());
  document.getElementById("editHitAmount").value = e.amount != null ? e.amount : "";""",
label="populate time")

rep("""  e.device = document.getElementById("editHitDevice").value;
  e.size   = document.getElementById("editHitSize").value;
  const am = document.getElementById("editHitAmount").value;
  e.amount = am === "" ? null : (+am > 0 ? +am : null);""",
"""  const am = document.getElementById("editHitAmount").value;
  const grams = am === "" ? null : +am;
  // Same bounds the import path uses: a fat-fingered 99g would skew every total.
  if (grams != null && (isNaN(grams) || grams <= 0 || grams > 5)){
    toast("Grams must be between 0 and 5");
    return;
  }
  const when = new Date(document.getElementById("editHitTime").value);
  if (!isNaN(when.getTime())) e.time = when.toISOString();
  e.device = document.getElementById("editHitDevice").value;
  e.size   = document.getElementById("editHitSize").value;
  e.amount = grams;""",
label="validate + time")

# ---------------------------------------------------------------- edit from a day's modal
rep("""</div><button onclick="deleteEntry('${x.id}');openDay('${k}')">\u2022</button></div>`;""",
"""</div><button class="del-btn" style="color:var(--muted)" onclick="openHitEdit('${x.id}')" aria-label="Edit hit">\u270e</button><button class="del-btn" onclick="deleteEntry('${x.id}');openDay('${k}')" aria-label="Delete hit">\u2715</button></div>`;""",
label="day modal edit")

# ---------------------------------------------------------------- quick-button hint
rep("""      <select id="device" onchange="onDeviceChange()"></select>""",
"""      <select id="device" onchange="onDeviceChange()"></select>
      <p class="tiny" style="margin:4px 0 0">Quick buttons use their own grams and device \u2014 this panel only applies to the big Log button.</p>""",
label="quick hint")

# ---------------------------------------------------------------- lock fallback
rep("""  navigator.locks.request("hitTrackerInstance", { ifAvailable: true }, (lock) => {
    if (lock) return new Promise(() => {});
    const ov = document.getElementById("dupOverlay");
    if (ov) ov.classList.remove("hidden");
  }).catch(() => {});
})();""",
"""  const showDup = () => {
    const ov = document.getElementById("dupOverlay");
    if (ov) ov.classList.remove("hidden");
  };
  if (navigator.locks){
    navigator.locks.request("hitTrackerInstance", { ifAvailable: true }, (lock) => {
      if (lock) return new Promise(() => {});
      showDup();
    }).catch(() => {});
    return;
  }
  // Fallback for browsers without the Locks API: a shared heartbeat.
  const K = "htInstancePing";
  const beat = () => { try { localStorage.setItem(K, String(Date.now())); } catch(e){} };
  const prev = +(localStorage.getItem(K) || 0);
  if (Date.now() - prev < 8000) showDup();
  beat();
  setInterval(beat, 4000);
  window.addEventListener("beforeunload", () => {
    try { localStorage.removeItem(K); } catch(e){}
  });
})();""",
label="lock fallback")

open(PATH, "w", encoding="utf-8", newline="").write(src.replace("\n", nl))
print("four fixes applied")
