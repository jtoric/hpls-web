/**
 * Pinia auth store — manages JWT authentication state.
 *
 * The token is persisted in localStorage so the session survives
 * page reloads. On app startup, `checkAuth()` is called to validate
 * the stored token against the `/api/auth/me` endpoint; if the token
 * is expired or invalid the user is silently logged out.
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, getMe } from '../api'

export const useAuthStore = defineStore('auth', () => {
  /** Currently authenticated user object (or null). */
  const user = ref(null)

  /** JWT access token read from localStorage on init. */
  const token = ref(localStorage.getItem('token') || null)

  /** True when both a token and a validated user object exist. */
  const isAuthenticated = computed(() => !!token.value && !!user.value)

  /**
   * Log in with username + password.
   * Stores the returned token and fetches the user profile.
   */
  async function login(credentials) {
    const response = await apiLogin(credentials)
    token.value = response.data.access_token
    localStorage.setItem('token', token.value)
    await checkAuth()
  }

  /** Clear all auth state and remove the persisted token. */
  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  /**
   * Validate the current token by calling `/api/auth/me`.
   * If the call fails (expired/invalid token) the user is logged out.
   */
  async function checkAuth() {
    if (!token.value) return
    try {
      const response = await getMe()
      user.value = response.data
    } catch {
      logout()
    }
  }

  return { user, token, isAuthenticated, login, logout, checkAuth }
})
