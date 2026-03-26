<!--
  PostView.vue — Single post detail page (route: /novosti/:slug or /kalendar/:slug).

  Displays the full post content (rendered HTML via v-html), the featured
  image, a formatted date, and a list of downloadable attachments.
  The "back" link adapts based on the post category.
-->
<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <div v-if="loading" class="text-center py-12 text-gray-500">
      Učitavanje...
    </div>

    <template v-else-if="post">
      <!-- Context-aware back link (news vs calendar) -->
      <router-link
        :to="backLink"
        class="inline-flex items-center text-blue-700 hover:text-blue-900 font-medium mb-6 transition"
      >
        &larr; {{ backLabel }}
      </router-link>

      <article>
        <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-3">
          {{ post.title }}
        </h1>

        <p class="text-gray-500 mb-6">
          {{ formatDate(post.created_at) }}
        </p>

        <img
          v-if="post.featured_image"
          :src="post.featured_image"
          :alt="post.title"
          class="w-full rounded-lg mb-8 object-cover max-h-96"
        />

        <!-- Post HTML content (sanitised on the backend) -->
        <div class="prose prose-lg max-w-none" v-html="post.content"></div>

        <!-- Downloadable attachments -->
        <div v-if="post.attachments && post.attachments.length" class="mt-10 border-t pt-6">
          <h3 class="text-xl font-semibold text-gray-800 mb-4">Prilozi</h3>
          <ul class="space-y-2">
            <li v-for="attachment in post.attachments" :key="attachment.id">
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
      </article>
    </template>

    <div v-else class="text-center py-12 text-gray-500">
      Objava nije pronađena.
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getPost } from '@/api/index.js'
import { formatDate } from '@/utils/formatters'

const route = useRoute()

const post = ref(null)
const loading = ref(true)

/** Navigate back to the appropriate list view. */
const backLink = computed(() => {
  return post.value?.category === 'calendar' ? '/kalendar' : '/novosti'
})

const backLabel = computed(() => {
  return post.value?.category === 'calendar' ? 'Natrag na kalendar' : 'Natrag na novosti'
})

onMounted(async () => {
  try {
    const response = await getPost(route.params.slug)
    post.value = response.data
  } catch (error) {
    console.error('Greška pri dohvaćanju objave:', error)
  } finally {
    loading.value = false
  }
})
</script>
