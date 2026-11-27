/* RFS Cyclorama Dawn Drop-In Motion Controller (v2.3.0, zero dependencies).
   Progressive enhancement for:
   - [data-rfs-radio-jump]  : 60fps compositor ballistic arc for Reticle Jump & Aperture Hop radios
   - [data-rfs-segmented]   : Sliding segmented cue bar indicator sync
   - [data-rfs-fader]       : Native <input type="range"> --control-value / --attr-min / --attr-max sync
   - [data-rfs-arm]         : Two-stage destructive confirmation latch (keyboard + pointer safe)
   - [data-rfs-led-ladder]  : 20-cell hardware Patch-Bay LED progress bar controller
   - [data-rfs-icon-click]  : Opt-in click micro-animations on Cyclorama Precision Silkscreen icons
   - .rfs-progress-ring     : Fallback MutationObserver for browsers without typed CSS attr() */
(() => {
  "use strict";

  const reducedMotion = (el) => {
    const scope = el && el.closest ? el.closest("[data-rfs-reduced-motion]") : null;
    if (scope && scope.dataset.rfsReducedMotion === "on") return true;
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  };

  const speedScale = (el) => {
    const scope = el && el.closest ? el.closest("[data-rfs-motion-speed]") : null;
    const raw = scope ? parseFloat(scope.dataset.rfsMotionSpeed) : 1;
    return Number.isFinite(raw) && raw > 0 ? raw : 1;
  };

  // ---- 1. Jumping Radios (Reticle Jump & Aperture Hop) ----
  const initRadioJump = (group) => {
    if (group.dataset.rfsJumpBound) return;
    group.dataset.rfsJumpBound = "1";
    const style = group.dataset.rfsRadioJump || "reticle";
    let flyer = group.querySelector(".rfs-radio-flyer");
    if (!flyer) {
      flyer = document.createElement("span");
      flyer.className = `rfs-radio-flyer ${style === "aperture" ? "is-aperture" : "is-reticle"}`;
      flyer.setAttribute("aria-hidden", "true");
      group.prepend(flyer);
    }
    const radios = Array.from(group.querySelectorAll('input[type="radio"]'));
    if (!radios.length) return;
    let activeRadio = radios.find((r) => r.checked) || radios[0];
    let currentAnim = null;

    const getPos = (radio) => {
      const gRect = group.getBoundingClientRect();
      const rRect = radio.getBoundingClientRect();
      return {
        x: rRect.left - gRect.left + (rRect.width - flyer.offsetWidth) / 2,
        y: rRect.top - gRect.top + (rRect.height - flyer.offsetHeight) / 2,
      };
    };

    const seat = (radio) => {
      if (!radio || group.offsetParent === null) return;
      const p = getPos(radio);
      flyer.style.transform = `translate3d(${p.x}px, ${p.y}px, 0)`;
    };

    group._rfsSeat = () => seat(activeRadio);
    requestAnimationFrame(() => seat(activeRadio));

    if ("ResizeObserver" in window) {
      const ro = new ResizeObserver(() => seat(activeRadio));
      ro.observe(group);
    }

    group.addEventListener("change", (e) => {
      const nextRadio = e.target;
      if (!radios.includes(nextRadio)) return;
      const from = getPos(activeRadio);
      const to = getPos(nextRadio);
      activeRadio = nextRadio;

      if (currentAnim) currentAnim.cancel();
      if (reducedMotion(group) || !flyer.animate) {
        seat(nextRadio);
        return;
      }

      const dx = to.x - from.x;
      const dy = to.y - from.y;
      const dist = Math.hypot(dx, dy);
      const mul = speedScale(group);
      const duration = Math.round((style === "aperture" ? 350 : 320) * mul);
      const lift = Math.min(20, Math.max(9, dist * (style === "aperture" ? 0.14 : 0.19)));

      const frames =
        style === "aperture"
          ? [
              { transform: `translate3d(${from.x}px, ${from.y}px, 0) scale(1)` },
              { transform: `translate3d(${from.x + dx * 0.36}px, ${from.y + dy * 0.36 - lift}px, 0) scale(0.62)`, offset: 0.38 },
              { transform: `translate3d(${to.x}px, ${to.y}px, 0) scale(1.18)`, offset: 0.78 },
              { transform: `translate3d(${to.x}px, ${to.y}px, 0) scale(1)` },
            ]
          : [
              { transform: `translate3d(${from.x}px, ${from.y}px, 0) scale(1, 1)` },
              { transform: `translate3d(${from.x + dx * 0.22}px, ${from.y + dy * 0.22 - lift * 0.65}px, 0) scale(1.32, 0.78)`, offset: 0.22 },
              { transform: `translate3d(${from.x + dx * 0.52}px, ${from.y + dy * 0.52 - lift}px, 0) scale(1.42, 0.72)`, offset: 0.5 },
              { transform: `translate3d(${to.x}px, ${to.y + 1.5}px, 0) scale(0.84, 1.16)`, offset: 0.82 },
              { transform: `translate3d(${to.x}px, ${to.y}px, 0) scale(1, 1)` },
            ];

      flyer.style.transform = `translate3d(${to.x}px, ${to.y}px, 0)`;
      currentAnim = flyer.animate(frames, {
        duration,
        easing: "cubic-bezier(0.22, 1, 0.36, 1)",
      });
    });
  };

  // ---- 2. Segmented Cue Bar ----
  const initSegmented = (bar) => {
    if (bar.dataset.rfsSegBound) return;
    bar.dataset.rfsSegBound = "1";
    const btns = Array.from(bar.querySelectorAll('[role="radio"], button'));
    bar.style.setProperty("--rfs-seg-count", String(Math.max(1, btns.length)));
    const sync = (activeBtn) => {
      const idx = Math.max(0, btns.indexOf(activeBtn));
      bar.style.setProperty("--rfs-seg-idx", String(idx));
      btns.forEach((b) => {
        const on = b === activeBtn;
        b.setAttribute("aria-checked", String(on));
        b.tabIndex = on ? 0 : -1;
      });
    };
    const initial = btns.find((b) => b.getAttribute("aria-checked") === "true") || btns[0];
    if (initial) sync(initial);
    btns.forEach((btn, idx) => {
      btn.addEventListener("click", () => sync(btn));
      btn.addEventListener("keydown", (e) => {
        if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
          e.preventDefault();
          const next = btns[(idx + (e.key === "ArrowRight" ? 1 : -1) + btns.length) % btns.length];
          sync(next);
          next.focus();
        }
      });
    });
  };

  // ---- 3. Console Fader Range Input Sync ----
  const initFader = (input) => {
    if (input.dataset.rfsFaderBound) return;
    input.dataset.rfsFaderBound = "1";
    const outId = input.dataset.rfsFaderOut;
    const outEl = outId ? document.getElementById(outId) : null;
    const unit = input.dataset.rfsFaderUnit ?? "%";
    const sync = () => {
      input.style.setProperty("--attr-min", input.min || "0");
      input.style.setProperty("--attr-max", input.max || "100");
      input.style.setProperty("--control-value", input.value);
      input.setAttribute("aria-valuetext", `${input.value}${unit}`);
      if (outEl) outEl.textContent = `${input.value}${unit}`;
    };
    sync();
    input.addEventListener("input", sync);
  };

  // ---- 4. Two-Stage Armed Destructive Latch ----
  const initArmedLatch = (btn) => {
    if (btn.dataset.rfsArmBound) return;
    btn.dataset.rfsArmBound = "1";
    const idleLabel = btn.dataset.armIdle || btn.textContent.trim();
    const armedLabel = btn.dataset.armConfirm || "[!] Confirm Action";
    const doneLabel = btn.dataset.armDone || "[ok] Completed";
    const timeoutMs = Number(btn.dataset.armTimeout || 3000);
    let timer = 0;

    btn.dataset.armed = "idle";
    btn.addEventListener("click", () => {
      clearTimeout(timer);
      const state = btn.dataset.armed;
      if (state === "idle") {
        btn.dataset.armed = "armed";
        btn.textContent = armedLabel;
        timer = setTimeout(() => {
          btn.dataset.armed = "idle";
          btn.textContent = idleLabel;
        }, timeoutMs);
      } else if (state === "armed") {
        btn.dataset.armed = "done";
        btn.textContent = doneLabel;
        btn.dispatchEvent(new CustomEvent("rfs:armed-confirm", { bubbles: true }));
        timer = setTimeout(() => {
          btn.dataset.armed = "idle";
          btn.textContent = idleLabel;
        }, 1600);
      }
    });
  };

  // ---- 5. 20-Cell Hardware Patch-Bay LED Ladder ----
  const setLadder = (el, value) => {
    if (!el) return;
    const cells = Array.from(el.querySelectorAll(".rfs-led-cell"));
    if (!cells.length) return;
    const total = cells.length;
    if (value === null || value === undefined || Number.isNaN(Number(value))) {
      el.dataset.indet = "true";
      el.dataset.done = "false";
      el.removeAttribute("aria-valuenow");
      el.setAttribute("aria-valuetext", "Loading");
      cells.forEach((c) => c.classList.remove("is-lit", "is-head"));
      return;
    }
    const pct = Math.max(0, Math.min(100, Number(value)));
    const lit = Math.round((pct / 100) * total);
    const done = pct >= 100;
    el.dataset.indet = "false";
    el.dataset.done = String(done);
    el.setAttribute("aria-valuenow", String(pct));
    el.setAttribute("aria-valuetext", `${pct}%`);
    cells.forEach((c, idx) => {
      c.classList.toggle("is-lit", idx < lit);
      c.classList.toggle("is-head", !done && lit > 0 && idx === lit - 1);
    });
  };

  const initLedLadder = (el) => {
    if (el.dataset.rfsLadderBound) return;
    el.dataset.rfsLadderBound = "1";
    const count = Math.max(8, Math.min(40, Number(el.dataset.rfsLedCount || 20)));
    el.style.setProperty("--rfs-led-count", String(count));
    if (!el.children.length) {
      for (let i = 0; i < count; i++) {
        const cell = document.createElement("span");
        cell.className = "rfs-led-cell";
        cell.style.setProperty("--i", String(i));
        cell.style.setProperty("--n", String(count - 1));
        const pct = Math.round((i / Math.max(1, count - 1)) * 100);
        cell.style.setProperty(
          "--cell-c",
          `color-mix(in oklab, var(--rfs-steel-ink) ${100 - pct}%, var(--rfs-beacon) ${pct}%)`
        );
        el.appendChild(cell);
      }
    }
    const initVal = el.dataset.rfsLedValue;
    setLadder(el, initVal === "indeterminate" ? null : Number(initVal ?? 68));
  };

  // ---- 6. Native <progress class="rfs-progress-ring"> Value Sync ----
  const syncRing = (el) => {
    const raw = el.getAttribute("value");
    if (raw === null) {
      el.style.removeProperty("--rfs-ring-val");
    } else {
      const max = parseFloat(el.getAttribute("max")) || 100;
      const pct = Math.max(0, Math.min(100, (parseFloat(raw) / max) * 100));
      el.style.setProperty("--rfs-ring-val", String(pct));
    }
  };

  const initRing = (el) => {
    if (el.dataset.rfsRingBound) return;
    el.dataset.rfsRingBound = "1";
    syncRing(el);
    if ("MutationObserver" in window) {
      const mo = new MutationObserver(() => syncRing(el));
      mo.observe(el, { attributes: true, attributeFilter: ["value", "max"] });
    }
  };

  // ---- 7. Opt-In Clickable Icon Motion Trigger ----
  const iconTimers = new WeakMap();
  const triggerIconMotion = (host) => {
    if (!host) return;
    clearTimeout(iconTimers.get(host));
    const useA = !host.classList.contains("is-anim-a");
    host.classList.toggle("is-anim-a", useA);
    host.classList.toggle("is-anim-b", !useA);

    const verb = host.dataset.rfsMotion || host.dataset.rfsIconClick || "";
    if (verb === "part-shackle") {
      host.dataset.rfsToggled = String(host.dataset.rfsToggled !== "true");
    } else if (verb === "part-faders") {
      host.dataset.rfsCue = String((Number(host.dataset.rfsCue || 0) + 1) % 3);
    } else if (verb === "part-ratchet" || verb === "ratchet-60") {
      const deg = Number(host.dataset.rfsDeg || 0) + 60;
      host.dataset.rfsDeg = String(deg);
      host.style.setProperty("--rfs-gear-deg", `${deg}deg`);
    } else if (verb === "part-copy") {
      host.dataset.rfsToggled = "true";
      iconTimers.set(
        host,
        setTimeout(() => {
          host.dataset.rfsToggled = "false";
        }, Math.round(1150 * speedScale(host)))
      );
    }
  };

  const initIconClick = (el) => {
    if (el.dataset.rfsIconBound) return;
    el.dataset.rfsIconBound = "1";
    el.addEventListener("click", () => triggerIconMotion(el));
  };

  // ---- 8. Public Init & Native Switch Fallback ----
  const initMotion = (root = document) => {
    if (!("switch" in HTMLInputElement.prototype)) {
      root.querySelectorAll('input[type="checkbox"][switch]').forEach((el) => {
        if (!el.hasAttribute("role")) el.setAttribute("role", "switch");
        el.setAttribute("data-switch-fallback", "");
      });
    }
    root.querySelectorAll("[data-rfs-radio-jump]").forEach(initRadioJump);
    root.querySelectorAll("[data-rfs-segmented]").forEach(initSegmented);
    root.querySelectorAll("input[type='range'].rfs-fader, [data-rfs-fader]").forEach(initFader);
    root.querySelectorAll("[data-rfs-arm]").forEach(initArmedLatch);
    root.querySelectorAll("[data-rfs-led-ladder]").forEach(initLedLadder);
    root.querySelectorAll("progress.rfs-progress-ring").forEach(initRing);
    root.querySelectorAll("[data-rfs-icon-click]").forEach(initIconClick);
  };

  window.RFS = Object.assign(window.RFS || {}, {
    initMotion,
    setLadder,
    syncRing,
    triggerIconMotion,
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => initMotion(document));
  } else {
    initMotion(document);
  }
})();
