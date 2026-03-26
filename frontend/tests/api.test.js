/**
 * Unit tests for the API module.
 *
 * Verifies that the axios instance is configured correctly
 * and that each exported function calls the right endpoint.
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import axios from 'axios'

// Mock axios.create to return a spy-enabled instance.
vi.mock('axios', () => {
  const mockInstance = {
    get: vi.fn(() => Promise.resolve({ data: {} })),
    post: vi.fn(() => Promise.resolve({ data: {} })),
    put: vi.fn(() => Promise.resolve({ data: {} })),
    delete: vi.fn(() => Promise.resolve({ data: {} })),
    interceptors: {
      request: { use: vi.fn() },
    },
  }
  return {
    default: {
      create: vi.fn(() => mockInstance),
      _instance: mockInstance,
    },
  }
})

// Import after mocking so the module uses our mock.
const api = axios._instance

describe('API module', () => {
  let apiModule

  beforeEach(async () => {
    vi.clearAllMocks()
    // Dynamic import to get fresh module reference.
    apiModule = await import('../src/api/index.js')
  })

  it('registers a request interceptor', () => {
    expect(api.interceptors.request.use).toHaveBeenCalled()
  })

  it('getPosts calls GET /api/posts with params', async () => {
    await apiModule.getPosts({ category: 'news', page: 1 })
    expect(api.get).toHaveBeenCalledWith('/api/posts', {
      params: { category: 'news', page: 1 },
    })
  })

  it('getPost calls GET /api/posts/:slug', async () => {
    await apiModule.getPost('my-post')
    expect(api.get).toHaveBeenCalledWith('/api/posts/my-post')
  })

  it('createPost calls POST /api/posts', async () => {
    const data = { title: 'Test' }
    await apiModule.createPost(data)
    expect(api.post).toHaveBeenCalledWith('/api/posts', data)
  })

  it('updatePost calls PUT /api/posts/:id', async () => {
    const data = { title: 'Updated' }
    await apiModule.updatePost(5, data)
    expect(api.put).toHaveBeenCalledWith('/api/posts/5', data)
  })

  it('deletePost calls DELETE /api/posts/:id', async () => {
    await apiModule.deletePost(3)
    expect(api.delete).toHaveBeenCalledWith('/api/posts/3')
  })

  it('getPages calls GET /api/pages', async () => {
    await apiModule.getPages()
    expect(api.get).toHaveBeenCalledWith('/api/pages')
  })

  it('getPage calls GET /api/pages/:slug', async () => {
    await apiModule.getPage('kontakt')
    expect(api.get).toHaveBeenCalledWith('/api/pages/kontakt')
  })

  it('getDocuments calls GET /api/documents', async () => {
    await apiModule.getDocuments()
    expect(api.get).toHaveBeenCalledWith('/api/documents')
  })

  it('deleteDocument calls DELETE /api/documents/:id', async () => {
    await apiModule.deleteDocument(7)
    expect(api.delete).toHaveBeenCalledWith('/api/documents/7')
  })

  it('search calls GET /api/search with query', async () => {
    await apiModule.search('powerlifting')
    expect(api.get).toHaveBeenCalledWith('/api/search', {
      params: { q: 'powerlifting' },
    })
  })

  it('login calls POST /api/auth/login', async () => {
    const creds = { username: 'admin', password: 'pass' }
    await apiModule.login(creds)
    expect(api.post).toHaveBeenCalledWith('/api/auth/login', creds)
  })

  it('getMe calls GET /api/auth/me', async () => {
    await apiModule.getMe()
    expect(api.get).toHaveBeenCalledWith('/api/auth/me')
  })
})
