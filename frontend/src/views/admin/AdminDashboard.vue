<!--
  AdminDashboard.vue — Admin home page (route: /admin).

  Provides quick-action cards for the main admin tasks:
  creating news posts, calendar entries, editing static pages,
  and managing uploaded documents. Also includes a logout button.
-->
<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <div class="flex items-center justify-between mb-10">
      <h1 class="text-3xl font-bold text-gray-800">Admin panel</h1>
      <button
        @click="handleLogout"
        class="text-sm text-red-600 hover:text-red-800 font-medium transition"
      >
        Odjava
      </button>
    </div>

    <!-- Quick-action card grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- New news post -->
      <router-link
        to="/admin/posts/new?category=news"
        class="block bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg hover:border-blue-300 transition group"
      >
        <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center mb-4 group-hover:bg-blue-200 transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </div>
        <h3 class="font-semibold text-lg text-gray-800 mb-1">Nova vijest</h3>
        <p class="text-sm text-gray-500">Objavi novu vijest na stranicu</p>
      </router-link>

      <!-- New calendar entry -->
      <router-link
        to="/admin/posts/new?category=calendar"
        class="block bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg hover:border-green-300 transition group"
      >
        <div class="w-12 h-12 bg-green-100 text-green-600 rounded-lg flex items-center justify-center mb-4 group-hover:bg-green-200 transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <h3 class="font-semibold text-lg text-gray-800 mb-1">Novi kalendar</h3>
        <p class="text-sm text-gray-500">Dodaj natjecanje u kalendar</p>
      </router-link>

      <!-- Edit static pages -->
      <router-link
        to="/admin/pages"
        class="block bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg hover:border-purple-300 transition group"
      >
        <div class="w-12 h-12 bg-purple-100 text-purple-600 rounded-lg flex items-center justify-center mb-4 group-hover:bg-purple-200 transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="font-semibold text-lg text-gray-800 mb-1">Uredi stranice</h3>
        <p class="text-sm text-gray-500">Rekordi, Poredak, O nama, Kontakt</p>
      </router-link>

      <!-- Manage documents -->
      <router-link
        to="/admin/documents"
        class="block bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg hover:border-orange-300 transition group"
      >
        <div class="w-12 h-12 bg-orange-100 text-orange-600 rounded-lg flex items-center justify-center mb-4 group-hover:bg-orange-200 transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        <h3 class="font-semibold text-lg text-gray-800 mb-1">Dokumenti</h3>
        <p class="text-sm text-gray-500">Upravljaj PDF dokumentima</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

/** Log out and redirect to the public homepage. */
function handleLogout() {
  authStore.logout()
  router.push('/')
}
</script>
