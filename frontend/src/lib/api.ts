import axios from "axios";

const base = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1").replace(/\/$/, "");

export async function getNotes() {
  try {
    const r = await axios.get(`${base}/notes`);
    return r.data;
  } catch (error) {
    console.error("Failed to fetch notes:", error);
    return [];
  }
}

export async function getNote(id: string) {
  try {
    const r = await axios.get(`${base}/notes/${id}`);
    return r.data;
  } catch (error) {
    console.error("Failed to fetch note:", error);
    return null;
  }
}

export async function createNote(payload: any) {
  try {
    const r = await axios.post(`${base}/notes`, payload);
    return r.data;
  } catch (error) {
    console.error("Failed to create note:", error);
    throw error;
  }
}

export async function updateNote(id: string, payload: any) {
  try {
    const r = await axios.put(`${base}/notes/${id}`, payload);
    return r.data;
  } catch (error) {
    console.error("Failed to update note:", error);
    throw error;
  }
}

export async function deleteNote(id: string) {
  try {
    const r = await axios.delete(`${base}/notes/${id}`);
    return r.data;
  } catch (error) {
    console.error("Failed to delete note:", error);
    throw error;
  }
}

export async function searchNotes(q: string) {
  try {
    const r = await axios.get(`${base}/notes/search`, { params: { q } });
    return r.data;
  } catch (error) {
    console.error("Failed to search notes:", error);
    return [];
  }
}

export async function chatWithNotes(message: string) {
  try {
    const r = await axios.post(`${base}/chat`, { message });
    return r.data.reply;
  } catch (error) {
    console.error("Failed to chat with notes:", error);
    throw error;
  }
}
