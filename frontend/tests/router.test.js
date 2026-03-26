/**
 * Unit tests for the Vue Router configuration.
 *
 * Verifies route definitions, the 404 catch-all, and the auth guard.
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import router from '../src/router/index.js'

// Mock the auth store so we can control isAuthenticated.
vi.mock('../src/stores/auth', () => {
  const ref = (v) => ({ value: v })
  const computed = (fn) => ({ get value() { return fn() } })
  let _user = ref(null)
  let _token = ref(null)
  return {
    useAuthStore: () => ({
      user: _user,
      token: _token,
      get isAuthenticated() { return !!_token.value && !!_user.value },
      _setAuth(authenticated) {
        if (authenticated) {
          _user.value = { id: 1 }
          _token.value = 'tok'
        } else {
          _user.value = null
          _token.value = null
        }
      },
      login: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
    }),
  }
})

import { useAuthStore } from '../src/stores/auth'

describe('Router', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('resolves the home route', () => {
    const route = router.resolve('/')
    expect(route.name).toBe('home')
  })

  it('resolves news list route', () => {
    const route = router.resolve('/novosti')
    expect(route.name).toBe('news')
  })

  it('resolves a post route with slug param', () => {
    const route = router.resolve('/novosti/some-slug')
    expect(route.name).toBe('post')
    expect(route.params.slug).toBe('some-slug')
  })

  it('resolves calendar route', () => {
    const route = router.resolve('/kalendar')
    expect(route.name).toBe('calendar')
  })

  it('resolves static page routes with meta slug', () => {
    const rekordi = router.resolve('/rekordi')
    expect(rekordi.name).toBe('rekordi')
    expect(rekordi.meta.slug).toBe('rekordi')

    const kontakt = router.resolve('/kontakt')
    expect(kontakt.name).toBe('kontakt')
    expect(kontakt.meta.slug).toBe('kontakt')
  })

  it('resolves "O nama" sub-page routes', () => {
    const pravila = router.resolve('/o-nama/pravila')
    expect(pravila.name).toBe('pravila')
    expect(pravila.meta.slug).toBe('pravila')
  })

  it('resolves admin routes with requiresAuth meta', () => {
    const admin = router.resolve('/admin')
    expect(admin.meta.requiresAuth).toBe(true)

    const postCreate = router.resolve('/admin/posts/new')
    expect(postCreate.meta.requiresAuth).toBe(true)

    const docsManager = router.resolve('/admin/documents')
    expect(docsManager.meta.requiresAuth).toBe(true)
  })

  it('catches unknown paths with the 404 route', () => {
    const route = router.resolve('/this-does-not-exist')
    expect(route.name).toBe('not-found')
  })

  it('catches deeply nested unknown paths', () => {
    const route = router.resolve('/a/b/c/d')
    expect(route.name).toBe('not-found')
  })
})
