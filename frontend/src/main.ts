import "./style.css";

type Course = { id: string; name: string };
const API_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");
let courses: Course[] = [];
let query = "";
let noticeTimer = 0;

const icon = (name: string, size = 20) => {
  const paths: Record<string, string> = {
    grid: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    book: '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21z"/><path d="M4 5.5v15M8 7h8M8 11h7"/>',
    search: '<circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 4.5 4.5"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    arrow: '<path d="M7 17 17 7M7 7h10v10"/>',
    close: '<path d="m18 6-12 12M6 6l12 12"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    layers: '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/>',
  };
  return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[name] ?? ""}</svg>`;
};

function shell() {
  document.querySelector<HTMLDivElement>("#app")!.innerHTML = `
    <div class="app-shell">
      <aside class="sidebar">
        <a class="brand" href="#" aria-label="Northstar University home"><span class="brand-mark">n<span>.</span></span><span class="brand-name">northstar<span>UNIVERSITY</span></span></a>
        <div class="side-label">CAMPUS</div>
        <nav aria-label="Main navigation"><a class="nav-item" href="#">${icon("grid")} <span>Overview</span></a><a class="nav-item active" href="#catalog" aria-current="page">${icon("book")} <span>Course catalog</span><span class="nav-dot"></span></a></nav>
        <div class="sidebar-bottom"><div class="term-card"><div class="term-icon">${icon("clock", 17)}</div><div><span class="term-label">CURRENT TERM</span><strong>Fall semester</strong><span class="term-date">September — December</span></div></div><div class="profile"><div class="avatar">NS</div><div class="profile-copy"><strong>Registrar portal</strong><span>Academic services</span></div><button class="more-button" aria-label="Profile options">···</button></div></div>
      </aside>
      <main class="main-content" id="catalog">
        <header class="topbar"><div class="breadcrumb">Academics <span>/</span> <strong>Course catalog</strong></div><div class="topbar-right"><span class="status-indicator"><i></i> Academic year 2025–26</span><div class="top-avatar">NS</div></div></header>
        <section class="page-wrap">
          <div class="eyebrow"><span class="eyebrow-line"></span>ACADEMIC SERVICES</div>
          <div class="page-heading"><div><h1>Course catalog<span class="heading-period">.</span></h1><p class="intro">Explore the courses shaping what comes next.</p></div><button class="primary-button" id="open-form">${icon("plus", 18)} <span>Add a course</span></button></div>
          <div class="metrics" aria-label="Catalog summary"><article class="metric-card"><div class="metric-top"><span class="metric-icon green">${icon("book", 18)}</span><span class="metric-caption">AVAILABLE NOW</span></div><div class="metric-value" id="course-count">—</div><div class="metric-foot">Courses in the catalog</div></article><article class="metric-card"><div class="metric-top"><span class="metric-icon lavender">${icon("layers", 18)}</span><span class="metric-caption">LEARNING PATHS</span></div><div class="metric-value">Explore</div><div class="metric-foot">Find your next area of study</div></article><article class="metric-card term-metric"><div class="metric-top"><span class="metric-icon peach">${icon("clock", 18)}</span><span class="metric-caption">ENROLLMENT</span></div><div class="metric-value">Open</div><div class="metric-foot">Fall semester · 2025–26</div></article></div>
          <div class="catalog-header"><div><div class="section-kicker">THE OFFERINGS</div><h2>All courses <span class="count-pill" id="visible-count">0</span></h2></div><label class="search-box">${icon("search", 18)}<input id="search" type="search" placeholder="Search courses" aria-label="Search courses"><kbd>/</kbd></label></div>
          <div class="course-table-wrap"><table><thead><tr><th>COURSE</th><th>COURSE CODE</th><th class="action-column"></th></tr></thead><tbody id="course-rows"></tbody></table><div id="empty-state" class="empty-state" hidden><div class="empty-art">${icon("book", 26)}</div><h3>No courses to show</h3><p id="empty-copy">Try a different search, or add the first course to your catalog.</p><button class="text-button" id="empty-add">Add a course ${icon("arrow", 15)}</button></div></div>
          <footer class="page-footer"><span>Showing <strong id="footer-count">0</strong> courses</span><span>Northstar University <span class="footer-mark">✳</span> Registrar's office</span></footer>
        </section>
      </main>
    </div>
    <div class="toast" id="toast" role="status" aria-live="polite"></div>
    <div class="modal-backdrop" id="modal" hidden><section class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title"><div class="modal-head"><div><div class="section-kicker">CATALOG MANAGEMENT</div><h2 id="modal-title">Add a course</h2><p>Enter the details for this course offering.</p></div><button class="icon-button" id="close-form" aria-label="Close">${icon("close")}</button></div><form id="course-form"><label>Course name<input name="name" placeholder="e.g. Introduction to Computing" required maxlength="120" /></label><label>Course code<input name="id" placeholder="e.g. CPS 109" required maxlength="20" /></label><div class="form-row"><label>Credit hours<input name="creditHours" type="number" min="0.5" max="12" step="0.5" placeholder="3" required /></label><label>Department ID<input name="department_id" type="number" min="1" step="1" placeholder="e.g. 12" required /></label></div><p class="form-error" id="form-error" role="alert"></p><div class="modal-actions"><button type="button" class="secondary-button" id="cancel-form">Cancel</button><button class="primary-button" type="submit" id="submit-course">Add course ${icon("arrow", 16)}</button></div></form></section></div>`;
}

