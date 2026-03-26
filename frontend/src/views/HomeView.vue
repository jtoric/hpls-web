<template>
  <div>
    <!-- Hero section -->
    <section class="bg-gradient-to-br from-blue-900 to-blue-700 text-white py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">Hrvatski Powerlifting Savez</h1>
        <p class="text-xl md:text-2xl text-blue-100">
          Službena stranica Hrvatskog powerlifting saveza
        </p>
      </div>
    </section>

    <!-- Latest news -->
    <section class="max-w-6xl mx-auto px-4 py-16">
      <h2 class="text-3xl font-bold text-gray-800 mb-8">Najnovije novosti</h2>

      <div v-if="loading" class="text-center py-12 text-gray-500">
        Učitavanje...
      </div>

      <div v-else-if="posts.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
      </div>

      <div v-else class="text-center py-12 text-gray-500">
        Nema objavljenih novosti.
      </div>

      <div class="text-center mt-10">
        <router-link
          to="/novosti"
          class="inline-block bg-blue-700 hover:bg-blue-800 text-white font-semibold px-8 py-3 rounded-lg transition"
        >
          Sve novosti
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPosts } from '@/api/index.js'
import PostCard from '@/components/PostCard.vue'

const posts = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await getPosts({ limit: 6 })
    posts.value = response.data.items
  } catch (error) {
    console.error('Greška pri dohvaćanju novosti:', error)
  } finally {
    loading.value = false
  }
})
</script>
