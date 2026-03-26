<!--
  SearchModal.vue — Full-screen search overlay with debounced API lookup.

  Teleported to the body and opened via v-model from AppHeader.
  Features:
  - Auto-focus on the input when opened
  - 300 ms debounce to avoid excessive API calls
  - Results grouped by "Objave" (posts) and "Stranice" (pages)
  - Debounce timer is cleaned up on unmount to prevent memory leaks
-->
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
          <!-- Search input row -->
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

          <!-- Results area -->
          <div class="max-h-[60vh] overflow-y-auto">
            <!-- Loading indicator -->
            <div v-if="loading" class="px-4 py-8 text-center text-gray-400 text-sm">
              Pretraživanje...
            </div>

            <!-- No results found -->
            <div v-else-if="searched && !hasResults" class="px-4 py-8 text-center text-gray-400 text-sm">
              Nema rezultata za "{{ query }}"
            </div>

            <!-- Posts results -->
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

            <!-- Pages results -->
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
import { ref, computed, watch, nextTick, onBeforeUnmount } from 'vue'
import { search as searchApi } from '@/api/index.js'

const props = defineProps({
  /** Controls modal visibility (v-model). */
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

/** Timer ID for the debounced search — cleared on unmount and on each keystroke. */
let debounceTimer = null

const hasResults = computed(() => {
  return (results.value.posts && results.value.posts.length > 0) ||
    (results.value.pages && results.value.pages.length > 0)
})

/**
 * Called on every keystroke in the search input.
 * Debounces API calls by 300 ms to avoid hammering the backend.
 */
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

/** Build the route path for a post result based on its category. */
function postUrl(post) {
  const base = post.category === 'kalendar' ? '/kalendar' : '/novosti'
  return `${base}/${post.slug}`
}

/** Close the modal and reset search state. */
function close() {
  emit('update:modelValue', false)
  query.value = ''
  results.value = { posts: [], pages: [] }
  searched.value = false
}

// Auto-focus the search input when the modal opens.
watch(() => props.modelValue, async (open) => {
  if (open) {
    await nextTick()
    searchInput.value?.focus()
  }
})

// Clean up the debounce timer to prevent leaked timeouts.
onBeforeUnmount(() => {
  clearTimeout(debounceTimer)
})
</script>
