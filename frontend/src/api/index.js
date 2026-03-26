import axios from 'axios'

const api = axios.create({
  baseURL: '',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth
export const login = (credentials) => api.post('/api/auth/login', credentials)
export const getMe = () => api.get('/api/auth/me')

// Posts
export const getPosts = (params) => api.get('/api/posts', { params })
export const getAdminPosts = (params) => api.get('/api/posts/admin/all', { params })
export const getPost = (slug) => api.get(`/api/posts/${slug}`)
export const createPost = (data) => api.post('/api/posts', data)
export const updatePost = (id, data) => api.put(`/api/posts/${id}`, data)
export const deletePost = (id) => api.delete(`/api/posts/${id}`)

// Pages
export const getPages = () => api.get('/api/pages')
export const getPage = (slug) => api.get(`/api/pages/${slug}`)
export const createPage = (data) => api.post('/api/pages', data)
export const updatePage = (id, data) => api.put(`/api/pages/${id}`, data)

// Documents
export const getDocuments = () => api.get('/api/documents')
export const uploadDocument = (formData) =>
  api.post('/api/documents', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
export const deleteDocument = (id) => api.delete(`/api/documents/${id}`)

// File upload
export const uploadFile = (formData) =>
  api.post('/api/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

// Search
export const search = (query) => api.get('/api/search', { params: { q: query } })

export default api
