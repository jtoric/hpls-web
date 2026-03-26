<!--
  DocumentsView.vue — Public download page for documents (route: /dokumenti).

  Lists all uploaded documents with their title, file size, upload date,
  and a download button. Uses shared formatters for consistent display.
-->
<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold text-gray-800 mb-8">Dokumenti</h1>

    <div v-if="loading" class="text-center py-12 text-gray-500">
      Učitavanje...
    </div>

    <template v-else>
      <div v-if="documents.length" class="space-y-4">
        <div
          v-for="doc in documents"
          :key="doc.id"
          class="flex items-center justify-between bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition"
        >
          <div class="min-w-0 flex-1">
            <h3 class="text-lg font-semibold text-gray-800 truncate">{{ doc.title }}</h3>
            <div class="flex items-center gap-4 mt-1 text-sm text-gray-500">
              <span v-if="doc.file_size">{{ formatFileSize(doc.file_size) }}</span>
              <span v-if="doc.uploaded_at">{{ formatDate(doc.uploaded_at) }}</span>
            </div>
          </div>

          <a
            :href="doc.file_path"
            target="_blank"
            download
            class="ml-4 flex-shrink-0 inline-flex items-center gap-2 bg-blue-700 hover:bg-blue-800 text-white font-medium px-4 py-2 rounded-lg transition"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Preuzmi
          </a>
        </div>
      </div>

      <div v-else class="text-center py-12 text-gray-500">
        Nema dostupnih dokumenata.
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDocuments } from '@/api/index.js'
import { formatDate, formatFileSize } from '@/utils/formatters'

const documents = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await getDocuments()
    documents.value = response.data
  } catch (error) {
    console.error('Greška pri dohvaćanju dokumenata:', error)
  } finally {
    loading.value = false
  }
})
</script>
