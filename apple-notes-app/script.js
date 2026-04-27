const STORAGE_KEY = "apple-notes-clone-v1";

const notesListEl = document.getElementById("notes-list");
const newNoteBtn = document.getElementById("new-note");
const searchEl = document.getElementById("search");
const titleEl = document.getElementById("note-title");
const contentEl = document.getElementById("note-content");
const itemTemplate = document.getElementById("note-item-template");

let notes = loadNotes();
let selectedNoteId = notes[0]?.id || null;

if (!notes.length) {
  createNote();
}

render();

newNoteBtn.addEventListener("click", () => {
  createNote();
  render();
});

searchEl.addEventListener("input", render);

titleEl.addEventListener("input", () => updateSelectedNote());
contentEl.addEventListener("input", () => updateSelectedNote());

function createNote() {
  const id = crypto.randomUUID();
  const now = new Date().toISOString();
  const note = {
    id,
    title: "New Note",
    content: "",
    updatedAt: now,
  };
  notes.unshift(note);
  selectedNoteId = id;
  persist();
}

function updateSelectedNote() {
  const note = notes.find((n) => n.id === selectedNoteId);
  if (!note) return;

  note.title = titleEl.value.trim() || "Untitled";
  note.content = contentEl.value;
  note.updatedAt = new Date().toISOString();

  notes.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
  persist();
  render();
}

function removeNote(id) {
  notes = notes.filter((n) => n.id !== id);
  if (!notes.length) {
    createNote();
  }
  if (!notes.some((n) => n.id === selectedNoteId)) {
    selectedNoteId = notes[0].id;
  }
  persist();
  render();
}

function render() {
  const query = searchEl.value.trim().toLowerCase();
  const filtered = notes.filter((n) => {
    const text = `${n.title} ${n.content}`.toLowerCase();
    return text.includes(query);
  });

  notesListEl.innerHTML = "";
  filtered.forEach((note) => {
    const fragment = itemTemplate.content.cloneNode(true);
    const root = fragment.querySelector(".note-item");
    const selectBtn = fragment.querySelector(".note-select");
    const deleteBtn = fragment.querySelector(".delete-note");

    fragment.querySelector(".item-title").textContent = note.title;
    fragment.querySelector(".item-preview").textContent = note.content.slice(0, 70) || "No additional text";
    fragment.querySelector(".item-date").textContent = new Date(note.updatedAt).toLocaleString();

    if (note.id === selectedNoteId) {
      root.classList.add("active");
    }

    selectBtn.addEventListener("click", () => {
      selectedNoteId = note.id;
      render();
    });

    deleteBtn.addEventListener("click", (event) => {
      event.stopPropagation();
      removeNote(note.id);
    });

    notesListEl.appendChild(fragment);
  });

  hydrateEditor();
}

function hydrateEditor() {
  const selected = notes.find((n) => n.id === selectedNoteId);
  if (!selected) {
    titleEl.value = "";
    contentEl.value = "";
    return;
  }

  titleEl.value = selected.title;
  contentEl.value = selected.content;
}

function loadNotes() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed;
  } catch {
    return [];
  }
}

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(notes));
}
