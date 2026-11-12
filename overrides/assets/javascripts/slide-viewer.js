// Original-slide viewer (decision 2026-11-12, option B: auto mode), client-side only.
//
// Slide-notes pages: a page bar (switch + note + status) sits under the h1. With the switch
// on (the default, unless Save-Data or a stored preference says off), every slide the reader
// has not closed renders ORIGINAL upstream deck pages by itself as the reader scrolls near
// them, with PDF.js, read from raw.githubusercontent.com at the pinned commit. No copy of a
// deck is made: raw sends `access-control-allow-origin: *`, but answers a Range request with
// 501, so ranges and streaming are off and the first page shown downloads the whole deck; one
// document promise per deck is then reused. Two IntersectionObservers track how close each
// slide is to the viewport (NEAR to trigger a render, FAR to give pixels back once it is well
// past). With the switch off, a slide only renders when its own button is clicked (today's
// behaviour before this decision). Tutorial pages: a card near the top with the deck's page
// count and size, linking the slide notes and the original PDF.
// PDF.js is vendored next to this file (assets/pdfjs, Apache-2.0) and loaded on first use.
import { COMMIT, DECKS } from "./slide-decks.js";

const PDFJS = new URL("../pdfjs/pdf.min.mjs", import.meta.url).href;
const WORKER = new URL("../pdfjs/pdf.worker.min.mjs", import.meta.url).href;
const RAW = `https://raw.githubusercontent.com/Lordog/dive-into-llms/${COMMIT}/documents/`;
const BLOB = `https://github.com/Lordog/dive-into-llms/blob/${COMMIT}/documents/`;
const DECK_LINK = /\/Lordog\/dive-into-llms\/blob\/[0-9a-f]{40}\/documents\/(chapter\d+\/[^/?#]+\.pdf)$/;

const LANG = document.documentElement.lang === "en" ? "en" : "vi";
const T = {
  vi: {
    show: (k, size) => `Xem slide gốc ${k} (≈${size})`,
    loading: (size) => `Đang tải PDF gốc (≈${size}). Lần xem đầu tải cả deck, các slide sau dùng lại.`,
    error: "Không tải được slide gốc.",
    openPdf: "Mở PDF gốc",
    alt: (k, title) => (title ? `Slide gốc ${k}: ${title}` : `Slide gốc ${k}`),
    rendered: (k) => `Đã hiện slide gốc ${k}.`,
    cardTitle: "Slide của chương",
    cardMeta: (pages, size) => `${pages} trang · ≈${size} · PDF gốc của tác giả, tiếng Trung`,
    cardMetaEn: (pages, size) => `${pages} trang · ≈${size} · PDF gốc của tác giả, tiếng Anh`,
    notes: "Đọc ghi chú slide",
    original: "PDF gốc",
    switchLabel: "Tự động hiện slide gốc khi cuộn tới",
    switchNote: (size) => `Deck gốc ≈${size}, tải một lần khi slide đầu tiên hiện ra.`,
    barLoading: (size) => `Đang tải PDF gốc (≈${size})…`,
    retry: "Thử lại",
    retrying: "Đang thử lại…",
  },
  en: {
    show: (k, size) => `View original slide ${k} (≈${size})`,
    loading: (size) => `Loading the original PDF (≈${size}). The first view downloads the whole deck; later slides reuse it.`,
    error: "Could not load the original slide.",
    openPdf: "Open the original PDF",
    alt: (k, title) => (title ? `Original slide ${k}: ${title}` : `Original slide ${k}`),
    rendered: (k) => `Original slide ${k} shown.`,
    cardTitle: "Chapter slides",
    cardMeta: (pages, size) => `${pages} pages · ≈${size} · the authors' original PDF, in Chinese`,
    cardMetaEn: (pages, size) => `${pages} pages · ≈${size} · the authors' original PDF, in English`,
    notes: "Read the slide notes",
    original: "Original PDF",
    switchLabel: "Show original slides as I scroll",
    switchNote: (size) => `The original deck is ≈${size}, downloaded once when the first slide appears.`,
    barLoading: (size) => `Loading the original PDF (≈${size})…`,
    retry: "Try again",
    retrying: "Retrying…",
  },
}[LANG];
// Measured with pdftotext (Han characters per page): the chapter 5 and chapter 8 decks have
// none, and the chapter 3 deck has them only on its last page (21 of 21, a course-series page),
// so the card calls those three English. Every other deck has Chinese on 98–100% of its pages.
const ENGLISH_DECKS = new Set(["chapter3/dive_edit_0410.pdf", "chapter5/watermark.pdf", "chapter8/mllms.pdf"]);

function mb(bytes) {
  return `${(bytes / 1e6).toLocaleString(LANG === "en" ? "en-US" : "vi-VN", {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  })} MB`;
}

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  node.append(...children);
  return node;
}

// ---- localStorage preference: "on" | "off", every access guarded -------------------------
function readAutoPref() {
  try {
    const v = localStorage.getItem("dill-slides-auto");
    if (v === "on" || v === "off") return v === "on";
  } catch {
    // ignore: falls through to the Save-Data / default check below
  }
  try {
    if (navigator.connection?.saveData === true) return false;
  } catch {
    // ignore
  }
  return true;
}
function writeAutoPref(on) {
  try {
    localStorage.setItem("dill-slides-auto", on ? "on" : "off");
  } catch {
    // ignore: the switch still works for this load, just not remembered
  }
}

// ---- PDF.js, loaded once, and one document promise per deck ------------------------------
let pdfjs = null;
const documents = new Map();

function loadDeck(key) {
  if (!documents.has(key)) {
    pdfjs ||= import(PDFJS)
      .then((lib) => {
        lib.GlobalWorkerOptions.workerSrc = WORKER;
        return lib;
      })
      .catch((err) => {
        pdfjs = null; // a rejected import must not wedge every later retry
        throw err;
      });
    const promise = pdfjs.then(
      (lib) =>
        lib.getDocument({
          url: RAW + key,
          disableRange: true, // raw.githubusercontent.com answers Range with 501
          disableStream: true,
          isEvalSupported: false,
          verbosity: lib.VerbosityLevel.ERRORS,
        }).promise,
    );
    promise.catch(() => documents.delete(key)); // a later load (click or auto) retries
    documents.set(key, promise);
  }
  return documents.get(key);
}

// ---- Slide-notes pages ------------------------------------------------------------------
function slideTitle(heading) {
  // The first paragraph of the section: its bold text if it has some (the slide's title).
  for (let n = heading.nextElementSibling; n && n.tagName !== "H2"; n = n.nextElementSibling) {
    if (n.tagName !== "P") continue;
    const text = (n.querySelector("strong") || n).textContent.replace(/\s+/g, " ").trim();
    if (text) return text.length > 120 ? `${text.slice(0, 119)}…` : text;
  }
  return "";
}

// A fresh, unrendered placeholder: the aspect-ratio box (not the bordered frame around it)
// carries the ratio, so an empty and a rendered slide are the same height to the pixel.
function makeEmptyPlaceholder(item) {
  const { width, height } = DECKS[item.key];
  const canvas = el("canvas", { "aria-hidden": "true" });
  canvas.width = canvas.height = 0;
  const text = el("div", { class: "textLayer" });
  const box = el("div", { class: "dill-slide__box" }, canvas, text);
  box.style.aspectRatio = `${width} / ${height}`;
  const frame = el("div", { class: "dill-slide__frame dill-slide__frame--empty" }, box);
  item.frame = frame;
  item.canvas = canvas;
  item.text = text;
  item.view.replaceChildren(frame);
}

async function drawSlide(item, page) {
  const { view, k, title, status } = item;
  const { width, height } = DECKS[item.key];
  const base = page.getViewport({ scale: 1 });
  // The view may have been hidden again while loading; its parent keeps the column width.
  const scale = (view.clientWidth || view.parentElement.clientWidth || base.width) / base.width;
  const viewport = page.getViewport({ scale });
  const ratio = Math.min(window.devicePixelRatio || 1, 3);

  const canvas = el("canvas", { role: "img", "aria-label": T.alt(k, title) });
  canvas.width = Math.floor(viewport.width * ratio);
  canvas.height = Math.floor(viewport.height * ratio);
  await page.render({
    canvas,
    canvasContext: canvas.getContext("2d"),
    viewport,
    transform: ratio === 1 ? null : [ratio, 0, 0, ratio, 0, 0],
  }).promise;

  const text = el("div", { class: "textLayer" });
  const box = el("div", { class: "dill-slide__box" }, canvas, text);
  box.style.aspectRatio = `${width} / ${height}`;
  const frame = el("div", { class: "dill-slide__frame" }, box);
  frame.style.setProperty("--total-scale-factor", String(scale));
  view.replaceChildren(frame);
  item.frame = frame;
  item.canvas = canvas;
  item.text = text;
  // Keep the text layer on the canvas when the column width changes after rendering.
  if ("ResizeObserver" in window) {
    item.observer = new ResizeObserver(() => {
      if (frame.clientWidth) frame.style.setProperty("--total-scale-factor", String(frame.clientWidth / base.width));
    });
    item.observer.observe(frame);
  }
  try {
    const lib = await pdfjs; // already loaded by loadDeck
    await new lib.TextLayer({ textContentSource: page.streamTextContent(), container: text, viewport }).render();
  } catch {
    text.remove(); // the picture and its label still stand without selectable text
  }
  // A silent auto render never announces; a click render (manual, or one upgraded by a click
  // while it was in flight) does, unless the view is hidden again by the time it finishes.
  if (item.announce && !view.hidden) status.textContent = T.rendered(k);
  item.announce = false;
}

// A hidden or far-away slide gives back its pixels, text spans and observer. Its frame stays
// at the slide's aspect ratio (now flagged empty) so showing it again re-renders from the
// cached document without moving the page.
function release(item) {
  item.observer?.disconnect();
  item.observer = null;
  item.canvas.width = item.canvas.height = 0;
  item.text.replaceChildren();
  item.frame.classList.add("dill-slide__frame--empty");
  item.state = "released";
}

// One render call used by both a click (which may show today's per-slide error) and an auto
// render (which must tell a deck-load failure from a one-page failure). Throws with a `stage`
// of "deck" or "page" so callers can react differently; `cause` is the underlying error.
async function renderInto(item, ensureDeck) {
  let pdf;
  try {
    pdf = await ensureDeck(item.key);
  } catch (err) {
    throw Object.assign(new Error("deck load failed"), { stage: "deck", cause: err });
  }
  let page;
  try {
    page = await pdf.getPage(item.k);
  } catch (err) {
    throw Object.assign(new Error("page load failed"), { stage: "page", cause: err });
  }
  try {
    await drawSlide(item, page);
  } catch (err) {
    throw Object.assign(new Error("page render failed"), { stage: "page", cause: err });
  } finally {
    page.cleanup(); // the page's operator list and images go; the document stays cached
  }
}

function recomputeFlags(item) {
  // The two observers' own callbacks are the source of truth while a view stays visible, but
  // a view that was `hidden` (display:none) reports not-intersecting regardless of position,
  // so showing it again needs a synchronous re-read against the same margins (100%/300%).
  const r = item.view.getBoundingClientRect();
  const vh = window.innerHeight || document.documentElement.clientHeight;
  item.inNear = r.bottom >= -vh && r.top <= vh * 2;
  item.inFar = r.bottom >= -3 * vh && r.top <= vh * 4;
}

function setUpSlideNotes(article) {
  const link = [...article.querySelectorAll("a[href]")].find((a) => DECK_LINK.test(a.href));
  const key = link && link.href.match(DECK_LINK)[1];
  if (!key || !DECKS[key]) return;
  const size = mb(DECKS[key].bytes);
  const initialAuto = readAutoPref();

  const items = [];
  let pageState; // set once every item exists (needed only if there is at least one slide)

  // ---- render orchestration: at most 2 concurrent auto renders, nearest-to-viewport first,
  // and one enqueue guard every path (NEAR entering, switch on, retry, deck resolved) shares.
  const queue = [];
  let activeRenders = 0;
  const MAX_ACTIVE = 2;

  function canEnqueue(item) {
    return (
      pageState.autoOn &&
      !pageState.deckFailed &&
      !item.userClosed &&
      !item.autoFailed &&
      (item.state === "idle" || item.state === "released") &&
      !item.queued
    );
  }
  function distanceToViewport(item) {
    const r = item.view.getBoundingClientRect();
    return Math.abs((r.top + r.bottom) / 2 - window.innerHeight / 2);
  }
  function enqueue(item) {
    if (!canEnqueue(item)) return;
    item.queued = true;
    queue.push(item);
    pump();
  }
  function pump() {
    while (activeRenders < MAX_ACTIVE && queue.length) {
      queue.sort((a, b) => distanceToViewport(a) - distanceToViewport(b));
      const item = queue.shift();
      item.queued = false;
      // Its turn came: drop it if it is no longer near, or if anything changed since it was
      // queued (closed by the reader, a click render already under way, switch or deck state).
      if (!item.inNear || !canEnqueue(item)) continue;
      activeRenders++;
      runAutoRender(item).finally(() => {
        activeRenders--;
        pump();
      });
    }
  }

  async function ensureDeck(deckKey) {
    const firstLoad = !documents.has(deckKey);
    if (firstLoad) pageState.statusEl.textContent = T.barLoading(pageState.size);
    let pdf;
    try {
      pdf = await loadDeck(deckKey);
    } catch (err) {
      // Never leave the loading line behind: a failed auto render sets the error line next
      // (onDeckFailed), a failed retry keeps it, and a failed click render or a failure while
      // the switch is off leaves the page status empty (the slide shows its own error).
      if (firstLoad) pageState.statusEl.textContent = pageState.deckFailed ? T.error : "";
      throw err; // caught by the caller
    }
    if (pageState.deckFailed) {
      pageState.deckFailed = false;
      clearPageStatus();
      for (const it of pageState.items) if (it.inNear) enqueue(it);
    } else if (firstLoad) {
      clearPageStatus();
    }
    return pdf;
  }

  async function runAutoRender(item) {
    const priorState = item.state; // "idle" or "released" (canEnqueue's own guard)
    item.state = "loading";
    item.view.setAttribute("aria-busy", "true");
    try {
      await renderInto(item, ensureDeck);
      item.state = "done";
      if (item.view.hidden) release(item);
      else if (pageState.autoOn && !item.inFar) release(item); // scrolled far away while it rendered
    } catch (err) {
      item.state = priorState;
      item.announce = false; // a later silent re-render of this slide must stay silent
      if (pageState.autoOn) {
        // a failure that arrives after the switch went off changes nothing (no deck-failed
        // mark, no per-item mark): the reader is back in manual mode already.
        if (err.stage === "deck") onDeckFailed();
        else item.autoFailed = true; // only this page; auto never retries it, a click still can
      }
      console.warn("slide viewer:", err.cause ?? err);
    } finally {
      item.view.removeAttribute("aria-busy");
    }
  }

  function clearPageStatus() {
    if (document.activeElement === pageState.retryBtn) pageState.switchEl.focus();
    pageState.statusEl.textContent = "";
    pageState.retryBtn.hidden = true;
    pageState.retryBtn.removeAttribute("aria-disabled");
    pageState.retryBtn.textContent = T.retry;
  }
  function onDeckFailed() {
    pageState.deckFailed = true;
    for (const it of pageState.items) it.queued = false;
    queue.length = 0;
    pageState.statusEl.textContent = T.error;
    pageState.retryBtn.hidden = false;
    pageState.retryBtn.removeAttribute("aria-disabled");
    pageState.retryBtn.textContent = T.retry;
  }

  function setAuto(on) {
    pageState.autoOn = on;
    pageState.switchEl.setAttribute("aria-checked", String(on));
    writeAutoPref(on);
    if (!on) {
      for (const it of pageState.items) it.queued = false;
      queue.length = 0;
      const active = document.activeElement;
      if (active && (active === pageState.retryBtn || pageState.items.some((it) => it.view.contains(active)))) {
        pageState.switchEl.focus();
      }
      for (const it of pageState.items) {
        it.button.setAttribute("aria-expanded", "false");
        it.view.hidden = true;
        it.status.textContent = "";
        if (it.state === "done") release(it);
        it.userClosed = false;
      }
      clearPageStatus();
      pageState.deckFailed = false; // switch on is always a fresh attempt
    } else {
      for (const it of pageState.items) {
        it.button.setAttribute("aria-expanded", "true");
        it.view.hidden = false;
        if (it.state === "idle") makeEmptyPlaceholder(it);
      }
      // A second pass: a view's position depends on every view above it being shown first.
      for (const it of pageState.items) recomputeFlags(it); // flags were stale while hidden
      for (const it of pageState.items) if (it.inNear) enqueue(it); // no observer callback comes
    }
  }

  for (const heading of article.querySelectorAll("h2[id^='slide-']")) {
    const m = heading.id.match(/^slide-(\d+)$/);
    const k = m && Number(m[1]);
    if (!k || k > DECKS[key].pages) continue;
    const viewId = `dill-slide-${k}`;
    const button = el(
      "button",
      { type: "button", class: "dill-slide__button", "aria-expanded": "false", "aria-controls": viewId },
      T.show(k, size),
    );
    const view = el("div", { id: viewId, class: "dill-slide__view", hidden: "" });
    const status = el("p", { class: "dill-slide__status", role: "status" });
    // state: idle → loading → done; hiding a done slide makes it released, and showing a
    // released slide loads it again; error retries on click. drawSlide/makeEmptyPlaceholder
    // add frame/canvas/text/observer to the item, and release() empties them.
    const item = {
      view,
      button,
      status,
      key,
      k,
      title: slideTitle(heading),
      state: "idle",
      userClosed: false,
      autoFailed: false,
      announce: false,
      inNear: false,
      inFar: false,
      queued: false,
    };
    items.push(item);
    heading.after(el("div", { class: "dill-slide" }, button, status, view));

    button.addEventListener("click", async () => {
      if (button.getAttribute("aria-expanded") === "true" && item.state !== "error") {
        button.setAttribute("aria-expanded", "false");
        view.hidden = true;
        status.textContent = ""; // the live region never describes a slide the reader closed
        if (item.state === "done") release(item); // a slide still loading is released when it finishes
        if (pageState.autoOn) item.userClosed = true;
        return;
      }
      button.setAttribute("aria-expanded", "true");
      view.hidden = false;
      if (pageState.autoOn) item.userClosed = false;
      recomputeFlags(item); // stale while hidden; a finish-time release decision reads it next
      if (item.state === "loading") {
        item.announce = true; // a click on a slide whose silent auto render is in flight
        return; // the render under way finishes into the shown view
      }
      // A slide that already has its frame (a released slide, or an auto-mode placeholder) keeps
      // it while it renders, so the page does not move; otherwise show today's loading line.
      if (!item.frame || !view.contains(item.frame)) {
        view.replaceChildren(el("p", { class: "dill-slide__loading" }, T.loading(size)));
      }
      item.state = "loading";
      item.announce = true; // a click render is always announced, as today
      view.setAttribute("aria-busy", "true");
      status.textContent = "";
      try {
        await renderInto(item, ensureDeck);
        item.state = "done";
        if (view.hidden) release(item); // hidden again while it rendered
        else if (pageState.autoOn && !item.inFar) release(item); // scrolled far while it rendered
      } catch (err) {
        item.state = "error";
        item.announce = false;
        console.warn("slide viewer:", err.cause ?? err);
        view.replaceChildren(
          el(
            "p",
            { class: "dill-slide__error" },
            `${T.error} `,
            el("a", { href: link.href }, T.openPdf),
          ),
        );
        if (!view.hidden) status.textContent = T.error; // a slide closed while loading fails silently
      } finally {
        view.removeAttribute("aria-busy");
      }
    });

    if (initialAuto) {
      button.setAttribute("aria-expanded", "true");
      view.hidden = false;
      makeEmptyPlaceholder(item);
    }
  }

  if (!items.length) return; // en ch5/ch8 stub pages: a deck link but no slide headings

  const switchEl = el(
    "button",
    { type: "button", class: "dill-bar__switch", role: "switch", "aria-checked": String(initialAuto) },
    el("span", { class: "dill-bar__switch-track", "aria-hidden": "true" }, el("span", { class: "dill-bar__switch-thumb" })),
    el("span", { class: "dill-bar__switch-label" }, T.switchLabel),
  );
  const note = el("p", { class: "dill-bar__note" }, T.switchNote(size));
  const statusEl = el("p", { class: "dill-bar__status", role: "status" });
  const retryBtn = el("button", { type: "button", class: "dill-bar__retry", hidden: "" }, T.retry);
  const bar = el(
    "div",
    { class: "dill-bar" },
    el("div", { class: "dill-bar__row" }, switchEl, note),
    el("div", { class: "dill-bar__statusrow" }, statusEl, retryBtn),
  );
  const h1 = article.querySelector("h1");
  if (h1) h1.after(bar);
  else article.prepend(bar);

  pageState = { items, key, size, autoOn: initialAuto, deckFailed: false, switchEl, statusEl, retryBtn };

  switchEl.addEventListener("click", () => setAuto(switchEl.getAttribute("aria-checked") !== "true"));

  retryBtn.addEventListener("click", async () => {
    if (retryBtn.getAttribute("aria-disabled") === "true") return;
    retryBtn.setAttribute("aria-disabled", "true");
    retryBtn.textContent = T.retrying;
    try {
      await ensureDeck(pageState.key); // success clears status/deckFailed and requeues itself
    } catch (err) {
      retryBtn.removeAttribute("aria-disabled");
      retryBtn.textContent = T.retry;
      console.warn("slide viewer:", err);
    }
  });

  // Hash navigation: only on an actual link click (not reload/back-forward, where the browser
  // restores the reader's own position), and only after every placeholder above exists, so the
  // scroll lands on the final layout. This runs before the observers below start, so their
  // first callbacks already see the post-scroll position.
  try {
    const navEntry = performance.getEntriesByType("navigation")[0];
    if (navEntry?.type === "navigate" && location.hash) {
      const target = article.querySelector(`#${CSS.escape(decodeURIComponent(location.hash.slice(1)))}`);
      target?.scrollIntoView();
    }
  } catch {
    // Navigation Timing unavailable: no scroll correction, the browser's own fragment handling applies
  }

  const itemsByView = new Map(items.map((it) => [it.view, it]));
  const nearObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        const item = itemsByView.get(entry.target);
        item.inNear = entry.isIntersecting;
        if (entry.isIntersecting) enqueue(item);
      }
    },
    { root: null, rootMargin: "100% 0px" },
  );
  const farObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        const item = itemsByView.get(entry.target);
        item.inFar = entry.isIntersecting;
        if (!entry.isIntersecting && pageState.autoOn && item.state === "done") release(item);
      }
    },
    { root: null, rootMargin: "300% 0px" },
  );
  for (const item of items) {
    nearObserver.observe(item.view);
    farObserver.observe(item.view);
  }
}

