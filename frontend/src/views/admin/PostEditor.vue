<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold text-gray-800">
        {{ isEditing ? 'Uredi objavu' : 'Nova objava' }}
      </h1>
      <router-link to="/admin" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
        &larr; Natrag
      </router-link>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Title -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Naslov</label>
        <input
          v-model="form.title"
          type="text"
          required
          class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Naslov objave"
        />
      </div>

      <!-- Category -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Kategorija</label>
        <select
          v-model="form.category"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="news">Vijest</option>
          <option value="calendar">Kalendar</option>
        </select>
      </div>

      <!-- Excerpt -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Kratki opis</label>
        <textarea
          v-model="form.excerpt"
          rows="2"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Kratki opis za prikaz u listi"
        ></textarea>
      </div>

      <!-- Featured image -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Naslovna slika</label>
        <div class="flex items-center gap-4">
          <input
            type="file"
            accept="image/*"
            @change="handleFeaturedImage"
            class="text-sm"
          />
          <span v-if="uploadingImage" class="text-sm text-gray-500">Učitavanje...</span>
        </div>
        <img
          v-if="form.featured_image"
          :src="form.featured_image"
          class="mt-3 max-h-48 rounded-lg object-cover"
        />
      </div>

      <!-- Content editor -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Sadržaj</label>
        <div class="border border-gray-300 rounded-lg overflow-hidden">
          <!-- Toolbar -->
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
            <button type="button" @click="editor?.chain().focus().toggleOrderedList().run()"
              :class="{'bg-gray-300': editor?.isActive('orderedList')}"
              class="px-2 py-1 rounded text-sm hover:bg-gray-200">1. 2. 3.</button>
            <button type="button" @click="addLink"
              class="px-2 py-1 rounded text-sm hover:bg-gray-200">Link</button>
            <button type="button" @click="triggerEditorImage"
              class="px-2 py-1 rounded text-sm hover:bg-gray-200">Slika</button>
            <input ref="editorImageInput" type="file" accept="image/*" class="hidden" @change="handleEditorImage" />
          </div>
          <editor-content :editor="editor" />
        </div>
      </div>

      <!-- Published -->
      <div class="flex items-center gap-2">
        <input id="published" v-model="form.published" type="checkbox" class="w-4 h-4" />
        <label for="published" class="text-sm font-medium text-gray-700">Objavljeno</label>
      </div>

      <!-- Actions -->
      <div class="flex items-center gap-4 pt-4">
        <button
          type="submit"
          :disabled="saving"
          class="bg-blue-700 hover:bg-blue-800 text-white font-semibold px-6 py-2.5 rounded-lg transition disabled:opacity-50"
        >
          {{ saving ? 'Spremanje...' : 'Spremi' }}
        </button>

        <button
          v-if="isEditing"
          type="button"
          @click="handleDelete"
          class="text-red-600 hover:text-red-800 font-medium text-sm transition"
        >
          Obriši objavu
        </button>
      </div>

      <div v-if="message" class="text-green-600 font-medium">{{ message }}</div>
      <div v-if="error" class="text-red-600 font-medium">{{ error }}</div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Link from '@tiptap/extension-link'
import { getPost, createPost, updatePost, deletePost, uploadFile, getAdminPosts } from '@/api/index.js'

const route = useRoute()
const router = useRouter()

const isEditing = computed(() => !!route.params.id)
const postId = computed(() => route.params.id ? Number(route.params.id) : null)

const form = reactive({
  title: '',
  content: '',
  excerpt: '',
  featured_image: null,
  category: route.query.category || 'news',
  published: true,
})

const saving = ref(false)
const uploadingImage = ref(false)
const message = ref('')
const error = ref('')
const editorImageInput = ref(null)
const postSlug = ref('')

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
  if (isEditing.value) {
    try {
      // Fetch the post by finding it in admin list
      const response = await getAdminPosts({ limit: 100 })
      const post = response.data.items.find(p => p.id === postId.value)
      if (post) {
        postSlug.value = post.slug
        // Now fetch full post with content
        const fullPost = await getPost(post.slug)
        const data = fullPost.data
        form.title = data.title
        form.content = data.content
        form.excerpt = data.excerpt
        form.featured_image = data.featured_image
        form.category = data.category
        form.published = data.published
        editor.value?.commands.setContent(data.content || '')
      }
    } catch (err) {
      error.value = 'Greška pri učitavanju objave.'
    }
  }
})

onBeforeUnmount(() => {
  editor.value?.destroy()
})

async function handleFeaturedImage(event) {
  const file = event.target.files[0]
  if (!file) return
  uploadingImage.value = true
  try {
    const fd = new FormData()
    fd.append('file', file)
    const response = await uploadFile(fd)
    form.featured_image = response.data.file_path
  } catch (err) {
    error.value = 'Greška pri uploadu slike.'
  } finally {
    uploadingImage.value = false
  }
}

function triggerEditorImage() {
  editorImageInput.value?.click()
}

async function handleEditorImage(event) {
  const file = event.target.files[0]
  if (!file) return
  try {
    const fd = new FormData()
    fd.append('file', file)
    const response = await uploadFile(fd)
    editor.value?.chain().focus().setImage({ src: response.data.file_path }).run()
  } catch (err) {
    error.value = 'Greška pri uploadu slike.'
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
    if (isEditing.value) {
      await updatePost(postId.value, { ...form })
      message.value = 'Objava uspješno ažurirana!'
    } else {
      const response = await createPost({ ...form })
      message.value = 'Objava uspješno kreirana!'
      router.replace(`/admin/posts/${response.data.id}/edit`)
    }
  } catch (err) {
    error.value = 'Greška pri spremanju.'
  } finally {
    saving.value = false
  }
}

async function handleDelete() {
  if (!confirm('Jeste li sigurni da želite obrisati ovu objavu?')) return
  try {
    await deletePost(postId.value)
    router.push('/admin')
  } catch (err) {
    error.value = 'Greška pri brisanju.'
  }
}
</script>
