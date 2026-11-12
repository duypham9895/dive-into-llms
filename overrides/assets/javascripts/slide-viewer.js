// Original-slide viewer (decision 2026-11-12, option B; Amendment A: no switch), client-side
// only.
//
// Slide-notes pages: unless the reader has Save-Data on, every slide the reader has not closed
// renders ORIGINAL upstream deck pages by itself as the reader scrolls near them, with PDF.js,
// read from raw.githubusercontent.com at the pinned commit. The mode (auto vs. manual) has one
// source of truth: the `dill-auto` class overrides/main.html's inline head script puts on <html>
// from its own, single Save-Data read, before this module ever runs (F1) — this module never
// reads navigator.connection itself, only that class, and additionally falls back to manual mode
// when IntersectionObserver does not exist (no observer, no way to tell "near" from "far"). No
// copy of a deck is made: raw sends `access-control-allow-origin: *`, but answers a Range request
// with 501, so ranges and streaming are off and the first page shown downloads the whole deck;
// one document promise per deck is then reused. Two IntersectionObservers track how close each
// slide is to the viewport (NEAR to trigger a render, FAR to give pixels back once it is well
// past). In manual mode: a slide only renders when its own button is clicked, nothing is
// prefetched, and nothing above the slides says which mode is active.
//
// Loading and error text live INSIDE each slide's own fixed-ratio frame (never as a sibling
// block), so no state change ever moves the page below it: a slide-notes page also reserves
// that space before first paint (see overrides/main.html's inline head script + the
// `html.dill-auto:not(.dill-ready)` rule in slide-viewer.css) so inserting the blocks after
// load does not shift anything either. A deck-wide failure (the deck itself could not load)
// shows a retry button and the "open the original PDF" link on every nearby slide and
// announces once through one hidden, page-level live region; a single page's own failure
// (`item.autoFailed`) shows just the text and the link, since the slide's own per-slide button
// retries it. Tutorial pages: a card near the top with the deck's page count and size, linking
// the slide notes and the original PDF.
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
    loadingMsg: (size) => `Đang tải slide gốc… (file PDF ≈${size}, chỉ tải một lần)`, // F9: "deck" is English jargon
    error: "Không tải được slide gốc.",
    openPdf: "Mở PDF gốc",
    alt: (k, title) => (title ? `Slide gốc ${k}: ${title}` : `Slide gốc ${k}`),
    rendered: (k) => `Đã hiện slide gốc ${k}.`,
    retryLabel: (k) => `Thử lại slide gốc ${k}`,
    cardTitle: "Slide của chương",
    cardMeta: (pages, size) => `${pages} trang · ≈${size} · PDF gốc của tác giả, tiếng Trung`,
    cardMetaEn: (pages, size) => `${pages} trang · ≈${size} · PDF gốc của tác giả, tiếng Anh`,
    notes: "Đọc ghi chú slide",
    original: "PDF gốc",
    retry: "Thử lại",
    retrying: "Đang thử lại…",
  },
  en: {
    show: (k, size) => `View original slide ${k} (≈${size})`,
    loadingMsg: (size) => `Loading the original slide… (deck ≈${size}, downloaded once)`,
    error: "Could not load the original slide.",
    openPdf: "Open the original PDF",
    alt: (k, title) => (title ? `Original slide ${k}: ${title}` : `Original slide ${k}`),
    rendered: (k) => `Original slide ${k} shown.`,
    // Starts with the visible text "Try again" (WCAG 2.5.3 Label in Name, for voice control).
    retryLabel: (k) => `Try again: original slide ${k}`,
    cardTitle: "Chapter slides",
    cardMeta: (pages, size) => `${pages} pages · ≈${size} · the authors' original PDF, in Chinese`,
    cardMetaEn: (pages, size) => `${pages} pages · ≈${size} · the authors' original PDF, in English`,
    notes: "Read the slide notes",
    original: "Original PDF",
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

// Every frame (fresh placeholder, rendered slide, or a released one) is built the same way:
// a box holding the canvas, the PDF.js text layer, and an absolutely positioned message layer
// on top (empty unless a loading or error state is showing). Carrying the aspect ratio on the
// box, not the bordered frame, and reusing the same box for every message state, is what keeps
// a slide's height identical whether it is empty, loading, failed, or rendered (check c).
function buildBox(item, width, height) {
  const canvas = el("canvas", { "aria-hidden": "true" });
  canvas.width = canvas.height = 0;
  const text = el("div", { class: "textLayer", "aria-hidden": "true" });
  const msg = el("div", { class: "dill-slide__msg" });
  const box = el("div", { class: "dill-slide__box" }, canvas, text, msg);
  box.style.aspectRatio = `${width} / ${height}`;
  item.canvas = canvas;
  item.text = text;
  item.msg = msg;
  item.msgKind = null;
  item.retryBtn = null;
  return box;
}

function makeEmptyPlaceholder(item) {
  const { width, height } = DECKS[item.key];
  const box = buildBox(item, width, height);
  const frame = el("div", { class: "dill-slide__frame dill-slide__frame--empty" }, box);
  item.frame = frame;
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

  // F5: aria-hidden — the canvas already carries role=img + a label, and the translated notes
  // below carry the real text; without this, a screen reader reads the clean label and then the
  // raw PDF text runs right after, in content-stream order (not guaranteed reading order).
  const text = el("div", { class: "textLayer", "aria-hidden": "true" });
  const msg = el("div", { class: "dill-slide__msg" });
  const box = el("div", { class: "dill-slide__box" }, canvas, text, msg);
  box.style.aspectRatio = `${width} / ${height}`;
  const frame = el("div", { class: "dill-slide__frame" }, box);
  frame.style.setProperty("--total-scale-factor", String(scale));
  view.replaceChildren(frame);
  item.frame = frame;
  item.canvas = canvas;
  item.text = text;
  item.msg = msg;
  item.msgKind = null;
  item.retryBtn = null;
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
  item.msg.replaceChildren(); // a released slide carries no loading/error text
  item.msgKind = null;
  item.retryBtn = null;
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
  // F1: the ONLY source of truth for the mode is the `dill-auto` class the inline head script
  // (overrides/main.html) set before first paint from its own, single Save-Data read — never a
  // second read here. Exception: without IntersectionObserver, NEAR/FAR can never fire, so auto
  // mode cannot work regardless of the class; fall back to manual mode.
  const auto = "IntersectionObserver" in window && document.documentElement.classList.contains("dill-auto");

  const items = [];
  let pageState; // set once every item exists (needed only if there is at least one slide)

  // ---- render orchestration: at most 2 concurrent auto renders, nearest-to-viewport first,
  // and one enqueue guard every path (NEAR entering, retry, deck resolved) shares.
  const queue = [];
  let activeRenders = 0;
  const MAX_ACTIVE = 2;

  function canEnqueue(item) {
    return (
      pageState.auto &&
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
      // queued (closed by the reader, a click render already under way, deck state).
      if (!item.inNear || !canEnqueue(item)) continue;
      activeRenders++;
      runAutoRender(item).finally(() => {
        activeRenders--;
        pump();
      });
    }
  }

  // ---- in-frame message states: loading, the shared deck-failure (retry + link), and the
  // plain error (text + link only, used for a single page's own failure and for a click
  // failure). Every setter first moves focus off a retry button it is about to discard, so a
  // keyboard user is never dropped onto <body> (A2).
  function moveFocusOffRetry(item) {
    if (item.retryBtn && document.activeElement === item.retryBtn) item.button.focus();
  }
  function clearMsg(item) {
    moveFocusOffRetry(item);
    item.msg.replaceChildren();
    item.msgKind = null;
    item.retryBtn = null;
  }
  function showLoadingMsg(item) {
    moveFocusOffRetry(item);
    item.msg.replaceChildren(el("p", { class: "dill-slide__msgtext" }, T.loadingMsg(size)));
    item.msgKind = "loading";
    item.retryBtn = null;
  }
  function showDeckFailedMsg(item) {
    // Idempotent on purpose: the near/far observers and the reader reopening a slide all call
    // this on every qualifying item, but only idle/released items that are not already showing
    // it (and not a single-page autoFailed item, which keeps its own message) get rebuilt.
    if (item.autoFailed || item.msgKind === "deckFailed") return;
    if (item.state !== "idle" && item.state !== "released") return;
    // F8: several NEAR placeholders can fail together, each with a button visually labelled
    // "Thử lại"/"Try again"; aria-label gives each one a distinct accessible name so a screen
    // reader's button list does not show identical entries.
    const retryBtn = el(
      "button",
      { type: "button", class: "dill-slide__retry", "aria-label": T.retryLabel(item.k) },
      T.retry,
    );
    retryBtn.addEventListener("click", retryDeck);
    item.msg.replaceChildren(
      el("p", { class: "dill-slide__msgtext" }, T.error),
      retryBtn,
      el("a", { class: "dill-slide__msglink", href: link.href }, T.openPdf),
    );
    item.msgKind = "deckFailed";
    item.retryBtn = retryBtn;
  }
  function showStaticErrorMsg(item) {
    // Single-page auto failure (autoFailed) or a click-render failure: text and the "open the
    // original PDF" link only — no retry button, since the per-slide button itself retries.
    moveFocusOffRetry(item);
    item.msg.replaceChildren(
      el("p", { class: "dill-slide__msgtext" }, T.error),
      el("a", { class: "dill-slide__msglink", href: link.href }, T.openPdf),
    );
    item.msgKind = "error";
    item.retryBtn = null;
  }

  function currentRetryButtons() {
    return pageState.items.filter((it) => it.msgKind === "deckFailed").map((it) => it.retryBtn);
  }
  function announceDeckError() {
    // role=status does not re-announce unchanged text, but a reader needs to hear every
    // failure (the first one, and any later failed retry): clear it, then set it on the next
    // frame so each occurrence is a fresh text change.
    pageState.statusEl.textContent = "";
    requestAnimationFrame(() => {
      pageState.statusEl.textContent = T.error;
    });
  }

  async function ensureDeck(deckKey) {
    const pdf = await loadDeck(deckKey); // rejects straight through; renderInto wraps the stage
    if (pageState.deckFailed) {
      pageState.deckFailed = false;
      // A deck-wide retry can take a while (loadDeck re-fetches the whole deck): by the time it
      // resolves, a failed placeholder may have scrolled out of NEAR. Only the still-near ones
      // get the loading text (enqueue, just below, is about to start them); one that scrolled
      // away goes back to a plain empty placeholder instead of being stuck showing "loading"
      // forever with nothing actually in flight.
      for (const it of pageState.items) {
        if (it.msgKind !== "deckFailed") continue;
        if (it.inNear) showLoadingMsg(it);
        else clearMsg(it);
      }
      for (const it of pageState.items) if (it.inNear) enqueue(it);
    }
    return pdf;
  }

  function onDeckFailed() {
    const isNewFailure = !pageState.deckFailed;
    pageState.deckFailed = true;
    for (const it of pageState.items) it.queued = false;
    queue.length = 0; // nothing is queued while the deck is marked failed
    for (const it of pageState.items) if (it.inNear) showDeckFailedMsg(it);
    if (isNewFailure) announceDeckError();
  }

  async function retryDeck() {
    if (pageState.retrying) return;
    pageState.retrying = true;
    for (const btn of currentRetryButtons()) {
      btn.setAttribute("aria-disabled", "true"); // never the `disabled` attribute: it drops focus to body
      btn.textContent = T.retrying;
    }
    try {
      await ensureDeck(pageState.key); // success clears deckFailed and requeues itself above
      pageState.statusEl.textContent = ""; // F4: no stale "could not load" after a successful retry
    } catch (err) {
      for (const btn of currentRetryButtons()) {
        btn.removeAttribute("aria-disabled");
        btn.textContent = T.retry;
      }
      console.warn("slide viewer:", err.cause ?? err);
      announceDeckError();
    } finally {
      pageState.retrying = false;
    }
  }

  async function runAutoRender(item) {
    const priorState = item.state; // "idle" or "released" (canEnqueue's own guard)
    item.state = "loading";
    item.view.setAttribute("aria-busy", "true");
    showLoadingMsg(item); // not announced: auto renders stay silent
    try {
      await renderInto(item, ensureDeck);
      item.state = "done";
      if (item.view.hidden) release(item);
      else if (pageState.auto && !item.inFar) release(item); // scrolled far away while it rendered
    } catch (err) {
      item.state = priorState;
      item.announce = false; // a later silent re-render of this slide must stay silent
      if (err.stage === "deck") onDeckFailed();
      else {
        item.autoFailed = true; // only this page; auto never retries it, a click still can
        showStaticErrorMsg(item);
      }
      console.warn("slide viewer:", err.cause ?? err);
    } finally {
      item.view.removeAttribute("aria-busy");
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
    // add frame/canvas/text/msg/observer to the item, and release() empties them.
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
      msgKind: null,
      retryBtn: null,
    };
    items.push(item);
    heading.after(el("div", { class: "dill-slide" }, button, status, view));

    button.addEventListener("click", async () => {
      if (button.getAttribute("aria-expanded") === "true" && item.state !== "error" && !item.autoFailed) {
        button.setAttribute("aria-expanded", "false");
        view.hidden = true;
        status.textContent = ""; // the live region never describes a slide the reader closed
        if (item.state === "done") release(item); // a slide still loading is released when it finishes
        if (pageState.auto) item.userClosed = true;
        return;
      }
      button.setAttribute("aria-expanded", "true");
      view.hidden = false;
      if (pageState.auto) item.userClosed = false;
      recomputeFlags(item); // stale while hidden; a finish-time release decision reads it next
      if (item.state === "loading") {
        item.announce = true; // a click on a slide whose silent auto render is in flight
        return; // the render under way finishes into the shown view
      }
      if (!item.frame) makeEmptyPlaceholder(item); // manual mode / first open: build the frame now
      // Reopening into a known deck-wide failure shows the same shared message (with its own
      // retry button) instead of guaranteeing another failed attempt; a single-page autoFailed
      // item is unaffected and always gets its own fresh attempt below (today's click path).
      if (pageState.deckFailed && !item.autoFailed) {
        showDeckFailedMsg(item);
        return;
      }
      item.state = "loading";
      item.autoFailed = false; // a click always gets a fresh attempt
      item.announce = true; // a click render is always announced, as today
      view.setAttribute("aria-busy", "true");
      status.textContent = "";
      showLoadingMsg(item);
      try {
        await renderInto(item, ensureDeck);
        item.state = "done";
        if (view.hidden) release(item); // hidden again while it rendered
        else if (pageState.auto && !item.inFar) release(item); // scrolled far while it rendered
      } catch (err) {
        item.state = "error";
        item.announce = false;
        console.warn("slide viewer:", err.cause ?? err);
        showStaticErrorMsg(item); // today's per-slide error, now inside the frame
        if (!view.hidden) status.textContent = T.error; // a slide closed while loading fails silently
      } finally {
        view.removeAttribute("aria-busy");
      }
    });

    if (auto) {
      button.setAttribute("aria-expanded", "true");
      view.hidden = false;
      makeEmptyPlaceholder(item);
    }
  }

  if (!items.length) return; // en ch5/ch8 stub pages: a deck link but no slide headings

  // The one page-level live region for a deck-wide failure (visually hidden, same technique as
  // the per-slide status above). Nothing on the page is visible for this beyond the per-slide
  // messages, so it is the only clue a screen reader gets that the deck itself failed.
  const statusEl = el("p", { class: "dill-slide__status", role: "status" });
  const h1 = article.querySelector("h1");
  if (h1) h1.after(statusEl);
  else article.prepend(statusEl);

  pageState = { items, key, size, auto, deckFailed: false, retrying: false, statusEl };

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
        if (!entry.isIntersecting) continue;
        if (pageState.deckFailed) showDeckFailedMsg(item); // nothing is queued while failed
        else enqueue(item);
      }
    },
    { root: null, rootMargin: "100% 0px" },
  );
  const farObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        const item = itemsByView.get(entry.target);
        item.inFar = entry.isIntersecting;
        if (!entry.isIntersecting && pageState.auto && item.state === "done") release(item);
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
  if (m[2] === "slides") {
    // F3: try/finally so a throw inside setUpSlideNotes still clears the CSS reserve — never
    // leave `html.dill-auto:not(.dill-ready)` matching forever. (A second safety net lives in
    // overrides/main.html's own `load` listener, for when this module never runs at all: a 404,
    // a syntax error, or no ES module support.)
    try {
      setUpSlideNotes(article);
    } finally {
      // CLS fix: swap the CSS reserve (overrides/main.html's inline head script adds `dill-auto`
      // to <html> before this module runs) for the real blocks in the same task, so the browser
      // never has a frame with the reserve gone and the blocks not yet in.
      document.documentElement.classList.add("dill-ready");
    }
  } else setUpTutorial(article, m[1]);
}

init(); // module scripts run after the document is parsed
