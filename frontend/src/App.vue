<!--
  App.vue — Root application shell.

  Renders the sticky header, the current route view, and the footer.
  The flex layout ensures the footer stays at the bottom even when
  the page content is shorter than the viewport.
-->
<script setup>
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>
