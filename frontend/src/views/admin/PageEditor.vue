<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Uredi stranicu</h1>
      <router-link to="/admin/pages" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
        &larr; Natrag
      </router-link>
    </div>

    <div v-if="loading" class="text-center py-12 text-gray-500">Učitavanje...</div>

    <form v-else @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Title -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Naslov</label>
        <input
          v-model="form.title"
          type="text"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Content editor -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Sadržaj</label>
        <div class="border border-gray-300 rounded-lg overflow-hidden">
          <div class="flex flex-wrap gap-1 p-2 bg-gray-50 border-b border-gray-200">
            <button type="button" @click="editor?.chain().focus().toggleBold().run()"
              :class="{'bg-gray-300': editor?.isActive('bold')}"
              class="px-2 py-1 rounded text-sm font-bold hover:bg-gray-200">B</button>
            <button type="button" @click="editor?.chain().focus().toggleItalic().run()"
              :class="{'bg-gray-300': editor?.isActive('italic')}"
              class="px-2 py-1 rounded text-sm italic hover:bg-gray-200">I</button>
            <button type="button" @click="editor?.chain().focus().toggleHeading({level:2}).run()"
              :class="{'bg-gray-300': editor?.isActive('heading',{level:2})}"
              class="px-2 py-1 rounded text-sm font-semibold hover:bg-gray-200">H2</button>
            <button type="button" @click="editor?.chain().focus().toggleHeading({level:3}).run()"
              :class="{'bg-gray-300': editor?.isActive('heading',{level:3})}"
              class="px-2 py-1 rounded text-sm font-semibold hover:bg-gray-200">H3</button>
            <button type="button" @click="editor?.chain().focus().toggleBulletList().run()"
              :class="{'bg-gray-300': editor?.isActive('bulletList')}"
              class="px-2 py-1 rounded text-sm hover:bg-gray-200">Lista</button>
            <button type="button" @click="addLink"
              class="px-2 py-1 rounded text-sm hover:bg-gray-200">Link</button>
            <button type="button" @click="triggerImage"
              class="px-2 py-1 rounded text-sm hover:bg-gray-200">Slika</button>
            <input ref="imageInput" type="file" accept="image/*" class="hidden" @change="handleImage" />
            <button type="button" @click="triggerFile"
              class="px-2 py-1 rounded text-sm hover:bg-gray-200">Datoteka</button>
            <input ref="fileInput" type="file" class="hidden" @change="handleFile" />
          </div>
          <editor-content :editor="editor" />
        </div>
      </div>

      <!-- Uploaded files info -->
      <div v-if="uploadedFiles.length" class="bg-gray-50 rounded-lg p-4">
        <h3 class="text-sm font-medium text-gray-700 mb-2">Uploadane datoteke</h3>
        <ul class="space-y-1">
          <li v-for="f in uploadedFiles" :key="f.file_path" class="text-sm">
            <a :href="f.file_path" target="_blank" class="text-blue-600 hover:underline">{{ f.original_name }}</a>
          </li>
        </ul>
      </div>

      <div class="flex items-center gap-4 pt-4">
        <button
          type="submit"
          :disabled="saving"
          class="bg-blue-700 hover:bg-blue-800 text-white font-semibold px-6 py-2.5 rounded-lg transition disabled:opacity-50"
        >
          {{ saving ? 'Spremanje...' : 'Spremi' }}
        </button>
      </div>

      <div v-if="message" class="text-green-600 font-medium">{{ message }}</div>
      <div v-if="error" class="text-red-600 font-medium">{{ error }}</div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Link from '@tiptap/extension-link'
import { getPage, updatePage, uploadFile } from '@/api/index.js'

const route = useRoute()

const pageId = Number(route.params.id)
const slug = route.query.slug

const form = reactive({ title: '', content: '' })
const loading = ref(true)
const saving = ref(false)
const message = ref('')
const error = ref('')
const imageInput = ref(null)
const fileInput = ref(null)
const uploadedFiles = ref([])

const editor = useEditor({
  extensions: [
    StarterKit,
    Image.configure({ inline: false }),
    Link.configure({ openOnClick: false }),
  ],
  content: '',
  onUpdate: ({ editor: e }) => {
    form.content = e.getHTML()
  },
})

onMounted(async () => {
  try {
    const response = await getPage(slug)
    const data = response.data
    form.title = data.title
    form.content = data.content
    editor.value?.commands.setContent(data.content || '')
  } catch (err) {
    error.value = 'Greška pri učitavanju stranice.'
  } finally {
    loading.value = false
  }
})

onBeforeUnmount(() => {
  editor.value?.destroy()
})

function triggerImage() { imageInput.value?.click() }
function triggerFile() { fileInput.value?.click() }

async function handleImage(event) {
  const file = event.target.files[0]
  if (!file) return
  try {
    const fd = new FormData()
    fd.append('file', file)
    const response = await uploadFile(fd)
    editor.value?.chain().focus().setImage({ src: response.data.file_path }).run()
    uploadedFiles.value.push(response.data)
  } catch (err) {
    error.value = 'Greška pri uploadu slike.'
  }
}

async function handleFile(event) {
  const file = event.target.files[0]
  if (!file) return
  try {
    const fd = new FormData()
    fd.append('file', file)
    const response = await uploadFile(fd)
    const data = response.data
    // Insert link to file in editor
    editor.value?.chain().focus().setLink({ href: data.file_path }).insertContent(data.original_name).run()
    uploadedFiles.value.push(data)
  } catch (err) {
    error.value = 'Greška pri uploadu datoteke.'
  }
}

function addLink() {
  const url = prompt('Unesite URL:')
  if (url) {
    editor.value?.chain().focus().setLink({ href: url }).run()
  }
}

async function handleSubmit() {
  saving.value = true
  message.value = ''
  error.value = ''
  try {
    await updatePage(pageId, { ...form })
    message.value = 'Stranica uspješno ažurirana!'
  } catch (err) {
    error.value = 'Greška pri spremanju.'
  } finally {
    saving.value = false
  }
}
</script>
