import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, getMe } from '../api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  async function login(credentials) {
    const response = await apiLogin(credentials)
    token.value = response.data.access_token
    localStorage.setItem('token', token.value)
    await checkAuth()
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

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
