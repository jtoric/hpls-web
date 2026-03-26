<template>
  <div class="min-h-[70vh] flex items-center justify-center px-4">
    <div class="w-full max-w-md bg-white border border-gray-200 rounded-xl shadow-sm p-8">
      <h1 class="text-2xl font-bold text-gray-800 text-center mb-6">Prijava</h1>

      <form @submit.prevent="handleLogin" class="space-y-5">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 mb-1">
            Korisničko ime
          </label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            autocomplete="username"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
            Lozinka
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            autocomplete="current-password"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
          />
        </div>

        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="submitting"
          class="w-full bg-blue-700 hover:bg-blue-800 text-white font-semibold py-2.5 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ submitting ? 'Prijava u tijeku...' : 'Prijavi se' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const submitting = ref(false)

async function handleLogin() {
  error.value = ''
  submitting.value = true

  try {
    await authStore.login({ username: username.value, password: password.value })
    router.push('/admin')
  } catch (err) {
    if (err.response && err.response.status === 401) {
      error.value = 'Neispravno korisničko ime ili lozinka.'
    } else {
      error.value = 'Došlo je do greške. Pokušajte ponovo.'
    }
  } finally {
    submitting.value = false
  }
}
</script>
