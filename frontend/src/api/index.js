/**
 * Axios HTTP client and API function exports.
 *
 * A single axios instance is configured with a request interceptor
 * that attaches the JWT Bearer token from localStorage on every request.
 * All API calls are exported as named functions grouped by resource.
 */
import axios from 'axios'

/** Shared axios instance — baseURL is empty so requests use the Vite dev proxy. */
const api = axios.create({
  baseURL: '',
})

// Attach the JWT token (if present) to every outgoing request.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ---------------------------------------------------------------------------
// Auth
// ---------------------------------------------------------------------------
export const login = (credentials) => api.post('/api/auth/login', credentials)
export const getMe = () => api.get('/api/auth/me')

// ---------------------------------------------------------------------------
// Posts (news & calendar)
// ---------------------------------------------------------------------------
/** List published posts. Accepts `{ category, page, limit }` params. */
export const getPosts = (params) => api.get('/api/posts', { params })
/** List ALL posts (including unpublished) for admin views. */
export const getAdminPosts = (params) => api.get('/api/posts/admin/all', { params })
export const getPost = (slug) => api.get(`/api/posts/${slug}`)
export const createPost = (data) => api.post('/api/posts', data)
export const updatePost = (id, data) => api.put(`/api/posts/${id}`, data)
export const deletePost = (id) => api.delete(`/api/posts/${id}`)

// ---------------------------------------------------------------------------
// Pages (static content)
// ---------------------------------------------------------------------------
export const getPages = () => api.get('/api/pages')
export const getPage = (slug) => api.get(`/api/pages/${slug}`)
export const createPage = (data) => api.post('/api/pages', data)
export const updatePage = (id, data) => api.put(`/api/pages/${id}`, data)

// ---------------------------------------------------------------------------
// Documents (downloadable files)
// ---------------------------------------------------------------------------
export const getDocuments = () => api.get('/api/documents')
export const uploadDocument = (formData) =>
  api.post('/api/documents', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
export const deleteDocument = (id) => api.delete(`/api/documents/${id}`)

// ---------------------------------------------------------------------------
// File upload (used by TipTap editor for inline images)
// ---------------------------------------------------------------------------
export const uploadFile = (formData) =>
  api.post('/api/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

// ---------------------------------------------------------------------------
// Search (cross-model full-text search)
// ---------------------------------------------------------------------------
export const search = (query) => api.get('/api/search', { params: { q: query } })

export default api