function renderCourses() {
  const filtered = courses.filter((course) => `${course.name} ${course.id}`.toLowerCase().includes(query.toLowerCase()));
  const rows = document.querySelector<HTMLTableSectionElement>("#course-rows")!;
  rows.innerHTML = filtered.map((course, index) => `<tr><td><div class="course-cell"><span class="course-index">${String(index + 1).padStart(2, "0")}</span><span class="course-name">${escapeHtml(course.name)}</span></div></td><td><span class="code-badge">${escapeHtml(course.id)}</span></td><td class="row-action">${icon("arrow", 17)}</td></tr>`).join("");
  document.querySelector<HTMLElement>("#course-count")!.textContent = String(courses.length).padStart(2, "0");
  document.querySelector<HTMLElement>("#visible-count")!.textContent = String(filtered.length);
  document.querySelector<HTMLElement>("#footer-count")!.textContent = String(filtered.length);
  const empty = document.querySelector<HTMLElement>("#empty-state")!;
  empty.hidden = filtered.length > 0;
  document.querySelector<HTMLElement>("#empty-copy")!.textContent = courses.length && !filtered.length ? "No courses match your search. Try another name or course code." : "Add the first course to start building your catalog.";
  document.querySelectorAll<HTMLTableRowElement>("thead tr").forEach((el) => el.classList.toggle("visually-hidden", filtered.length === 0));
}

function escapeHtml(value: string) {
  return value.replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]!);
}

function toast(message: string, error = false) {
  const element = document.querySelector<HTMLElement>("#toast")!;
  element.textContent = message;
  element.classList.toggle("error", error);
  element.classList.add("show");
  window.clearTimeout(noticeTimer);
  noticeTimer = window.setTimeout(() => element.classList.remove("show"), 3500);
}

async function loadCourses() {
  const rows = document.querySelector<HTMLElement>("#course-rows")!;
  rows.innerHTML = '<tr><td colspan="3" class="loading-cell"><span class="spinner"></span>Loading the course catalog…</td></tr>';
  try {
    const response = await fetch(`${API_URL}/courses`);
    if (!response.ok) throw new Error(`The server returned ${response.status}.`);
    courses = await response.json() as Course[];
    renderCourses();
  } catch {
    courses = [];
    renderCourses();
    document.querySelector<HTMLElement>("#empty-copy")!.textContent = "We couldn't reach the course service. Check that the API is running, then try again.";
    toast("Unable to connect to the course service.", true);
  }
}

function setModal(open: boolean) {
  const modal = document.querySelector<HTMLElement>("#modal")!;
  modal.hidden = !open;
  document.body.classList.toggle("modal-open", open);
  if (open) window.setTimeout(() => document.querySelector<HTMLInputElement>('[name="name"]')?.focus(), 50);
}

function bindEvents() {
  document.querySelector<HTMLInputElement>("#search")!.addEventListener("input", (event) => { query = (event.target as HTMLInputElement).value.trim(); renderCourses(); });
  document.querySelector<HTMLInputElement>("#search")!.addEventListener("keydown", (event) => { if ((event as KeyboardEvent).key === "Escape") { (event.target as HTMLInputElement).value = ""; query = ""; renderCourses(); } });
  document.addEventListener("keydown", (event) => { if (event.key === "/" && !["INPUT", "TEXTAREA"].includes((event.target as HTMLElement).tagName)) { event.preventDefault(); document.querySelector<HTMLInputElement>("#search")!.focus(); } if (event.key === "Escape") setModal(false); });
  document.querySelectorAll("#open-form, #empty-add").forEach((el) => el.addEventListener("click", () => setModal(true)));
  document.querySelectorAll("#close-form, #cancel-form").forEach((el) => el.addEventListener("click", () => setModal(false)));
  document.querySelector<HTMLElement>("#modal")!.addEventListener("click", (event) => { if (event.target === event.currentTarget) setModal(false); });
  document.querySelector<HTMLFormElement>("#course-form")!.addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget as HTMLFormElement;
    const data = new FormData(form);
    const button = document.querySelector<HTMLButtonElement>("#submit-course")!;
    const error = document.querySelector<HTMLElement>("#form-error")!;
    const payload = { name: String(data.get("name")).trim(), id: String(data.get("id")).trim().toUpperCase(), creditHours: Number(data.get("creditHours")), department_id: Number(data.get("department_id")) };
    button.disabled = true;
    button.innerHTML = '<span class="spinner light"></span> Adding…';
    error.textContent = "";
    try {
      const response = await fetch(`${API_URL}/courses`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
      if (!response.ok) {
        const detail = await response.json().catch(() => null) as { detail?: string } | null;
        throw new Error(detail?.detail || `Unable to add course (${response.status}).`);
      }
      form.reset();
      setModal(false);
      toast("Course added to the catalog.");
      await loadCourses();
    } catch (cause) {
      error.textContent = cause instanceof Error ? cause.message : "Something went wrong. Please try again.";
    } finally {
      button.disabled = false;
      button.innerHTML = `Add course ${icon("arrow", 16)}`;
    }
  });
}

shell();
bindEvents();
renderCourses();
void loadCourses();
