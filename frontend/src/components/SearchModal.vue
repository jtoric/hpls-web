<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="modelValue"
        class="fixed inset-0 z-[110] bg-black/50 flex items-start justify-center pt-[10vh] px-4"
        @click.self="close"
        @keydown.escape="close"
      >
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-lg overflow-hidden">
          <!-- Search input -->
          <div class="flex items-center border-b px-4">
            <svg class="w-5 h-5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              ref="searchInput"
              v-model="query"
              type="text"
              placeholder="Pretraži..."
              class="flex-1 px-3 py-4 text-base outline-none bg-transparent"
              @input="onInput"
            />
            <button
              class="text-gray-400 hover:text-gray-600 p-1"
              @click="close"
              aria-label="Zatvori"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Results -->
          <div class="max-h-[60vh] overflow-y-auto">
            <!-- Loading -->
            <div v-if="loading" class="px-4 py-8 text-center text-gray-400 text-sm">
              Pretraživanje...
            </div>

            <!-- No results -->
            <div v-else-if="searched && !hasResults" class="px-4 py-8 text-center text-gray-400 text-sm">
              Nema rezultata za "{{ query }}"
            </div>

            <!-- Posts -->
            <div v-if="results.posts && results.posts.length">
              <h3 class="px-4 pt-4 pb-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">
                Objave
              </h3>
              <router-link
                v-for="post in results.posts"
                :key="'post-' + post.id"
                :to="postUrl(post)"
                class="block px-4 py-3 hover:bg-gray-50 transition-colors"
                @click="close"
              >
                <div class="text-sm font-medium text-gray-900">{{ post.title }}</div>
                <div v-if="post.excerpt" class="text-xs text-gray-500 mt-0.5 line-clamp-1">
                  {{ post.excerpt }}
                </div>
              </router-link>
            </div>

            <!-- Pages -->
            <div v-if="results.pages && results.pages.length">
              <h3 class="px-4 pt-4 pb-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">
                Stranice
              </h3>
              <router-link
                v-for="page in results.pages"
                :key="'page-' + page.id"
                :to="'/' + page.slug"
                class="block px-4 py-3 hover:bg-gray-50 transition-colors"
                @click="close"
              >
                <div class="text-sm font-medium text-gray-900">{{ page.title }}</div>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { search as searchApi } from '@/api/index.js'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])

const searchInput = ref(null)
const query = ref('')
const results = ref({ posts: [], pages: [] })
const loading = ref(false)
const searched = ref(false)

let debounceTimer = null

const hasResults = computed(() => {
  return (results.value.posts && results.value.posts.length > 0) ||
    (results.value.pages && results.value.pages.length > 0)
})

function onInput() {
  clearTimeout(debounceTimer)
  const q = query.value.trim()

  if (!q) {
    results.value = { posts: [], pages: [] }
    searched.value = false
    loading.value = false
    return
  }

  loading.value = true
  debounceTimer = setTimeout(async () => {
    try {
      const response = await searchApi(q)
      results.value = response.data || { posts: [], pages: [] }
    } catch {
      results.value = { posts: [], pages: [] }
    } finally {
      loading.value = false
      searched.value = true
    }
  }, 300)
}

function postUrl(post) {
  const base = post.category === 'kalendar' ? '/kalendar' : '/novosti'
  return `${base}/${post.slug}`
}

function close() {
  emit('update:modelValue', false)
  query.value = ''
  results.value = { posts: [], pages: [] }
  searched.value = false
}

// Focus input when modal opens
watch(() => props.modelValue, async (open) => {
  if (open) {
    await nextTick()
    searchInput.value?.focus()
  }
})
</script>
