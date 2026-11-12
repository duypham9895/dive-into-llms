// Original-slide viewer (decision 2026-11-12, option B), client-side only.
//
// Slide-notes pages: a button under each "Slide k" heading renders page k of the ORIGINAL
// upstream deck with PDF.js, read from raw.githubusercontent.com at the pinned commit. No
// copy of a deck is made: raw sends `access-control-allow-origin: *`, but answers a Range
// request with 501, so ranges and streaming are off and the first view downloads the whole
// deck; one document promise per deck is then reused. A slide hidden again gives back its
// canvas memory and is re-rendered from that cached document when shown. Tutorial pages: a
// card near the top with the deck's page count and size, linking the slide notes and the
// original PDF.
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
  },
}[LANG];
// The chapter 5 and chapter 8 decks are in English (their slide notes say so, and pdftotext
// finds no Chinese in them); the card calls every other deck Chinese.
const ENGLISH_DECKS = new Set(["chapter5/watermark.pdf", "chapter8/mllms.pdf"]);

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
    pdfjs ||= import(PDFJS).then((lib) => {
      lib.GlobalWorkerOptions.workerSrc = WORKER;
      return lib;
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
    promise.catch(() => documents.delete(key)); // a later click retries
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

async function renderSlide(item) {
  const pdf = await loadDeck(item.key);
  const page = await pdf.getPage(item.k);
  try {
    await drawSlide(item, page);
  } finally {
    page.cleanup(); // the page's operator list and images go; the document stays cached
  }
}

async function drawSlide(item, page) {
  const { view, k, title, status } = item;
  const base = page.getViewport({ scale: 1 });
  // The view may have been hidden again while loading; its parent keeps the column width.
  const scale = (view.clientWidth || view.parentElement.clientWidth || base.width) / base.width;
  const viewport = page.getViewport({ scale });
  const ratio = Math.min(window.devicePixelRatio || 1, 3);

  const canvas = el("canvas", { role: "img", "aria-label": T.alt(k, title) });
  canvas.width = Math.floor(viewport.width * ratio);
  canvas.height = Math.floor(viewport.height * ratio);
  canvas.style.aspectRatio = `${base.width} / ${base.height}`;
  await page.render({
    canvas,
    canvasContext: canvas.getContext("2d"),
    viewport,
    transform: ratio === 1 ? null : [ratio, 0, 0, ratio, 0, 0],
  }).promise;

  const frame = el("div", { class: "dill-slide__frame" }, canvas);
  const text = el("div", { class: "textLayer" });
  frame.style.setProperty("--total-scale-factor", String(scale));
  frame.append(text);
  view.replaceChildren(frame);
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
  // A view hidden while it rendered is released by the caller, and is not announced.
  if (!view.hidden) status.textContent = T.rendered(k);
}

// A hidden slide gives back its pixels, text spans and observer. Its frame stays in place at
// the slide's aspect ratio, so showing it again re-renders from the cached document.
function release(item) {
  item.observer?.disconnect();
  item.observer = null;
  item.canvas.width = item.canvas.height = 0;
  item.text.replaceChildren();
  item.state = "released";
}

function setUpSlideNotes(article) {
  const link = [...article.querySelectorAll("a[href]")].find((a) => DECK_LINK.test(a.href));
  const key = link && link.href.match(DECK_LINK)[1];
  if (!key || !DECKS[key]) return;
  const size = mb(DECKS[key].bytes);
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
    // released slide loads it again; error retries on click. drawSlide adds canvas, text and
    // observer to the item, and release() empties them.
    const item = { view, key, k, title: slideTitle(heading), status, state: "idle" };
    heading.after(el("div", { class: "dill-slide" }, button, status, view));

    button.addEventListener("click", async () => {
      if (button.getAttribute("aria-expanded") === "true" && item.state !== "error") {
        button.setAttribute("aria-expanded", "false");
        view.hidden = true;
        if (item.state === "done") release(item); // a slide still loading is released when it finishes
        return;
      }
      button.setAttribute("aria-expanded", "true");
      view.hidden = false;
      if (item.state === "loading") return; // the render under way finishes into the shown view
      // A released slide keeps its empty frame while it re-renders; the deck is already cached.
      if (item.state !== "released") view.replaceChildren(el("p", { class: "dill-slide__loading" }, T.loading(size)));
      item.state = "loading";
      view.setAttribute("aria-busy", "true");
      status.textContent = "";
      try {
        await renderSlide(item);
        item.state = "done";
        if (view.hidden) release(item); // hidden again while it rendered
      } catch (err) {
        item.state = "error";
        console.warn("slide viewer:", err);
        view.replaceChildren(
          el(
            "p",
            { class: "dill-slide__error" },
            `${T.error} `,
            el("a", { href: link.href }, T.openPdf),
          ),
        );
        status.textContent = T.error;
      } finally {
        view.removeAttribute("aria-busy");
      }
    });
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