// ---- Tutorial pages ---------------------------------------------------------------------
function setUpTutorial(article, chapter) {
  const key = Object.keys(DECKS).find((name) => name.startsWith(`${chapter}/`));
  if (!key) return;
  const { pages, bytes } = DECKS[key];
  const meta = ENGLISH_DECKS.has(key) ? T.cardMetaEn : T.cardMeta;
  const card = el(
    "aside",
    { class: "dill-deck", "aria-label": T.cardTitle },
    el("p", { class: "dill-deck__title" }, T.cardTitle),
    el("p", { class: "dill-deck__meta" }, meta(pages, mb(bytes))),
    el(
      "p",
      { class: "dill-deck__actions" },
      el("a", { class: "md-button md-button--primary", href: "slides/" }, T.notes),
      el("a", { class: "md-button", href: BLOB + key }, T.original),
    ),
  );
  const h1 = article.querySelector("h1");
  if (h1) h1.after(card);
  else article.prepend(card);
}

// ---- Entry ------------------------------------------------------------------------------
function init() {
  const article = document.querySelector("article.md-content__inner");
  const page = document.querySelector('meta[name="dill-page"]')?.content || "";
  const m = page.match(/(?:^|\/)(chapter\d+)\/(README|slides)\.md$/);
  if (!article || !m) return;
  if (m[2] === "slides") setUpSlideNotes(article);
  else setUpTutorial(article, m[1]);
}

init(); // module scripts run after the document is parsed
