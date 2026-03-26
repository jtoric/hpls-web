/**
 * Unit tests for the Pinia auth store.
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../src/stores/auth'

// Mock the API module so we don't make real HTTP requests.
vi.mock('../src/api', () => ({
  login: vi.fn(),
  getMe: vi.fn(),
}))

import { login as apiLogin, getMe } from '../src/api'

describe('useAuthStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('starts unauthenticated when there is no stored token', () => {
    const store = useAuthStore()
    expect(store.isAuthenticated).toBe(false)
    expect(store.user).toBeNull()
    expect(store.token).toBeNull()
  })

  it('reads existing token from localStorage on init', () => {
    localStorage.setItem('token', 'existing-token')
    const store = useAuthStore()
    expect(store.token).toBe('existing-token')
    // Still not authenticated until checkAuth succeeds
    expect(store.isAuthenticated).toBe(false)
  })

  it('login stores token and fetches user profile', async () => {
    apiLogin.mockResolvedValue({ data: { access_token: 'new-token' } })
    getMe.mockResolvedValue({ data: { id: 1, username: 'admin' } })

    const store = useAuthStore()
    await store.login({ username: 'admin', password: 'pass' })

    expect(store.token).toBe('new-token')
    expect(store.user).toEqual({ id: 1, username: 'admin' })
    expect(store.isAuthenticated).toBe(true)
    expect(localStorage.getItem('token')).toBe('new-token')
  })

  it('logout clears token and user', async () => {
    apiLogin.mockResolvedValue({ data: { access_token: 'tok' } })
    getMe.mockResolvedValue({ data: { id: 1, username: 'admin' } })

    const store = useAuthStore()
    await store.login({ username: 'admin', password: 'pass' })
    store.logout()

    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    expect(localStorage.getItem('token')).toBeNull()
  })

  it('checkAuth logs out when token is invalid', async () => {
    localStorage.setItem('token', 'expired-token')
    getMe.mockRejectedValue(new Error('401'))

    const store = useAuthStore()
    await store.checkAuth()

    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('checkAuth does nothing when there is no token', async () => {
    const store = useAuthStore()
    await store.checkAuth()

    expect(getMe).not.toHaveBeenCalled()
    expect(store.user).toBeNull()
  })

  it('checkAuth sets user when token is valid', async () => {
    localStorage.setItem('token', 'valid-token')
    getMe.mockResolvedValue({ data: { id: 1, username: 'admin' } })

    const store = useAuthStore()
    await store.checkAuth()

    expect(store.user).toEqual({ id: 1, username: 'admin' })
    expect(store.isAuthenticated).toBe(true)
  })
})
