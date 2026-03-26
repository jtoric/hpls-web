<template>
  <router-link
    :to="postUrl"
    class="group block bg-white rounded-lg shadow hover:shadow-lg transition-shadow duration-200 overflow-hidden"
  >
    <div class="flex flex-col sm:flex-row">
      <!-- Image -->
      <div class="sm:w-1/3 flex-shrink-0">
        <div class="aspect-video sm:aspect-auto sm:h-full bg-gray-100 overflow-hidden">
          <img
            v-if="post.featured_image"
            :src="post.featured_image"
            :alt="post.title"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <div
            v-else
            class="w-full h-full min-h-[160px] flex items-center justify-center bg-gray-200 text-gray-400"
          >
            <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Content -->
      <div class="p-4 sm:p-5 flex flex-col justify-center flex-1">
        <time class="text-xs text-gray-400 mb-1 block">{{ formattedDate }}</time>
        <h3 class="text-lg font-semibold text-gray-900 group-hover:text-[#2471a3] transition-colors mb-2 line-clamp-2">
          {{ post.title }}
        </h3>
        <p v-if="post.excerpt" class="text-sm text-gray-600 line-clamp-3">
          {{ post.excerpt }}
        </p>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const croatianMonths = [
  'siječnja', 'veljače', 'ožujka', 'travnja', 'svibnja', 'lipnja',
  'srpnja', 'kolovoza', 'rujna', 'listopada', 'studenoga', 'prosinca',
]

const formattedDate = computed(() => {
  if (!props.post.created_at) return ''
  const date = new Date(props.post.created_at)
  const day = date.getDate()
  const month = croatianMonths[date.getMonth()]
  const year = date.getFullYear()
  return `${day}. ${month} ${year}.`
})

const postUrl = computed(() => {
  const base = props.post.category === 'kalendar' ? '/kalendar' : '/novosti'
  return `${base}/${props.post.slug}`
})
</script>
