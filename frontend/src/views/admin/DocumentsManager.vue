<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Dokumenti</h1>
      <router-link to="/admin" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
        &larr; Natrag
      </router-link>
    </div>

    <!-- Upload form -->
    <div class="bg-gray-50 border border-gray-200 rounded-xl p-6 mb-8">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">Dodaj novi dokument</h2>
      <form @submit.prevent="handleUpload" class="flex flex-col sm:flex-row gap-4">
        <input
          v-model="newTitle"
          type="text"
          required
          placeholder="Naziv dokumenta"
          class="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          ref="fileInput"
          type="file"
          required
          accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx"
          class="text-sm"
        />
        <button
          type="submit"
          :disabled="uploading"
          class="bg-blue-700 hover:bg-blue-800 text-white font-semibold px-6 py-2 rounded-lg transition disabled:opacity-50 whitespace-nowrap"
        >
          {{ uploading ? 'Učitavanje...' : 'Dodaj' }}
        </button>
      </form>
      <div v-if="uploadError" class="text-red-600 text-sm mt-2">{{ uploadError }}</div>
      <div v-if="uploadMessage" class="text-green-600 text-sm mt-2">{{ uploadMessage }}</div>
    </div>

    <!-- Documents list -->
    <div v-if="loading" class="text-center py-12 text-gray-500">Učitavanje...</div>

    <div v-else-if="documents.length" class="space-y-3">
      <div
        v-for="doc in documents"
        :key="doc.id"
        class="flex items-center justify-between bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition"
      >
        <div class="min-w-0 flex-1">
          <h3 class="font-medium text-gray-800 truncate">{{ doc.title }}</h3>
          <div class="flex items-center gap-3 text-sm text-gray-400 mt-1">
            <span v-if="doc.file_size">{{ formatFileSize(doc.file_size) }}</span>
            <span>{{ formatDate(doc.uploaded_at) }}</span>
          </div>
        </div>
        <div class="flex items-center gap-3 ml-4">
          <a
            :href="doc.file_path"
            target="_blank"
            class="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            Preuzmi
          </a>
          <button
            @click="handleDelete(doc)"
            class="text-red-600 hover:text-red-800 text-sm font-medium"
          >
            Obriši
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12 text-gray-500">
      Nema dokumenata.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDocuments, uploadDocument, deleteDocument } from '@/api/index.js'

const documents = ref([])
const loading = ref(true)
const uploading = ref(false)
const uploadError = ref('')
const uploadMessage = ref('')
const newTitle = ref('')
const fileInput = ref(null)

function formatFileSize(bytes) {
  if (!bytes) return ''
  const units = ['B', 'KB', 'MB', 'GB']
  let size = bytes
  let i = 0
  while (size >= 1024 && i < units.length - 1) { size /= 1024; i++ }
  return `${size.toFixed(i === 0 ? 0 : 1)} ${units[i]}`
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('hr-HR', {
    day: 'numeric', month: 'long', year: 'numeric',
  })
}

async function fetchDocuments() {
  loading.value = true
  try {
    const response = await getDocuments()
    documents.value = response.data
  } catch (err) {
    console.error('Greška:', err)
  } finally {
    loading.value = false
  }
}

async function handleUpload() {
  const file = fileInput.value?.files[0]
  if (!file || !newTitle.value) return

  uploading.value = true
  uploadError.value = ''
  uploadMessage.value = ''

  try {
    const fd = new FormData()
    fd.append('title', newTitle.value)
    fd.append('file', file)
    await uploadDocument(fd)
    uploadMessage.value = 'Dokument uspješno dodan!'
    newTitle.value = ''
    fileInput.value.value = ''
    await fetchDocuments()
  } catch (err) {
    uploadError.value = 'Greška pri uploadu dokumenta.'
  } finally {
    uploading.value = false
  }
}

async function handleDelete(doc) {
  if (!confirm(`Obrisati dokument "${doc.title}"?`)) return
  try {
    await deleteDocument(doc.id)
    await fetchDocuments()
  } catch (err) {
    console.error('Greška pri brisanju:', err)
  }
}

onMounted(() => fetchDocuments())
</script>
