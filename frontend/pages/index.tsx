import React, { useEffect, useState } from "react";
import { getNotes, createNote, updateNote, deleteNote, searchNotes, chatWithNotes } from "../src/lib/api";

type Note = {
  id: string;
  title: string;
  content?: string;
  tags?: string[];
  created_at: string;
  updated_at: string;
};

type DraftNote = {
  title: string;
  content: string;
  tags: string;
};

const emptyDraft: DraftNote = {
  title: "",
  content: "",
  tags: "",
};

export default function Home() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [selected, setSelected] = useState<Note | null>(null);
  const [draft, setDraft] = useState<DraftNote>(emptyDraft);
  const [search, setSearch] = useState("");
  const [chatInput, setChatInput] = useState("");
  const [chatReply, setChatReply] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [chatWarning, setChatWarning] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void fetchNotes();
  }, []);

  async function fetchNotes() {
    try {
      const data = await getNotes();
      setNotes(data);
      setError(null);
      if (data.length && !selected) setSelected(data[0]);
    } catch (err) {
      setError("Could not reach the backend. Please start the API server on port 8000.");
      setNotes([]);
      setSelected(null);
    }
  }

  async function handleCreateNote() {
    try {
      const payload = {
        title: draft.title.trim() || "New note",
        content: draft.content.trim(),
        tags: draft.tags
          .split(",")
          .map((tag) => tag.trim())
          .filter(Boolean),
      };

      const created = await createNote(payload);
      setDraft(emptyDraft);
      await fetchNotes();
      setSelected(created);
      setError(null);
    } catch (err) {
      setError("Unable to create a note. Check that the backend is running.");
    }
  }

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    try {
      const results = search ? await searchNotes(search) : await getNotes();
      setNotes(results);
      setError(null);
      setSelected(results[0] ?? null);
    } catch (err) {
      setError("Unable to search notes. Check that the backend is running.");
    }
  }

  async function handleSave(note: Note) {
    try {
      await updateNote(note.id, note);
      await fetchNotes();
      setError(null);
    } catch (err) {
      setError("Unable to save the note. Check that the backend is running.");
    }
  }

  async function handleDelete(id: string) {
    if (!confirm("Delete note?")) return;
    try {
      await deleteNote(id);
      await fetchNotes();
      setSelected(null);
      setError(null);
    } catch (err) {
      setError("Unable to delete the note. Check that the backend is running.");
    }
  }

  async function handleChatSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!chatInput.trim()) {
      setChatWarning("Please write a question before asking your notes.");
      setError(null);
      return;
    }

    setChatWarning(null);

    try {
      setChatLoading(true);
      setError(null);
      const reply = await chatWithNotes(chatInput.trim());
      setChatReply(reply);
      setChatInput("");
    } catch (err) {
      setError("Unable to chat with your notes right now.");
    } finally {
      setChatLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_#fdfcff,_#f8f4ff_40%,_#eef6ff)] p-4 text-slate-700 sm:p-6 lg:p-8">
      <div className="mx-auto max-w-7xl overflow-hidden rounded-[32px] border border-violet-100 bg-white/80 shadow-[0_24px_80px_rgba(134,110,182,0.16)] backdrop-blur-sm">
        <header className="flex items-center justify-between border-b border-slate-200/80 px-5 py-4 sm:px-6">
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.28em] text-violet-500">Notes</p>
            <h1 className="text-3xl font-semibold tracking-[-0.04em] text-slate-800">Context</h1>
          </div>
          <div className="rounded-full bg-violet-50 px-3 py-1.5 text-sm font-medium text-violet-700 shadow-sm">
            {notes.length} saved
          </div>
        </header>

        <div className="flex min-h-[80vh] flex-col lg:flex-row">
          <aside className="w-full border-b border-slate-200/80 bg-[#fbf9ff] p-4 lg:w-[420px] lg:border-b-0 lg:border-r">
            <div className="rounded-[28px] border border-violet-100 bg-white p-4 shadow-[0_12px_25px_rgba(168,138,220,0.08)]">
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-slate-800">New note</h2>
                <span className="rounded-full bg-emerald-50 px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.2em] text-emerald-600">
                  Draft
                </span>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="mb-2 block text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-400">Title</label>
                  <input
                    value={draft.title}
                    onChange={(e) => setDraft((prev) => ({ ...prev, title: e.target.value }))}
                    placeholder="Untitled note"
                    className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-violet-300 focus:bg-white focus:ring-4 focus:ring-violet-100"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-400">Tags</label>
                  <input
                    value={draft.tags}
                    onChange={(e) => setDraft((prev) => ({ ...prev, tags: e.target.value }))}
                    placeholder="ideas, work, notes"
                    className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-violet-300 focus:bg-white focus:ring-4 focus:ring-violet-100"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-400">Content</label>
                  <textarea
                    value={draft.content}
                    onChange={(e) => setDraft((prev) => ({ ...prev, content: e.target.value }))}
                    rows={8}
                    placeholder="Write your note..."
                    className="w-full resize-none rounded-2xl border border-slate-200 bg-slate-50 px-3 py-3 text-sm leading-6 text-slate-700 outline-none transition focus:border-violet-300 focus:bg-white focus:ring-4 focus:ring-violet-100"
                  />
                </div>

                <button
                  type="button"
                  onClick={handleCreateNote}
                  className="w-full rounded-2xl bg-gradient-to-r from-violet-500 via-fuchsia-500 to-pink-500 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-200 transition hover:translate-y-[-1px]"
                >
                  Save note
                </button>
              </div>
            </div>
          </aside>

          <main className="flex-1 bg-[linear-gradient(180deg,#fffdfd_0%,#f8f7ff_100%)] p-4 sm:p-5 lg:p-6">
            <div className="mb-5 rounded-[24px] border border-slate-200 bg-white p-3 shadow-sm">
              <div className="flex items-center justify-between gap-2">
                <h2 className="text-lg font-semibold text-slate-800">All notes</h2>
                <div className="rounded-full bg-slate-100 px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                  {notes.length ? `${notes.length} items` : "Empty"}
                </div>
              </div>

              <form onSubmit={handleSearch} className="mt-3 flex gap-2">
                <input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search notes"
                  className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-violet-300 focus:bg-white focus:ring-4 focus:ring-violet-100"
                />
                <button
                  type="submit"
                  className="rounded-2xl bg-slate-800 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-slate-700"
                >
                  Search
                </button>
              </form>
            </div>

            {error && <div className="mb-4 rounded-2xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">{error}</div>}

            <div className="mb-6 rounded-[28px] border border-violet-100 bg-white p-4 shadow-[0_12px_30px_rgba(168,138,220,0.08)]">
              <div className="mb-3 flex items-center justify-between">
                <h3 className="text-lg font-semibold text-slate-800">Ask Context</h3>
                <span className="rounded-full bg-violet-50 px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.2em] text-violet-700">
                  AI
                </span>
              </div>

              <form onSubmit={handleChatSubmit} className="space-y-3">
                <textarea
                  value={chatInput}
                  onChange={(e) => {
                    setChatInput(e.target.value);
                    if (chatWarning) setChatWarning(null);
                  }}
                  rows={3}
                  placeholder="Ask about your notes, like: What did I write about Kubernetes?"
                  className="w-full resize-none rounded-2xl border border-slate-200 bg-slate-50 px-3 py-3 text-sm text-slate-700 outline-none transition focus:border-violet-300 focus:bg-white focus:ring-4 focus:ring-violet-100"
                />

                <div className="flex items-center justify-between gap-3">
                  <button
                    type="submit"
                    disabled={chatLoading}
                    className="rounded-full bg-gradient-to-r from-violet-500 to-fuchsia-500 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-violet-200 transition hover:translate-y-[-1px] disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {chatLoading ? "Thinking..." : "Ask notes"}
                  </button>

                  {chatWarning && (
                    <div
                      aria-live="polite"
                      className="flex-1 text-right text-xs font-medium text-amber-700"
                    >
                      {chatWarning}
                    </div>
                  )}
                </div>
              </form>

              {chatReply && (
                <div className="mt-4 rounded-2xl border border-slate-200 bg-slate-50 p-3 text-sm leading-6 text-slate-700">
                  {chatReply}
                </div>
              )}
            </div>

            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {notes.length === 0 && !error ? (
                <div className="col-span-full rounded-[24px] border border-dashed border-violet-200 bg-violet-50/60 px-4 py-12 text-center text-sm text-slate-500">
                  No notes yet. Start by adding one on the left.
                </div>
              ) : (
                notes.map((note) => (
                  <button
                    key={note.id}
                    type="button"
                    onClick={() => setSelected(note)}
                    className={`rounded-[24px] border p-4 text-left shadow-sm transition ${
                      selected?.id === note.id
                        ? "border-violet-200 bg-gradient-to-r from-violet-50 to-fuchsia-50 shadow-violet-100"
                        : "border-slate-200 bg-white hover:border-violet-200 hover:shadow-md"
                    }`}
                  >
                    <div className="mb-3 flex items-start justify-between gap-3">
                      <div>
                        <div className="text-[10px] font-semibold uppercase tracking-[0.2em] text-slate-400">Note</div>
                        <h3 className="mt-1 text-lg font-semibold text-slate-800">{note.title || "Untitled"}</h3>
                      </div>
                      <span className="rounded-full bg-slate-100 px-2 py-1 text-[10px] font-medium uppercase tracking-[0.14em] text-slate-500">
                        open
                      </span>
                    </div>

                    <div className="mb-4 min-h-[110px] rounded-2xl bg-[#fffdfd] p-3 text-sm leading-6 text-slate-600">
                      {note.content || "No content yet."}
                    </div>

                    <div className="mb-4 flex flex-wrap gap-2">
                      {(note.tags || []).length ? (
                        (note.tags || []).map((tag) => (
                          <span key={tag} className="rounded-full bg-violet-50 px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.14em] text-violet-700">
                            {tag}
                          </span>
                        ))
                      ) : (
                        <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.14em] text-slate-500">
                          no tags
                        </span>
                      )}
                    </div>

                    <div className="flex items-center justify-between border-t border-slate-200 pt-3">
                      <span className="text-[11px] text-slate-400">{new Date(note.updated_at).toLocaleString()}</span>
                    </div>
                  </button>
                ))
              )}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
