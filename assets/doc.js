// Long-document behaviour: progress bar, table of contents, heading anchors, table labels.
(function () {
  const bar = document.getElementById("progress");
  if (bar) {
    const onScroll = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = max > 0 ? Math.min(100, (window.scrollY / max) * 100) + "%" : "0%";
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  const toc = document.querySelector(".toc");
  const sections = [...document.querySelectorAll(".prose section[id]")];
  if (toc && sections.length) {
    const frag = document.createDocumentFragment();
    for (const s of sections) {
      const h = s.querySelector("h2");
      if (!h) continue;
      const a = document.createElement("a");
      a.href = "#" + s.id;
      a.textContent = h.textContent.replace(/#$/, "").trim();
      frag.appendChild(a);
      if (!h.querySelector("a.anchor")) {
        const link = document.createElement("a");
        link.className = "anchor";
        link.href = "#" + s.id;
        link.textContent = "#";
        link.title = "Link to this section";
        h.appendChild(link);
      }
    }
    toc.appendChild(frag);
    const links = [...toc.querySelectorAll("a")];
    const setActive = (id) => links.forEach((l) => l.classList.toggle("active", l.getAttribute("href") === "#" + id));
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) if (e.isIntersecting) setActive(e.target.id);
      },
      { rootMargin: "-80px 0px -65% 0px" }
    );
    sections.forEach((s) => io.observe(s));
  }

  // Data labels for the mobile card reflow.
  for (const table of document.querySelectorAll(".table-wrap:not(.data-table) table")) {
    const heads = [...table.querySelectorAll("thead th")].map((th) => th.textContent.trim());
    if (!heads.length) continue;
    for (const tr of table.querySelectorAll("tbody tr")) {
      [...tr.children].forEach((td, i) => { if (heads[i]) td.setAttribute("data-label", heads[i]); });
    }
  }
})();
