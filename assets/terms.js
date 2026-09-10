// Glossary popovers: hover, focus, or tap a glossary term to read its definition in place.
(function () {
  const G = window.GLOSSARY || {};
  if (!Object.keys(G).length) return;
  let pop = null, current = null, hideTimer = null;
  const isTouch = window.matchMedia("(hover: none)").matches;

  function ensure() {
    if (pop) return pop;
    pop = document.createElement("div");
    pop.className = "termpop";
    pop.setAttribute("role", "tooltip");
    pop.hidden = true;
    pop.addEventListener("mouseenter", () => clearTimeout(hideTimer));
    pop.addEventListener("mouseleave", scheduleHide);
    document.body.appendChild(pop);
    return pop;
  }
  function slugOf(a) {
    const h = a.getAttribute("href") || "";
    const i = h.indexOf("#");
    return i >= 0 ? h.slice(i + 1) : "";
  }
  function show(a) {
    const s = slugOf(a), d = G[s];
    if (!d) return;
    clearTimeout(hideTimer);
    const p = ensure();
    if (current === a && !p.hidden) return;
    current = a;
    p.innerHTML = `<div class="tp-head"><b>${d.term}</b><a class="tp-more" href="/learn/#${s}">Full glossary</a></div><div class="tp-body">${d.html}</div>`;
    p.hidden = false;
    const r = a.getBoundingClientRect();
    const w = Math.min(380, window.innerWidth - 24);
    p.style.width = w + "px";
    let left = Math.max(12, Math.min(r.left, window.innerWidth - w - 12));
    let top = r.bottom + 8;
    p.style.left = left + window.scrollX + "px";
    p.style.top = top + window.scrollY + "px";
    const ph = p.offsetHeight;
    if (top + ph > window.innerHeight - 12 && r.top - ph - 8 > 12) {
      p.style.top = (r.top - ph - 8 + window.scrollY) + "px";
      p.classList.add("above");
    } else p.classList.remove("above");
  }
  function hide() { if (pop) { pop.hidden = true; } current = null; }
  function scheduleHide() { clearTimeout(hideTimer); hideTimer = setTimeout(hide, 180); }

  document.addEventListener("mouseover", (e) => { const a = e.target.closest("a.term"); if (a && !isTouch) show(a); });
  document.addEventListener("mouseout", (e) => { const a = e.target.closest("a.term"); if (a && !isTouch) scheduleHide(); });
  document.addEventListener("focusin", (e) => { const a = e.target.closest("a.term"); if (a) show(a); });
  document.addEventListener("focusout", (e) => { const a = e.target.closest("a.term"); if (a) scheduleHide(); });
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a.term");
    if (a && G[slugOf(a)]) {
      e.preventDefault();
      if (current === a && pop && !pop.hidden) hide(); else show(a);
      return;
    }
    if (pop && !pop.hidden && !e.target.closest(".termpop")) hide();
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") hide(); });
  window.addEventListener("scroll", () => { if (pop && !pop.hidden && current) show(current); }, { passive: true });
})();
