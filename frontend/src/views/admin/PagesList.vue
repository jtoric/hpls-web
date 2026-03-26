<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Stranice</h1>
      <router-link to="/admin" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
        &larr; Natrag
      </router-link>
    </div>

    <div v-if="loading" class="text-center py-12 text-gray-500">Učitavanje...</div>

    <template v-else>
      <!-- Top-level pages -->
      <div class="mb-8">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">Glavne stranice</h2>
        <div class="space-y-2">
          <div
            v-for="page in topPages"
            :key="page.id"
            class="flex items-center justify-between bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition"
          >
            <div>
              <h3 class="font-medium text-gray-800">{{ page.title }}</h3>
              <span class="text-sm text-gray-400">/{{ page.slug }}</span>
            </div>
            <router-link
              :to="`/admin/pages/${page.id}/edit?slug=${page.slug}`"
              class="text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              Uredi
            </router-link>
          </div>
        </div>
      </div>

      <!-- O nama sub-pages -->
      <div>
        <h2 class="text-lg font-semibold text-gray-700 mb-4">O nama - podstranice</h2>
        <div class="space-y-2">
          <div
            v-for="page in subPages"
            :key="page.id"
            class="flex items-center justify-between bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition"
          >
            <div>
              <h3 class="font-medium text-gray-800">{{ page.title }}</h3>
              <span class="text-sm text-gray-400">/o-nama/{{ page.slug }}</span>
            </div>
            <router-link
              :to="`/admin/pages/${page.id}/edit?slug=${page.slug}`"
              class="text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              Uredi
            </router-link>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getPages } from '@/api/index.js'

const pages = ref([])
const loading = ref(true)

const topPages = computed(() => pages.value.filter(p => !p.parent_slug))
const subPages = computed(() => pages.value.filter(p => p.parent_slug === 'o-nama'))

onMounted(async () => {
  try {
    const response = await getPages()
    pages.value = response.data
  } catch (error) {
    console.error('Greška:', error)
  } finally {
    loading.value = false
  }
})
</script>
