<template>
  <div class="max-w-6xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold text-gray-800 mb-8">Kalendar natjecanja</h1>

    <div v-if="loading" class="text-center py-12 text-gray-500">
      Učitavanje...
    </div>

    <template v-else>
      <div v-if="posts.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
      </div>

      <div v-else class="text-center py-12 text-gray-500">
        Nema nadolazećih natjecanja.
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center items-center gap-4 mt-12">
        <button
          :disabled="currentPage <= 1"
          class="px-5 py-2 rounded-lg bg-blue-700 text-white font-semibold hover:bg-blue-800 transition disabled:opacity-40 disabled:cursor-not-allowed"
          @click="goToPage(currentPage - 1)"
        >
          Prethodna
        </button>

        <span class="text-gray-600">
          Stranica {{ currentPage }} od {{ totalPages }}
        </span>

        <button
          :disabled="currentPage >= totalPages"
          class="px-5 py-2 rounded-lg bg-blue-700 text-white font-semibold hover:bg-blue-800 transition disabled:opacity-40 disabled:cursor-not-allowed"
          @click="goToPage(currentPage + 1)"
        >
          Sljedeća
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPosts } from '@/api/index.js'
import PostCard from '@/components/PostCard.vue'

const route = useRoute()
const router = useRouter()

const posts = ref([])
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(1)

async function fetchPosts(page = 1) {
  loading.value = true
  try {
    const response = await getPosts({ category: 'calendar', page, limit: 9 })
    posts.value = response.data.items
    currentPage.value = response.data.page
    totalPages.value = response.data.pages
  } catch (error) {
    console.error('Greška pri dohvaćanju kalendara:', error)
  } finally {
    loading.value = false
  }
}

function goToPage(page) {
  router.push({ query: { ...route.query, page } })
}

watch(
  () => route.query.page,
  (page) => {
    fetchPosts(Number(page) || 1)
  }
)

onMounted(() => {
  fetchPosts(Number(route.query.page) || 1)
})
</script>
