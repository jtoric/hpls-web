<!--
  PageView.vue — Generic static page renderer.

  Reused for all static pages (Rekordi, Poredak, Kontakt, "O nama" sub-pages).
  The page slug is taken from either `route.meta.slug` (for routes with a fixed
  slug like /rekordi) or `route.params.slug` (for dynamic routes).

  Watches the slug source so the content reloads when navigating between
  different static pages without a full component remount.
-->
<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <div v-if="loading" class="text-center py-12 text-gray-500">
      Učitavanje...
    </div>

    <template v-else-if="page">
      <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-8">
        {{ page.title }}
      </h1>

      <!-- Page HTML content (sanitised on the backend) -->
      <div class="prose prose-lg max-w-none" v-html="page.content"></div>

      <!-- Downloadable attachments -->
      <div v-if="page.attachments && page.attachments.length" class="mt-10 border-t pt-6">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">Prilozi</h3>
        <ul class="space-y-2">
          <li v-for="attachment in page.attachments" :key="attachment.id">
            <a
              :href="attachment.file_path"
              target="_blank"
              class="inline-flex items-center text-blue-700 hover:text-blue-900 hover:underline transition"
            >
              <svg class="w-5 h-5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              {{ attachment.original_name }}
            </a>
          </li>
        </ul>
      </div>
    </template>

    <div v-else class="text-center py-12 text-gray-500">
      Stranica nije pronađena.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getPage } from '@/api/index.js'

const route = useRoute()

const page = ref(null)
const loading = ref(true)

/** Fetch the page by slug (from meta or params). */
async function fetchPage() {
  const slug = route.meta.slug || route.params.slug
  if (!slug) return

  loading.value = true
  try {
    const response = await getPage(slug)
    page.value = response.data
  } catch (error) {
    console.error('Greška pri dohvaćanju stranice:', error)
  } finally {
    loading.value = false
  }
}

// Re-fetch when the slug changes (e.g. navigating between "O nama" sub-pages).
watch(
  () => route.meta.slug || route.params.slug,
  () => {
    fetchPage()
  }
)

onMounted(() => {
  fetchPage()
})
</script>
