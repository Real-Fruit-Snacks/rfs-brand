// RFS project page: theme switch (sweeps in from the control), install tabs, copy buttons,
// typing terminals and the Nightshift dot grid that warms around the pointer. The motions are
// the four in BRAND.md §8; with reduced motion every one of them is skipped and the page is the still frame.
(function () {
  var root = document.documentElement;
  var light = matchMedia('(prefers-color-scheme: light)');
  var still = matchMedia('(prefers-reduced-motion: reduce)');
  var fine = matchMedia('(hover: hover) and (pointer: fine)');
  var css = getComputedStyle(root);
  var ms = function (name, d) { return parseFloat(css.getPropertyValue(name)) || d; };
  var $$ = function (sel, el) { return [].slice.call((el || document).querySelectorAll(sel)); };

  // ---- theme ----
  function current() { return root.getAttribute('data-theme') || (light.matches ? 'dayshift' : 'nightshift'); }
  function sync() {
    var night = current() === 'nightshift', next = night ? 'Dayshift' : 'Nightshift';
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = night ? '#0C0D10' : '#F6F5F2';
    $$('.toggle').forEach(function (b) { b.setAttribute('aria-label', 'Nightshift Dayshift: now ' + (night ? 'Nightshift' : 'Dayshift') + ', switch to ' + next); });
    $$('[data-next-theme]').forEach(function (s) { s.textContent = next; });
    // Older pages: a <picture> lockup follows the OS, not data-theme, so drive it here.
    var lock = document.querySelector('[data-lockup]');
    if (lock) {
      var url = 'https://raw.githubusercontent.com/Real-Fruit-Snacks/rfs-brand/main/assets/rfs-lockup-' + (night ? 'dark' : 'light') + '.svg';
      lock.src = url; var src = lock.parentElement.querySelector('source'); if (src) src.srcset = url;
    }
  }
  function flip(from) {
    var next = current() === 'nightshift' ? 'dayshift' : 'nightshift';
    var apply = function () { root.setAttribute('data-theme', next); try { localStorage.setItem('rfs-theme', next); } catch (e) {} sync(); };
    if (!document.startViewTransition || still.matches) return apply();
    var r = from.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2;
    var end = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    document.startViewTransition(apply).ready.then(function () {
      root.animate({ clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + end + 'px at ' + x + 'px ' + y + 'px)'] },
        { duration: ms('--rfs-dur-slow', 600), easing: 'cubic-bezier(.2, .7, .2, 1)', pseudoElement: '::view-transition-new(root)' });
    });
  }
  $$('#theme, [data-theme-toggle]').forEach(function (b) { b.addEventListener('click', function () { flip(b); }); });
  if (light.addEventListener) light.addEventListener('change', sync);
  sync();

  // ---- install tabs (tool pages) and copy buttons ----
  var tabs = $$('.install [role="tab"]');
  tabs.forEach(function (b) {
    b.addEventListener('click', function () {
      tabs.forEach(function (x) { x.setAttribute('aria-selected', String(x === b)); });
      $$('.install .pane').forEach(function (p) { p.toggleAttribute('data-active', p.getAttribute('data-id') === b.getAttribute('data-pane')); });
    });
  });
  var status = document.getElementById('status');
  $$('[data-copy]').forEach(function (b) {
    var label = b.textContent;
    b.addEventListener('click', function () {
      var done = function (ok) {
        b.textContent = ok ? 'Copied' : 'Select it'; b.toggleAttribute('data-done', ok);
        if (status) status.textContent = ok ? 'Copied to the clipboard' : 'Copy failed; select the text instead';
        clearTimeout(b._t); b._t = setTimeout(function () { b.textContent = label; b.removeAttribute('data-done'); }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(b.getAttribute('data-copy')).then(function () { done(true); }, function () { done(false); });
      else done(false);
    });
  });

  // ---- a terminal types its command at --rfs-type-rate, then prints its output 150ms a line ----
  function type(pre, delay) {
    if (still.matches) return;
    var rate = ms('--rfs-type-rate', 45), lines = $$('.ln:not(.end)', pre), end = pre.querySelector('.ln.end');
    var cursor = pre.querySelector('.cursor') || document.createElement('span'), i = 0;
    cursor.className = 'cursor';
    clearTimeout(pre._t);
    lines.forEach(function (ln) {
      var t = ln.querySelector('.t');
      if (t && ln._text == null) { ln._text = t.textContent; ln._rest = document.createElement('span'); ln._rest.className = 'rest'; }
      if (t) { t.textContent = ''; ln._rest.textContent = ln._text; }
      ln.classList.add('wait');
    });
    if (end) end.classList.add('wait');
    pre.classList.remove('booting');
    function step() {
      if (i >= lines.length) { if (end) { end.appendChild(cursor); end.classList.remove('wait'); } void cursor.offsetWidth; cursor.classList.add('blink'); return; }
      var ln = lines[i++], t = ln.querySelector('.t'), n = 0;
      ln.classList.remove('wait');
      if (!t) { pre._t = setTimeout(step, 150); return; }
      t.after(cursor); cursor.after(ln._rest);
      (function tick() {
        t.textContent = ln._text.slice(0, n); ln._rest.textContent = ln._text.slice(n);
        pre._t = n++ < ln._text.length ? setTimeout(tick, rate) : setTimeout(step, 250);
      })();
    }
    pre._t = setTimeout(step, delay || 0);
  }
  // ---- the Ember rule draws in, left to right ----
  function draw(el) { if (still.matches) return; el.classList.remove('go'); void el.offsetWidth; el.classList.add('go'); }
  function play(el, delay) { if (el.hasAttribute('data-type')) type(el, delay); else draw(el); }

  $$('[data-type="load"]').forEach(function (pre) { type(pre, 450); });
  var later = $$('[data-type="view"], [data-draw]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); play(e.target, 200); } });
    }, { threshold: 0.6 });
    later.forEach(function (el) { io.observe(el); });
  }
  $$('[data-replay]').forEach(function (b) {
    b.addEventListener('click', function () { var el = document.getElementById(b.getAttribute('data-replay')); if (el) play(el, 0); });
  });

  // ---- Nightshift: the dot grid warms to Ember around a fine pointer (CSS hides it in Dayshift) ----
  if (fine.matches && !still.matches) {
    $$('[data-warm]').forEach(function (el) {
      var raf = 0, x = 0, y = 0;
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect(); x = e.clientX - r.left; y = e.clientY - r.top;
        if (!raf) raf = requestAnimationFrame(function () { el.style.setProperty('--px', x + 'px'); el.style.setProperty('--py', y + 'px'); el.classList.add('is-warm'); raf = 0; });
      });
      el.addEventListener('pointerleave', function () { el.classList.remove('is-warm'); });
    });
  }
})();
