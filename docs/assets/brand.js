(() => {
  "use strict";

  const root = document.documentElement;
  const metaScheme = document.querySelector('meta[name="color-scheme"]');
  const $$ = (sel, el = document) => Array.from(el.querySelectorAll(sel));

  // ---- 1. Two-state Theme Switch (Dark LX 263 default; Light LX 512 opt-in) ----
  const renderedScheme = () => (metaScheme && metaScheme.content === "light" ? "light" : "dark");

  const syncThemeUI = () => {
    const mode = renderedScheme();
    const isLight = mode === "light";
    $$("[data-theme-toggle]").forEach((btn) => {
      btn.setAttribute("aria-pressed", String(isLight));
    });
    $$("[data-next-theme]").forEach((el) => {
      el.textContent = isLight ? "LX 263 Dark" : "LX 512 Light";
    });
    $$('meta[name="theme-color"]').forEach((m) => {
      m.content = isLight ? "#f5f7f9" : "#050507";
    });
  };

  const toggleTheme = (triggerEl, evt) => {
    const target = renderedScheme() === "dark" ? "light" : "dark";
    const apply = () => {
      try {
        if (target === "dark") {
          localStorage.removeItem("rfs-theme");
          localStorage.removeItem("color-scheme");
        } else {
          localStorage.setItem("rfs-theme", "light");
          localStorage.setItem("color-scheme", "light");
        }
      } catch {}
      if (metaScheme) metaScheme.content = target;
      syncThemeUI();
    };
    if (!document.startViewTransition || !triggerEl) {
      apply();
      return;
    }
    const r = triggerEl.getBoundingClientRect();
    const x = evt && evt.clientX ? evt.clientX : r.left + r.width / 2;
    const y = evt && evt.clientY ? evt.clientY : r.top + r.height / 2;
    const end = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    // Set CSS custom properties synchronously BEFORE startViewTransition so @keyframes rfs-vt-circle runs reliably on frame 0
    root.style.setProperty("--vt-x", `${x.toFixed(1)}px`);
    root.style.setProperty("--vt-y", `${y.toFixed(1)}px`);
    root.style.setProperty("--vt-r", `${end.toFixed(1)}px`);
    document.startViewTransition(apply);
  };

  $$("[data-theme-toggle]").forEach((btn) => {
    btn.hidden = false;
    btn.addEventListener("click", (evt) => toggleTheme(btn, evt));
  });
  addEventListener("storage", (e) => {
    if ((e.key !== "rfs-theme" && e.key !== "color-scheme") || !metaScheme) return;
    metaScheme.content = e.newValue === "light" ? "light" : "dark";
    syncThemeUI();
  });
  syncThemeUI();

  // ---- 2. Scrollspy inside App-Shell Scroll Region (.page-scroll) ----
  const pageScroll = document.getElementById("page-scroll");
  const navLinks = $$(".section-nav a[href^='#']");
  if (navLinks.length && "IntersectionObserver" in window) {
    const sections = navLinks
      .map((a) => document.getElementById(a.getAttribute("href").slice(1)))
      .filter(Boolean);
    const markActive = (id) => {
      navLinks.forEach((a) => {
        const hit = a.getAttribute("href") === `#${id}`;
        a.classList.toggle("target-current", hit);
        a.setAttribute("aria-current", hit ? "true" : "false");
      });
    };
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) markActive(entry.target.id);
        });
      },
      { root: pageScroll || null, rootMargin: "-20% 0px -65% 0px", threshold: 0 }
    );
    sections.forEach((sec) => io.observe(sec));
    navLinks.forEach((a) => {
      a.addEventListener("click", () => markActive(a.getAttribute("href").slice(1)));
    });
  }

  // ---- 3. Copy Buttons via Invoker Commands (--copy) + Fallback + Click-to-Copy Swatches ----
  const copyTimers = new WeakMap();
  let lastAnnouncement = "";

  const reportCopy = (btn, ok) => {
    const tip = btn.nextElementSibling;
    clearTimeout(copyTimers.get(btn));
    btn.removeAttribute("data-copied");
    btn.removeAttribute("data-failed");
    let msg = ok ? "Copied" : "Copy failed";
    if (msg === lastAnnouncement) msg += "\u00A0";
    lastAnnouncement = msg;
    if (tip) tip.textContent = "";
    void btn.offsetWidth;
    btn.setAttribute(ok ? "data-copied" : "data-failed", "");
    if (tip) requestAnimationFrame(() => (tip.textContent = msg));
    copyTimers.set(
      btn,
      setTimeout(() => {
        btn.removeAttribute("data-copied");
        btn.removeAttribute("data-failed");
        if (tip) tip.textContent = "";
      }, 1900)
    );
  };

  const runCopy = async (btn, target) => {
    if (!target) return;
    const text = target.matches("input, textarea") ? target.value : target.innerText.trim();
    if (!text) return;
    try {
      await navigator.clipboard.writeText(text);
      reportCopy(btn, true);
    } catch {
      reportCopy(btn, false);
    }
  };

  if ("CommandEvent" in window) {
    document.addEventListener(
      "command",
      (event) => {
        if (event.command === "--copy") runCopy(event.source, event.target);
      },
      true
    );
  } else {
    document.addEventListener("click", (event) => {
      if (event.defaultPrevented) return;
      const btn = event.target.closest('button[command="--copy"]');
      if (!btn) return;
      const target = document.getElementById(btn.getAttribute("commandfor"));
      runCopy(btn, target);
    });
  }

  // Swatch hex click-to-copy with live status announcement
  const globalStatus = document.getElementById("copy-status");
  $$("[data-copy-value]").forEach((btn) => {
    const orig = btn.innerHTML;
    btn.addEventListener("click", async () => {
      const val = btn.getAttribute("data-copy-value");
      try {
        await navigator.clipboard.writeText(val);
        let msg = `Copied ${val}`;
        if (msg === lastAnnouncement) msg += "\u00A0";
        lastAnnouncement = msg;
        if (globalStatus) globalStatus.textContent = msg;
        const label = btn.querySelector(".swatch-val");
        if (label) {
          label.textContent = "Copied";
          clearTimeout(btn._t);
          btn._t = setTimeout(() => {
            btn.innerHTML = orig;
          }, 1200);
        }
      } catch {}
    });
  });

  // Hero calibration plate gel swatch click-to-copy (theme-aware dark/light hex)
  $$("[data-spec-copy]").forEach((btn) => {
    const hexEl = btn.querySelector(".spec-gel-hex");
    const origHexHtml = hexEl ? hexEl.innerHTML : "";
    btn.addEventListener("click", async () => {
      const val = renderedScheme() === "light" ? btn.dataset.hexLight : btn.dataset.hexDark;
      if (!val) return;
      try {
        await navigator.clipboard.writeText(val);
        btn.classList.add("is-copied");
        if (hexEl) hexEl.textContent = "copied";
        if (globalStatus) {
          let msg = `Copied ${val}`;
          if (msg === lastAnnouncement) msg += "\u00A0";
          lastAnnouncement = msg;
          globalStatus.textContent = msg;
        }
        clearTimeout(btn._t);
        btn._t = setTimeout(() => {
          btn.classList.remove("is-copied");
          if (hexEl) hexEl.innerHTML = origHexHtml;
        }, 1200);
      } catch {}
    });
  });

  // ---- 4. §2 Interactive Six-Phase Cyclorama Desk ----
  const CUES = [
    { lx: "LX 001", name: "Blackout", mode: "Dark", stops: "#06070A -> #090B10 -> #131922" },
    { lx: "LX 127", name: "Glacial Steel", mode: "Dark", stops: "#070A0E -> #133954 -> #1F547A" },
    { lx: "LX 263", name: "Beacon Horizon", mode: "Dark default", stops: "#07090D -> #1E5078 -> #CC5016 -> #F06E2B" },
    { lx: "LX 389", name: "Maritime Flame", mode: "Dark", stops: "#0B0707 -> #7A2A0A -> #CC5016" },
    { lx: "LX 455", name: "Warm Frost", mode: "Light", stops: "#FDF8F5 -> #F0E6DE -> #DCE5ED" },
    { lx: "LX 512", name: "Alabaster Day", mode: "Light default", stops: "#F5F7F9 -> #F0F4F8 -> #FDF5F0" },
  ];

  const cycStage = document.getElementById("cyc-stage");
  const cycCode = document.getElementById("cyc-code");
  const cycStops = document.getElementById("cyc-stops");
  const cycSlider = document.getElementById("cyc-slider");
  const cycBtns = $$("[data-cyc-cue]");

  const setCue = (idx) => {
    const i = Math.max(0, Math.min(5, Number(idx)));
    const cue = CUES[i];
    if (cycStage) cycStage.setAttribute("data-cue", String(i));
    if (cycCode) cycCode.textContent = `${cue.lx} · ${cue.name}`;
    if (cycStops) cycStops.textContent = `${cue.mode}  |  ${cue.stops}`;
    if (cycSlider) cycSlider.value = String(i);
    cycBtns.forEach((b) => b.setAttribute("aria-pressed", String(Number(b.dataset.cycCue) === i)));
  };

  if (cycSlider) cycSlider.addEventListener("input", () => setCue(cycSlider.value));
  cycBtns.forEach((b) => b.addEventListener("click", () => setCue(b.dataset.cycCue)));

  // ---- 5. §3 Live Typography Specimen Tester ----
  const typeInput = document.getElementById("type-tester-input");
  const outDisplay = document.getElementById("type-out-display");
  const outSans = document.getElementById("type-out-sans");
  const outMono = document.getElementById("type-out-mono");
  if (typeInput) {
    const updateType = () => {
      const val = typeInput.value.trim() || "Real-Fruit-Snacks. Built local-first.";
      if (outDisplay) outDisplay.textContent = val;
      if (outSans) outSans.textContent = val;
      if (outMono) outMono.textContent = `$ ${val.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "rfs"} --check`;
    };
    typeInput.addEventListener("input", updateType);
  }

  // ---- 6. §5 Interactive Controls, Indeterminate & 4-Loader Workbench + §6 Blueprint ----
  $$("[data-demo-pill]").forEach((pill) => {
    pill.addEventListener("click", () => {
      const pressed = pill.getAttribute("aria-pressed") === "true";
      pill.setAttribute("aria-pressed", String(!pressed));
    });
  });

  const indetBtn = document.getElementById("ctrl-indet-btn");
  if (indetBtn) {
    let isIndet = false;
    const indetBoxes = $$("[data-indet-demo]");
    indetBtn.addEventListener("click", () => {
      isIndet = !isIndet;
      indetBtn.setAttribute("aria-pressed", String(isIndet));
      indetBoxes.forEach((cb) => {
        cb.indeterminate = isIndet;
        if (!isIndet) cb.checked = true;
      });
    });
  }

  // §05B Hardware Loading Bars & Precision Ring interactive workbench
  const ldDmx = document.getElementById("ld-dmx");
  const ldBeam = document.getElementById("ld-beam");
  const ldLed = document.getElementById("ld-led");
  const ldRing = document.getElementById("ld-ring");
  const ldRingTxt = document.getElementById("ld-ring-txt");
  const ldScrub = document.getElementById("ld-scrub");
  const ldScrubOut = document.getElementById("ld-scrub-out");
  const ldDmxVal = document.getElementById("ld-dmx-val");
  const ldBeamVal = document.getElementById("ld-beam-val");
  const ldLedVal = document.getElementById("ld-led-val");
  const ldDetBtn = document.getElementById("ld-mode-det");
  const ldIndBtn = document.getElementById("ld-mode-ind");
  const ldSimBtn = document.getElementById("ld-sim-btn");

  if (ldDmx && ldBeam && ldLed && ldRing && ldScrub) {
    let ldIndet = false;
    let ldSimTimer = 0;

    const renderAllLoaders = (val) => {
      if (ldScrubOut) ldScrubOut.innerHTML = `<span class="k">${ldIndet ? "auto" : `${val}%`}</span>`;
      if (ldIndet) {
        [ldDmx, ldBeam, ldRing].forEach((el) => {
          el.removeAttribute("value");
          el.setAttribute("aria-valuetext", "Loading");
        });
        if (window.RFS && window.RFS.setLadder) window.RFS.setLadder(ldLed, null);
        if (window.RFS && window.RFS.syncRing) window.RFS.syncRing(ldRing);
        if (ldRingTxt) ldRingTxt.textContent = "…";
        if (ldDmxVal) ldDmxVal.textContent = "[scan]";
        if (ldBeamVal) ldBeamVal.textContent = "[busy]";
        if (ldLedVal) ldLedVal.textContent = "LIVE";
      } else {
        const done = val >= 100;
        const lit = Math.round((val / 100) * 20);
        [ldDmx, ldBeam, ldRing].forEach((el) => {
          el.setAttribute("value", String(val));
          el.setAttribute("aria-valuetext", `${val}%`);
        });
        if (window.RFS && window.RFS.setLadder) window.RFS.setLadder(ldLed, val);
        if (window.RFS && window.RFS.syncRing) window.RFS.syncRing(ldRing);
        if (ldRingTxt) ldRingTxt.textContent = done ? "OK" : `${val}%`;
        if (ldDmxVal) {
          ldDmxVal.textContent = done ? "[ok] 100%" : `${val}%`;
          ldDmxVal.style.color = done ? "var(--rfs-signal)" : "var(--rfs-beacon-ink)";
        }
        if (ldBeamVal) {
          ldBeamVal.textContent = done ? "[ok] 100%" : `${val}%`;
          ldBeamVal.style.color = done ? "var(--rfs-signal)" : "var(--rfs-steel-ink)";
        }
        if (ldLedVal) {
          ldLedVal.textContent = done ? "[ok] 20/20" : `${lit} / 20`;
          ldLedVal.style.color = done ? "var(--rfs-signal)" : "var(--rfs-text)";
        }
      }
    };

    const setLoaderMode = (indet) => {
      clearInterval(ldSimTimer);
      ldIndet = indet;
      if (ldDetBtn) ldDetBtn.setAttribute("aria-pressed", String(!indet));
      if (ldIndBtn) ldIndBtn.setAttribute("aria-pressed", String(indet));
      ldScrub.disabled = indet;
      renderAllLoaders(Number(ldScrub.value));
    };

    if (ldDetBtn) ldDetBtn.addEventListener("click", () => setLoaderMode(false));
    if (ldIndBtn) ldIndBtn.addEventListener("click", () => setLoaderMode(true));
    ldScrub.addEventListener("input", () => {
      clearInterval(ldSimTimer);
      if (ldIndet) setLoaderMode(false);
      renderAllLoaders(Number(ldScrub.value));
    });

    if (ldSimBtn) {
      ldSimBtn.addEventListener("click", () => {
        clearInterval(ldSimTimer);
        if (ldIndet) setLoaderMode(false);
        let v = 0;
        ldScrub.value = "0";
        ldScrub.style.setProperty("--control-value", "0");
        renderAllLoaders(0);
        ldSimTimer = setInterval(() => {
          v = Math.min(100, v + (v < 70 ? 6 : 4));
          ldScrub.value = String(v);
          ldScrub.style.setProperty("--control-value", String(v));
          renderAllLoaders(v);
          if (v >= 100) clearInterval(ldSimTimer);
        }, 55);
      });
    }
    renderAllLoaders(68);
  }

  const markBp = document.getElementById("mark-blueprint");
  const markBpBtns = $$("[data-bp-mode-btn]");
  if (markBp && markBpBtns.length) {
    markBpBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const mode = btn.dataset.bpModeBtn || "blueprint";
        markBp.dataset.bpMode = mode;
        markBpBtns.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      });
    });
  }

  // ---- 6b. §9 Org Art Standards Tabs (Static vs. Animated One-Shot vs. Ambient Board) ----
  const artTabsRoot = document.getElementById("art-standards-tabs");
  if (artTabsRoot) {
    const tablist = artTabsRoot.querySelector('[role="tablist"]');
    const tabs = $$('[role="tab"]', tablist);
    const panels = $$('[role="tabpanel"]', artTabsRoot);
    const hasFocusGroup = Object.hasOwn(HTMLElement.prototype, "focusGroup");
    let animCounter = 0;

    const replayOneShotBanner = () => {
      animCounter += 1;
      $$("[data-anim-banner]", artTabsRoot).forEach((img) => {
        const base = img.dataset.animSrc;
        if (base) img.src = `${base}?play=${animCounter}`;
      });
    };

    const selectArtTab = (targetTab, moveFocus = false) => {
      const idx = tabs.indexOf(targetTab);
      if (idx < 0) return;
      tabs.forEach((tab, i) => {
        const active = i === idx;
        tab.setAttribute("aria-selected", String(active));
        tab.toggleAttribute("focusgroupstart", active);
        if (!hasFocusGroup) tab.tabIndex = active ? 0 : -1;
      });
      panels.forEach((panel, i) => {
        const active = i === idx;
        if (active) {
          panel.hidden = false;
          if (!panel.querySelector("button, a, input")) panel.tabIndex = 0;
        } else {
          panel.hidden = "until-found";
          panel.removeAttribute("tabindex");
        }
      });
      targetTab.scrollIntoView({ block: "nearest", inline: "nearest", container: "nearest" });
      if (moveFocus) targetTab.focus();
      if (targetTab.id === "art-tab-oneshot") replayOneShotBanner();
    };

    if (!hasFocusGroup) {
      tabs.forEach((tab, i) => {
        tab.tabIndex = i === 0 ? 0 : -1;
      });
      // Selection by activation: arrow keys move focus without prematurely starting animations or changing height
      tablist.addEventListener("keydown", (e) => {
        const cur = tabs.indexOf(document.activeElement);
        if (cur < 0) return;
        let next = -1;
        if (e.key === "ArrowRight") next = (cur + 1) % tabs.length;
        else if (e.key === "ArrowLeft") next = (cur - 1 + tabs.length) % tabs.length;
        else if (e.key === "Home") next = 0;
        else if (e.key === "End") next = tabs.length - 1;
        if (next >= 0) {
          e.preventDefault();
          tabs[next].focus();
        }
      });
    }

    tabs.forEach((tab) => {
      tab.addEventListener("click", () => selectArtTab(tab));
    });

    // Keep tab selection synced when find-in-page matches inside a hidden="until-found" panel
    panels.forEach((panel, i) => {
      panel.addEventListener("beforematch", () => selectArtTab(tabs[i]));
    });

    const replayBannerBtn = document.getElementById("banner-replay");
    if (replayBannerBtn) {
      replayBannerBtn.addEventListener("click", replayOneShotBanner);
    }

    // WCAG 2.2.2 Pause / Play control for >5s Ambient Board (enabled by default; user can pause anytime)
    const boardBtn = document.getElementById("board-toggle-play");
    const boardBadge = document.getElementById("board-state-badge");
    const boardImgs = $$("[data-ambient-board]", artTabsRoot);
    let boardPaused = false;

    const syncBoardPlayback = () => {
      boardImgs.forEach((img) => {
        const target = boardPaused ? img.dataset.staticSrc : `${img.dataset.liveSrc}?p=${++animCounter}`;
        if (target) img.src = target;
      });
      if (boardBtn) boardBtn.textContent = boardPaused ? "Play" : "Pause";
      if (boardBadge) {
        boardBadge.innerHTML = boardPaused
          ? '<span class="k">[paused]</span> static base frame'
          : '<span class="k">[ambient]</span> 54.4s cycle';
        boardBadge.classList.toggle("b-ok", !boardPaused);
        boardBadge.classList.toggle("b-steel", boardPaused);
      }
    };

    if (boardBtn) {
      if (boardPaused) syncBoardPlayback();
      boardBtn.addEventListener("click", () => {
        boardPaused = !boardPaused;
        syncBoardPlayback();
      });
    }
  }

  // ---- 7. §11 Motion Choreography & Interactive Lab ----
  // Parameterized cubic-bezier solver so the dot rides on whichever curve preset is selected
  const CURVE_PRESETS = {
    expo: {
      token: "--rfs-ease",
      formula: "cubic-bezier(0.16, 1, 0.3, 1)",
      desc: "Instant ignition, settled landing — entrances, DMX fader lifts, focus sweeps, and rule draws.",
      pts: [0.16, 1.0, 0.3, 1.0],
    },
    detent: {
      token: "--rfs-ease-detent",
      formula: "linear(0, 0.21 8%, 0.64 19%, 0.94 31%, 1.035 44%, 1.02 58%, 0.996 74%, 1)",
      desc: "3.5% mechanical hardware detent — switches, checkboxes, jumping radios, and icon ratchets (zero jelly bounce).",
      pts: [0.22, 1.18, 0.36, 1.0],
    },
    inout: {
      token: "--rfs-ease-in-out",
      formula: "cubic-bezier(0.65, 0, 0.35, 1)",
      desc: "Symmetric console crossfade — Cyclorama lighting transitions, cue shifts, and A/B state swaps.",
      pts: [0.65, 0.0, 0.35, 1.0],
    },
    exit: {
      token: "--rfs-ease-exit",
      formula: "cubic-bezier(0.7, 0, 0.84, 0)",
      desc: "Crisp acceleration out — closing overlays, copy-tip dismissals, and clearing retired notices.",
      pts: [0.7, 0.0, 0.84, 0.0],
    },
    linear: {
      token: "--rfs-ease-linear",
      formula: "linear (0, 0, 1, 1)",
      desc: "Constant-rate telemetry — 3.2s console dwell progress sweeps and clock-locked timelines.",
      pts: [0.0, 0.0, 1.0, 1.0],
    },
  };

  let activeCurveKey = "expo";
  const solveBezier = (t, [x1, y1, x2, y2]) => {
    if (t <= 0) return 0;
    if (t >= 1) return 1;
    if (x1 === y1 && x2 === y2) return t;
    const bx = (u) => 3 * (1 - u) * (1 - u) * u * x1 + 3 * (1 - u) * u * u * x2 + u * u * u;
    const bdx = (u) => 3 * (1 - u) * (1 - u) * x1 + 6 * (1 - u) * u * (x2 - x1) + 3 * u * u * (1 - x2);
    const by = (u) => 3 * (1 - u) * (1 - u) * u * y1 + 3 * (1 - u) * u * u * y2 + u * u * u;
    let u = t;
    for (let k = 0; k < 8; k++) {
      const dx = bdx(u);
      if (Math.abs(dx) < 1e-6) break;
      u = Math.max(0, Math.min(1, u - (bx(u) - t) / dx));
    }
    return by(u);
  };

  const playCurveBtn = document.getElementById("play-curve");
  const playCurveRaceBtn = document.getElementById("play-curve-race");
  const curveDot = document.getElementById("curve-dot");
  const curveOutDot = document.getElementById("curve-out-dot");
  const guideX = document.getElementById("curve-guide-x");
  const guideY = document.getElementById("curve-guide-y");
  const curvePathEl = document.getElementById("curve-path");
  const curveHandlesEl = document.getElementById("curve-handles");
  const curveP1El = document.getElementById("curve-p1");
  const curveP2El = document.getElementById("curve-p2");
  const curveTokenEl = document.getElementById("curve-token");
  const curveFormulaEl = document.getElementById("curve-formula");
  const curveDescEl = document.getElementById("curve-desc");
  const curvePresetBtns = $$("[data-curve-preset]");
  let curveRaf = 0;
  let curveResetTimer = 0;

  if (playCurveBtn && curveDot) {
    const placeDot = (t, showGuides) => {
      const pts = CURVE_PRESETS[activeCurveKey].pts;
      const x = t * 100;
      const y = 100 - solveBezier(t, pts) * 100;
      curveDot.setAttribute("cx", x.toFixed(2));
      curveDot.setAttribute("cy", y.toFixed(2));
      if (curveOutDot) curveOutDot.setAttribute("cy", y.toFixed(2));
      if (guideX) {
        guideX.setAttribute("x1", x.toFixed(2));
        guideX.setAttribute("x2", x.toFixed(2));
        guideX.setAttribute("y2", y.toFixed(2));
        guideX.setAttribute("opacity", showGuides ? "0.7" : "0");
      }
      if (guideY) {
        guideY.setAttribute("x1", x.toFixed(2));
        guideY.setAttribute("y1", y.toFixed(2));
        guideY.setAttribute("y2", y.toFixed(2));
        guideY.setAttribute("opacity", showGuides ? "0.7" : "0");
      }
    };

    const runCurvePlayback = () => {
      cancelAnimationFrame(curveRaf);
      clearTimeout(curveResetTimer);
      const dur = 950;
      const t0 = performance.now();
      const frame = (now) => {
        const t = Math.min(1, (now - t0) / dur);
        placeDot(t, t < 1);
        if (t < 1) {
          curveRaf = requestAnimationFrame(frame);
        } else {
          curveResetTimer = setTimeout(() => placeDot(0, false), 550);
        }
      };
      placeDot(0, true);
      curveRaf = requestAnimationFrame(frame);
    };

    const selectCurve = (key, autoPlay = false) => {
      const cfg = CURVE_PRESETS[key];
      if (!cfg) return;
      activeCurveKey = key;
      const [x1, y1, x2, y2] = cfg.pts;
      const p1x = (x1 * 100).toFixed(1);
      const p1y = (100 - y1 * 100).toFixed(1);
      const p2x = (x2 * 100).toFixed(1);
      const p2y = (100 - y2 * 100).toFixed(1);
      if (curvePathEl) curvePathEl.setAttribute("d", `M0 100C${p1x} ${p1y} ${p2x} ${p2y} 100 0`);
      if (curveHandlesEl) curveHandlesEl.setAttribute("d", `M0 100L${p1x} ${p1y} M100 0L${p2x} ${p2y}`);
      if (curveP1El) {
        curveP1El.setAttribute("cx", p1x);
        curveP1El.setAttribute("cy", p1y);
      }
      if (curveP2El) {
        curveP2El.setAttribute("cx", p2x);
        curveP2El.setAttribute("cy", p2y);
      }
      if (curveTokenEl) curveTokenEl.textContent = cfg.token;
      if (curveFormulaEl) curveFormulaEl.textContent = cfg.formula;
      if (curveDescEl) curveDescEl.textContent = cfg.desc;
      curvePresetBtns.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.curvePreset === key)));
      cancelAnimationFrame(curveRaf);
      clearTimeout(curveResetTimer);
      placeDot(0, false);
      if (autoPlay) runCurvePlayback();
    };

    curvePresetBtns.forEach((btn) => {
      btn.addEventListener("click", () => selectCurve(btn.dataset.curvePreset, true));
    });
    playCurveBtn.addEventListener("click", runCurvePlayback);

    if (playCurveRaceBtn) {
      playCurveRaceBtn.addEventListener("click", () => {
        $$("[data-race-ease]").forEach((dot) => {
          dot.getAnimations().forEach((a) => a.cancel());
          const track = dot.parentElement;
          const dist = Math.max(24, (track ? track.clientWidth : 120) - dot.offsetWidth - 8);
          const easing = dot.dataset.raceEase || "linear";
          dot.animate(
            [{ transform: "translateX(0px)" }, { transform: `translateX(${dist}px)` }],
            { duration: 950, easing, fill: "forwards" }
          );
        });
        runCurvePlayback();
      });
    }
  }

  const raceBtn = document.getElementById("play-dur-race");
  if (raceBtn) {
    raceBtn.addEventListener("click", () => {
      $$("[data-dur-ms]").forEach((bar) => {
        bar.getAnimations().forEach((a) => a.cancel());
        const ms = Number(bar.dataset.durMs) || 250;
        bar.animate(
          [{ transform: "scaleX(0)" }, { transform: "scaleX(1)" }],
          { duration: ms, easing: "cubic-bezier(0.16, 1, 0.3, 1)", fill: "both" }
        );
      });
    });
  }

  const replayClass = (el, cls = "is-playing") => {
    if (!el) return;
    el.classList.remove(cls);
    void el.offsetWidth;
    el.classList.add(cls);
  };

  // Terminal typing simulator (45ms/char + 150ms line gap + 2 cursor blinks)
  let termTimer = 0;
  const playTerm = () => {
    const pre = document.getElementById("motion-term");
    if (!pre) return;
    clearTimeout(termTimer);
    const cmdText = "port-sync check";
    const cmdSpan = pre.querySelector(".t-cmd");
    const outLines = $$(".t-out", pre);
    const endCursor = pre.querySelector(".cursor");
    if (!cmdSpan) return;
    cmdSpan.textContent = "";
    outLines.forEach((l) => l.classList.add("is-wait"));
    if (endCursor) endCursor.classList.remove("is-blink");
    let idx = 0;
    const stepChar = () => {
      if (idx <= cmdText.length) {
        cmdSpan.textContent = cmdText.slice(0, idx++);
        termTimer = setTimeout(stepChar, 45);
      } else {
        let li = 0;
        const stepOut = () => {
          if (li < outLines.length) {
            outLines[li++].classList.remove("is-wait");
            termTimer = setTimeout(stepOut, 160);
          } else if (endCursor) {
            void endCursor.offsetWidth;
            endCursor.classList.add("is-blink");
          }
        };
        termTimer = setTimeout(stepOut, 180);
      }
    };
    stepChar();
  };

  // Specimens 8, 9, 12 interactive controllers
  const XFADE_LABELS = ["LX 263 · BEACON HORIZON", "LX 127 · GLACIAL STEEL", "LX 512 · ALABASTER DAY"];
  const playXfade = () => {
    const stage = document.getElementById("motion-xfade");
    const lbl = document.getElementById("motion-xfade-lbl");
    if (!stage) return;
    const next = (Number(stage.dataset.phase || 0) + 1) % 3;
    stage.dataset.phase = String(next);
    if (lbl) lbl.textContent = XFADE_LABELS[next];
  };

  let tactileTimers = [];
  const playTactile = () => {
    const btn = document.getElementById("motion-tactile");
    const st = document.getElementById("motion-tactile-state");
    if (!btn) return;
    tactileTimers.forEach(clearTimeout);
    tactileTimers = [];
    const set = (cls, html) => {
      btn.classList.remove("sim-hover", "sim-press", "sim-focus");
      if (cls) btn.classList.add(cls);
      if (st) st.innerHTML = html;
    };
    set("sim-hover", '<span class="k">[hover]</span> -3px');
    tactileTimers.push(setTimeout(() => set("sim-press", '<span class="k">[press]</span> +1px'), 420));
    tactileTimers.push(setTimeout(() => set("sim-focus", '<span class="k">[focus]</span> 2px ring'), 840));
    tactileTimers.push(setTimeout(() => set("", '<span class="k">[idle]</span> 0px'), 1550));
  };
  const tactileBtnEl = document.getElementById("motion-tactile");
  if (tactileBtnEl) tactileBtnEl.addEventListener("click", playTactile);

  let drawerTimer = 0;
  const toggleDrawerDemo = () => {
    const el = document.getElementById("motion-drawer");
    if (!el) return;
    clearTimeout(drawerTimer);
    el.classList.add("is-closed");
    drawerTimer = setTimeout(() => el.classList.remove("is-closed"), 560);
  };

  const triggerReplay = (target) => {
    if (target === "draw") replayClass(document.getElementById("motion-draw"));
    else if (target === "sweep") {
      replayClass(document.getElementById("motion-sweep"));
      replayClass(document.getElementById("motion-sweep-link"));
    } else if (target === "term") playTerm();
    else if (target === "beam") replayClass(document.getElementById("motion-beam"));
    else if (target === "stagger") $$(".stagger-tile").forEach((t) => replayClass(t));
    else if (target === "fader") replayClass(document.getElementById("motion-fader"));
    else if (target === "xfade") playXfade();
    else if (target === "tactile") playTactile();
    else if (target === "toast") replayClass(document.getElementById("motion-toast"));
    else if (target === "conduit") replayClass(document.getElementById("motion-conduit"));
    else if (target === "drawer") toggleDrawerDemo();
  };

  $$("[data-replay]").forEach((btn) => {
    btn.addEventListener("click", () => triggerReplay(btn.dataset.replay));
  });

  const replayAllBtn = document.getElementById("replay-all-motion");
  if (replayAllBtn) {
    replayAllBtn.addEventListener("click", () => {
      ["draw", "sweep", "term", "beam", "stagger", "fader", "xfade", "tactile", "toast", "conduit", "drawer"].forEach(triggerReplay);
    });
  }

  // ---- 8. §13 System Standards Interactive Specimens ----
  // 8a. 60-Icon Precision Silkscreen Browser (size, tone, category, search, static copy & opt-in live click motion)
  const iconGrid = document.getElementById("icon-specimen-grid");
  const iconSizeBtns = $$("[data-icon-size]");
  const iconToneBtns = $$("[data-icon-tone]");
  const iconCatBtns = $$("[data-icon-cat-filter]");
  const iconInteractBtns = $$("[data-icon-interact]");
  const iconSlowBtn = document.getElementById("icon-motion-slow");
  const iconCascadeBtn = document.getElementById("icon-motion-cascade");
  const iconSearch = document.getElementById("icon-search");
  const iconStatus = document.getElementById("icon-copy-status");
  const iconEmpty = document.getElementById("icon-empty-state");
  const iconClearBtn = document.getElementById("icon-clear-filter");
  const iconSpriteCode = document.getElementById("cmd-icon-sprite");
  const iconTiles = iconGrid ? $$(".icon-tile", iconGrid) : [];

  if (iconGrid && iconTiles.length) {
    let activeCat = "all";
    let activeTone = iconGrid.dataset.tone || "text";
    let activeInteract = "copy";
    let activeIconName = "terminal";
    let activeMotionVerb = "part-prompt";
    let statusTimer = 0;

    const TONE_META = {
      text:    { cls: "",                 cssVar: null },
      steel:   { cls: " rfs-icon-steel",  cssVar: "--rfs-steel-ink" },
      beacon:  { cls: " rfs-icon-beacon", cssVar: "--rfs-beacon-ink" },
      ok:      { cls: " rfs-icon-ok",     cssVar: "--rfs-signal" },
      warn:    { cls: " rfs-icon-warn",   cssVar: "--rfs-accent" },
      fail:    { cls: " rfs-icon-fail",   cssVar: "--rfs-fault" },
      horizon: { cls: " rfs-icon-horizon", cssVar: "horizon" },
    };

    const renderSpriteSnippet = () => {
      if (!iconSpriteCode) return;
      const meta = TONE_META[activeTone] || TONE_META.text;
      const clsStr = `rfs-icon${meta.cls}`;
      if (activeInteract === "motion") {
        iconSpriteCode.innerHTML =
          `<span class="rfs-tok-kw">&lt;button</span> <span class="rfs-tok-fn">class</span>=<span class="rfs-tok-str">"rfs-btn rfs-icon-live"</span> ` +
          `<span class="rfs-tok-fn">data-rfs-motion</span>=<span class="rfs-tok-str">"${activeMotionVerb}"</span> ` +
          `<span class="rfs-tok-fn">data-rfs-icon-click</span><span class="rfs-tok-kw">&gt;&lt;svg</span> ` +
          `<span class="rfs-tok-fn">class</span>=<span class="rfs-tok-str">"${clsStr}"</span> ` +
          `<span class="rfs-tok-fn">aria-hidden</span>=<span class="rfs-tok-str">"true"</span>` +
          `<span class="rfs-tok-kw">&gt;</span><span class="rfs-tok-com">&lt;!-- ${activeIconName}.svg --&gt;</span>` +
          `<span class="rfs-tok-kw">&lt;/svg&gt;&lt;/button&gt;</span>`;
      } else {
        iconSpriteCode.innerHTML =
          `<span class="rfs-tok-kw">&lt;svg</span> ` +
          `<span class="rfs-tok-fn">class</span>=<span class="rfs-tok-str">"${clsStr}"</span> ` +
          `<span class="rfs-tok-fn">aria-hidden</span>=<span class="rfs-tok-str">"true"</span>` +
          `<span class="rfs-tok-kw">&gt;&lt;use</span> ` +
          `<span class="rfs-tok-fn">href</span>=<span class="rfs-tok-str">"rfs-icons.svg#rfs-i-${activeIconName}"</span>` +
          `<span class="rfs-tok-kw">/&gt;&lt;/svg&gt;</span>`;
      }
    };

    const setStatus = (toneClass, key, text) => {
      if (!iconStatus) return;
      iconStatus.className = `rfs-badge ${toneClass}`;
      iconStatus.innerHTML = `<span class="k">${key}</span> ${text}`;
    };

    const filterIcons = () => {
      const q = (iconSearch ? iconSearch.value : "").trim().toLowerCase();
      let shown = 0;
      iconTiles.forEach((tile) => {
        const catOk = activeCat === "all" || tile.dataset.iconCat === activeCat;
        const hay = `${tile.dataset.iconName} ${tile.dataset.iconCat} ${tile.dataset.iconTags} ${tile.dataset.rfsMotion || ""}`.toLowerCase();
        const qOk = !q || hay.includes(q);
        const match = catOk && qOk;
        tile.hidden = !match;
        if (match) shown += 1;
      });
      if (iconEmpty) iconEmpty.hidden = shown > 0;
      clearTimeout(statusTimer);
      const hint = activeInteract === "motion" ? "click to test motion" : "click to copy SVG";
      setStatus("b-steel", `[${shown}/${iconTiles.length}]`, hint);
    };

    const setInteractMode = (mode) => {
      activeInteract = mode === "motion" ? "motion" : "copy";
      iconGrid.dataset.interact = activeInteract;
      iconTiles.forEach((tile) => tile.classList.toggle("rfs-icon-live", activeInteract === "motion"));
      iconInteractBtns.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.iconInteract === activeInteract)));
      renderSpriteSnippet();
      filterIcons();
    };

    iconInteractBtns.forEach((btn) => {
      btn.addEventListener("click", () => setInteractMode(btn.dataset.iconInteract));
    });

    if (iconSlowBtn) {
      iconSlowBtn.addEventListener("click", () => {
        const slow = iconSlowBtn.getAttribute("aria-pressed") !== "true";
        iconSlowBtn.setAttribute("aria-pressed", String(slow));
        iconGrid.style.setProperty("--rfs-motion-speed", slow ? "3.5" : "1");
        iconGrid.dataset.rfsMotionSpeed = slow ? "3.5" : "1";
      });
    }

    if (iconCascadeBtn) {
      iconCascadeBtn.addEventListener("click", () => {
        if (activeInteract !== "motion") setInteractMode("motion");
        const visible = iconTiles.filter((t) => !t.hidden);
        const step = visible.length > 20 ? 45 : 75;
        visible.forEach((tile, i) => {
          setTimeout(() => {
            if (window.RFS && window.RFS.triggerIconMotion) window.RFS.triggerIconMotion(tile);
          }, i * step);
        });
        setStatus("b-beacon", "[live]", `cascaded ${visible.length} icons`);
      });
    }

    iconSizeBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const size = btn.dataset.iconSize || "24";
        iconGrid.dataset.size = size;
        iconSizeBtns.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      });
    });

    iconToneBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        activeTone = btn.dataset.iconTone || "text";
        iconGrid.dataset.tone = activeTone;
        iconToneBtns.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        renderSpriteSnippet();
      });
    });

    iconCatBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        activeCat = btn.dataset.iconCatFilter || "all";
        iconCatBtns.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        filterIcons();
      });
    });

    if (iconSearch) {
      iconSearch.addEventListener("input", filterIcons);
    }

    if (iconClearBtn) {
      iconClearBtn.addEventListener("click", () => {
        activeCat = "all";
        if (iconSearch) iconSearch.value = "";
        iconCatBtns.forEach((b) =>
          b.setAttribute("aria-pressed", String(b.dataset.iconCatFilter === "all"))
        );
        filterIcons();
      });
    }

    iconTiles.forEach((tile) => {
      tile.addEventListener("click", async () => {
        const name = tile.dataset.iconName || "icon";
        const verb = tile.dataset.rfsMotion || "part-arrow-r";
        const svgEl = tile.querySelector("svg");
        if (!svgEl) return;
        activeIconName = name;
        activeMotionVerb = verb;
        renderSpriteSnippet();

        if (activeInteract === "motion") {
          if (window.RFS && window.RFS.triggerIconMotion) window.RFS.triggerIconMotion(tile);
          clearTimeout(statusTimer);
          setStatus("b-beacon", `[${verb}]`, `${name} triggered`);
          return;
        }

        const meta = TONE_META[activeTone] || TONE_META.text;
        let strokeAttr = "currentColor";
        let defs = "";
        let inner = svgEl.innerHTML.replace(/<path[^>]*rfs-p-chk[^>]*\/>/g, "").replace(/<path[^>]*rfs-p-chk[^>]*><\/path>/g, "");
        if (meta.cssVar === "horizon") {
          strokeAttr = "url(#rfs-icon-grad-horizon)";
          defs = '<defs><linearGradient id="rfs-icon-grad-horizon" gradientUnits="userSpaceOnUse" x1="2" y1="22" x2="22" y2="2"><stop offset="0%" stop-color="#74B8E8"/><stop offset="52%" stop-color="#1F547A"/><stop offset="100%" stop-color="#F06E2B"/></linearGradient></defs>';
          inner = inner.replaceAll('fill="currentColor"', 'fill="url(#rfs-icon-grad-horizon)"');
        } else if (meta.cssVar) {
          const resolved = getComputedStyle(root).getPropertyValue(meta.cssVar).trim();
          if (resolved) {
            strokeAttr = resolved;
            inner = inner.replaceAll('fill="currentColor"', `fill="${resolved}"`);
          }
        }
        const markup = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="${strokeAttr}" stroke-width="1.75" stroke-linecap="square" stroke-linejoin="miter">${defs}${inner}</svg>`;
        try {
          await navigator.clipboard.writeText(markup);
          tile.classList.add("is-copied");
          clearTimeout(statusTimer);
          const suffix = activeTone === "text" ? "" : ` (${activeTone})`;
          setStatus("b-ok", "[ok]", `copied ${name}.svg${suffix} · motion: ${verb}`);
          statusTimer = setTimeout(() => {
            tile.classList.remove("is-copied");
            filterIcons();
          }, 1800);
        } catch {
          setStatus("b-fail", "[x]", "clipboard unavailable");
        }
      });
    });

    renderSpriteSnippet();
  }

  // 8b. CLI Truecolor vs. NO_COLOR=1 live toggle
  const cliDemo = document.getElementById("cli-live-demo");
  const cliBadge = document.getElementById("cli-mode-badge");
  const cliMeta = document.getElementById("cli-env-meta");
  const cliModeBtns = $$("[data-cli-mode]");
  if (cliDemo && cliModeBtns.length) {
    cliModeBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const isPlain = btn.dataset.cliMode === "nocolor";
        cliDemo.dataset.nocolor = String(isPlain);
        cliModeBtns.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        if (cliBadge) {
          cliBadge.innerHTML = isPlain
            ? '<span class="k">[pipe]</span> NO_COLOR=1'
            : '<span class="k">[tty]</span> 24-bit color';
          cliBadge.classList.toggle("b-steel", !isPlain);
          cliBadge.classList.toggle("b-beacon", isPlain);
        }
        if (cliMeta) {
          cliMeta.textContent = isPlain ? "stdout: piped / plain" : "stdout: interactive";
        }
      });
    });
  }

  // 8c. Native <progress> determinate stepper
  const stepProgBtn = document.getElementById("step-progress-btn");
  const detProg = document.getElementById("std-prog-det");
  const detVal = document.getElementById("std-prog-val");
  if (stepProgBtn && detProg) {
    stepProgBtn.addEventListener("click", () => {
      const cur = Number(detProg.value) || 0;
      const next = cur >= 100 ? 15 : Math.min(100, cur + 25);
      detProg.value = next;
      if (detVal) detVal.textContent = String(next);
    });
  }

  // 8d. Error recovery feedback
  const retryBtn = document.getElementById("retry-state-btn");
  const retryMsg = document.getElementById("retry-state-msg");
  let retryTimer = 0;
  if (retryBtn && retryMsg) {
    retryBtn.addEventListener("click", () => {
      clearTimeout(retryTimer);
      retryMsg.textContent = "[ok] check queued";
      retryTimer = setTimeout(() => {
        retryMsg.textContent = "";
      }, 2200);
    });
  }

  // ---- 9. §13E Branded Native <dialog> Confirmation Controller & Fallbacks ----
  // Feature-detected Invoker Commands fallback for show-modal / close (zero external CDN)
  if (!("commandForElement" in HTMLButtonElement.prototype)) {
    document.addEventListener("click", (event) => {
      if (event.defaultPrevented) return;
      const btn = event.target.closest('button[command="show-modal"], button[command="close"]');
      if (!btn) return;
      const dlg = document.getElementById(btn.getAttribute("commandfor"));
      if (!(dlg instanceof HTMLDialogElement)) return;
      if (btn.getAttribute("command") === "show-modal" && !dlg.open) dlg.showModal();
      else if (btn.getAttribute("command") === "close" && dlg.open) dlg.close();
    });
  }

  // Detect true discrete display transition support (guards Firefox bug 1882408)
  let supportsDisplayTransition;
  const canTransitionDisplay = () => {
    if (supportsDisplayTransition !== undefined) return supportsDisplayTransition;
    if (!window.CSS?.supports?.("transition-behavior", "allow-discrete") || !document.body) {
      return false;
    }
    const probe = document.createElement("div");
    probe.style.cssText = "transition: display 1s allow-discrete !important; display: block;";
    document.body.appendChild(probe);
    getComputedStyle(probe).display;
    probe.style.display = "none";
    supportsDisplayTransition = getComputedStyle(probe).display === "block";
    probe.remove();
    return supportsDisplayTransition;
  };
  const supportsTopLayerExit = () =>
    Boolean(window.CSS?.supports?.("overlay", "auto") && canTransitionDisplay());

  const closeTopLayer = async (dlg, returnVal) => {
    if (!supportsTopLayerExit()) {
      dlg.setAttribute("data-closing", "");
      const anims = dlg.getAnimations({ subtree: true });
      if (anims.length > 0) {
        await Promise.race([
          Promise.allSettled(anims.map((a) => a.finished)),
          new Promise((r) => setTimeout(r, 1000)),
        ]);
      }
      if (!dlg.hasAttribute("data-closing")) return;
      dlg.removeAttribute("data-closing");
    }
    dlg.close(returnVal);
  };

  // Fallback light-dismiss when closedby="any" is unsupported (press AND release outside rect)
  if (!("closedBy" in HTMLDialogElement.prototype)) {
    const isOutside = (e, dlg) => {
      const r = dlg.getBoundingClientRect();
      return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom;
    };
    $$('dialog[closedby="any"]').forEach((dlg) => {
      let pressedOut = false;
      dlg.addEventListener("pointerdown", (e) => {
        pressedOut = isOutside(e, dlg);
      });
      dlg.addEventListener("pointerup", (e) => {
        if (pressedOut && isOutside(e, dlg)) closeTopLayer(dlg, "");
      });
    });
  }

  const delDialog = document.getElementById("rfs-confirm-delete-demo");
  const delItem = document.getElementById("confirm-demo-item");
  const delTrigger = document.getElementById("confirm-demo-trigger");
  const delReset = document.getElementById("confirm-demo-reset");
  const delStatus = document.getElementById("confirm-demo-status");

  if (delDialog) {
    if (!supportsTopLayerExit()) {
      delDialog.addEventListener("cancel", (e) => {
        e.preventDefault();
        closeTopLayer(delDialog, "");
      });
    }
    delDialog.addEventListener("close", () => {
      const action = delDialog.returnValue;
      // Reset returnValue immediately so stale choices never leak on subsequent Esc dismiss
      delDialog.returnValue = "";
      if (action === "delete") {
        if (delItem) delItem.classList.add("is-deleted");
        if (delTrigger) delTrigger.hidden = true;
        if (delReset) delReset.hidden = false;
        if (delStatus) {
          delStatus.innerHTML =
            '<span class="rfs-badge b-ok"><span class="k">[ok]</span> deleted old-cover.toml (demo)</span>';
        }
      } else {
        if (delStatus) {
          delStatus.innerHTML =
            '<span class="rfs-badge b-steel"><span class="k">[i]</span> canceled — old-cover.toml kept</span>';
        }
      }
    });
  }

  if (delReset) {
    delReset.addEventListener("click", () => {
      if (delItem) delItem.classList.remove("is-deleted");
      if (delTrigger) delTrigger.hidden = false;
      delReset.hidden = true;
      if (delStatus) {
        delStatus.innerHTML =
          '<span class="rfs-badge b-steel"><span class="k">[i]</span> restored — awaiting user action</span>';
      }
    });
  }

  // ---- 10. Tier 2 Primitives: Switch fallback, Toasts, Action Panel, Tooltips & Tabs ----
  // 10a. Native <input type="checkbox" switch> progressive fallback (zero CDN)
  if (!("switch" in HTMLInputElement.prototype)) {
    $$('input[type="checkbox"][switch]').forEach((el) => {
      el.setAttribute("role", "switch");
      el.setAttribute("data-switch-fallback", "");
    });
  }

  // 10b. Non-blocking popover="manual" Semantic Colored Toast Manager (never fires while a modal dialog is open)
  const toastStack = document.getElementById("rfs-toast-stack");
  let lastToastTrigger = null;
  const TOAST_PRESETS = {
    ok:     { cls: "is-ok",   tone: "b-ok",    tag: "[ok]", msg: "Synced listening port 51037 to qBittorrent." },
    warn:   { cls: "is-warn", tone: "b-warn",  tag: "[!]",  msg: "ffmpeg not found on PATH — skipping transcode." },
    fail:   { cls: "is-fail", tone: "b-fail",  tag: "[x]",  msg: "Web UI refused on 127.0.0.1:8080." },
    info:   { cls: "is-info", tone: "b-steel", tag: "[i]",  msg: "Watching Proton VPN port-forward file locally." },
    copy:   { cls: "is-ok",   tone: "b-ok",    tag: "[ok]", msg: "Copied git clone URL to clipboard." },
    export: { cls: "is-info", tone: "b-steel", tag: "[i]",  msg: "Rendered cover-dark.png (1200×560)." },
  };

  const announceToast = (text) => {
    if (typeof document.ariaNotify === "function") {
      try {
        document.ariaNotify(text);
        return;
      } catch {}
    }
    if (globalStatus) {
      let msg = text;
      if (msg === lastAnnouncement) msg += "\u00A0";
      lastAnnouncement = msg;
      globalStatus.textContent = msg;
    }
  };

  const showToast = (kind, triggerEl) => {
    if (!toastStack || document.querySelector("dialog[open]")) return;
    const cfg = TOAST_PRESETS[kind] || TOAST_PRESETS.ok;
    if (triggerEl) lastToastTrigger = triggerEl;

    const item = document.createElement("div");
    item.className = `rfs-toast ${cfg.cls}`;
    item.innerHTML =
      `<span style="display:flex;align-items:center;gap:.55rem;min-width:0">` +
      `<span class="rfs-badge ${cfg.tone}"><span class="k">${cfg.tag}</span></span>` +
      `<span>${cfg.msg}</span></span>` +
      `<button type="button" class="rfs-toast-close" aria-label="Dismiss notification">` +
      `<svg class="rfs-icon rfs-icon-sm" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12"/><path d="M18 6L6 18"/></svg>` +
      `</button>`;

    const dismiss = () => {
      const hadFocus = item.contains(document.activeElement);
      const next = item.nextElementSibling || item.previousElementSibling;
      item.remove();
      if (!toastStack.children.length && toastStack.matches(":popover-open")) {
        toastStack.hidePopover();
      }
      if (hadFocus) {
        const targetBtn = next ? next.querySelector(".rfs-toast-close") : lastToastTrigger;
        if (targetBtn && typeof targetBtn.focus === "function") targetBtn.focus();
      }
    };

    item.querySelector(".rfs-toast-close").addEventListener("click", dismiss);
    toastStack.appendChild(item);
    while (toastStack.children.length > 3) toastStack.firstElementChild.remove();
    if (!toastStack.matches(":popover-open") && typeof toastStack.showPopover === "function") {
      toastStack.showPopover();
    }
    announceToast(`${cfg.tag} ${cfg.msg}`);
  };

  $$("[data-demo-toast]").forEach((btn) => {
    btn.addEventListener("click", () => showToast(btn.dataset.demoToast, btn));
  });

  // 10b2. Interactive KV Metadata <-> Skeleton Loader Toggle
  const skelToggleBtn = document.getElementById("toggle-kv-skeleton");
  const skelCard = document.getElementById("kv-skeleton-card");
  const skelLoaded = document.getElementById("kv-loaded-list");
  const skelRows = document.getElementById("kv-skeleton-list");
  if (skelToggleBtn && skelLoaded && skelRows) {
    skelToggleBtn.addEventListener("click", () => {
      const loading = skelToggleBtn.getAttribute("aria-pressed") !== "true";
      skelToggleBtn.setAttribute("aria-pressed", String(loading));
      skelToggleBtn.textContent = loading ? "Show Loaded Data" : "Preview Skeleton";
      skelLoaded.hidden = loading;
      skelRows.hidden = !loading;
      if (skelCard) skelCard.dataset.loading = String(loading);
    });
  }

  // 10c. Anchored Popover Action Panel items
  const actionPanel = document.getElementById("demo-action-panel");
  if (actionPanel) {
    $$("[data-menu-action]", actionPanel).forEach((item) => {
      item.addEventListener("click", () => {
        const act = item.dataset.menuAction;
        if (actionPanel.matches(":popover-open")) actionPanel.hidePopover();
        if (act === "delete" && delDialog && !delDialog.open) {
          delDialog.showModal();
        } else if (act === "copy" || act === "export") {
          showToast(act, item);
        }
      });
    });
  }

  // 10d. Interest-triggered Tooltip / Toggletip ARIA upfront wiring + Safari hint->auto fallback
  const hintProbe = document.createElement("div");
  if ("popover" in hintProbe) {
    hintProbe.popover = "hint";
    if (hintProbe.popover !== "hint") {
      document.addEventListener(
        "beforetoggle",
        (ev) => {
          const t = ev.target;
          if (
            ev.newState === "open" &&
            t instanceof HTMLElement &&
            t.getAttribute("popover") === "hint" &&
            t.id &&
            document.querySelector(`[popovertarget="${CSS.escape(t.id)}"]`)
          ) {
            t.popover = "auto";
          }
        },
        true
      );
    }
  }
  const ownedHintTriggers = new Map();
  $$("[interestfor]").forEach((trigger) => {
    const id = trigger.getAttribute("interestfor");
    const tip = id ? document.getElementById(id) : null;
    if (!tip || tip.getAttribute("popover") !== "hint") return;
    if (!tip.hasAttribute("role")) tip.setAttribute("role", "tooltip");
    const isToggletip = trigger.getAttribute("popovertarget") === id;
    if (isToggletip) {
      if (!trigger.hasAttribute("aria-expanded")) {
        trigger.setAttribute("aria-expanded", String(tip.matches(":popover-open")));
        ownedHintTriggers.set(trigger, id);
      }
    } else if (!trigger.hasAttribute("aria-describedby")) {
      trigger.setAttribute("aria-describedby", id);
    }
  });
  document.addEventListener(
    "toggle",
    (ev) => {
      const t = ev.target;
      if (!(t instanceof HTMLElement) || !t.id) return;
      const open = ev.newState === "open";
      ownedHintTriggers.forEach((id, trigger) => {
        if (id === t.id) trigger.setAttribute("aria-expanded", String(open));
      });
    },
    true
  );

  // 10e. Native/TUI Drop-in Tabs controller
  const ntTabsRoot = document.getElementById("native-tui-tabs");
  if (ntTabsRoot) {
    const tablist = ntTabsRoot.querySelector('[role="tablist"]');
    const tabs = $$('[role="tab"]', tablist);
    const panels = $$('[role="tabpanel"]', ntTabsRoot);
    const selectNtTab = (targetTab, moveFocus = false) => {
      const idx = tabs.indexOf(targetTab);
      if (idx < 0) return;
      tabs.forEach((tab, i) => {
        const active = i === idx;
        tab.setAttribute("aria-selected", String(active));
        tab.tabIndex = active ? 0 : -1;
      });
      panels.forEach((panel, i) => {
        panel.hidden = i === idx ? false : "until-found";
      });
      if (moveFocus) targetTab.focus();
    };
    tabs.forEach((tab) => tab.addEventListener("click", () => selectNtTab(tab)));
    panels.forEach((panel, i) => panel.addEventListener("beforematch", () => selectNtTab(tabs[i])));
    tablist.addEventListener("keydown", (e) => {
      const cur = tabs.indexOf(document.activeElement);
      if (cur < 0) return;
      let next = -1;
      if (e.key === "ArrowRight") next = (cur + 1) % tabs.length;
      else if (e.key === "ArrowLeft") next = (cur - 1 + tabs.length) % tabs.length;
      else if (e.key === "Home") next = 0;
      else if (e.key === "End") next = tabs.length - 1;
      if (next >= 0) {
        e.preventDefault();
        tabs[next].focus();
      }
    });
  }
})();
