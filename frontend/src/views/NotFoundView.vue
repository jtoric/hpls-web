<!--
  NotFoundView.vue — 404 catch-all page.

  Displayed when no route matches the requested URL.
  Provides a friendly message and a link back to the homepage.
-->
<template>
  <div class="min-h-[60vh] flex flex-col items-center justify-center px-4 text-center">
    <h1 class="text-6xl font-extrabold text-gray-300 mb-4">404</h1>
    <p class="text-xl text-gray-600 mb-8">Stranica nije pronađena.</p>
    <router-link
      to="/"
      class="inline-block bg-blue-700 hover:bg-blue-800 text-white font-semibold px-8 py-3 rounded-lg transition"
    >
      Natrag na naslovnicu
    </router-link>
  </div>
</template>
