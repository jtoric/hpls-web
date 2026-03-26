<template>
  <header class="sticky top-0 z-50 bg-[#1a1a2e] shadow-lg">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      <!-- Hamburger (mobile only) -->
      <button
        class="md:hidden text-white p-2 hover:bg-white/10 rounded"
        @click="mobileMenuOpen = true"
        aria-label="Otvori izbornik"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <!-- Logo -->
      <router-link
        to="/"
        class="flex items-center gap-2 text-[#f1c40f] font-extrabold text-2xl tracking-wider select-none"
      >
        <span class="inline-flex items-center justify-center w-9 h-9 border-2 border-[#f1c40f] rounded-sm rotate-45">
          <span class="-rotate-45 text-base leading-none">&#9878;</span>
        </span>
        <span>HPLS</span>
      </router-link>

      <!-- Desktop nav -->
      <nav class="hidden md:flex items-center gap-1 text-sm">
        <router-link to="/" class="nav-link">Naslovnica</router-link>
        <router-link to="/novosti" class="nav-link">Novosti</router-link>
        <router-link to="/rekordi" class="nav-link">Rekordi</router-link>
        <router-link to="/poredak" class="nav-link">Poredak</router-link>
        <router-link to="/kalendar" class="nav-link">Kalendar</router-link>

        <!-- O nama dropdown -->
        <div class="relative" @mouseenter="oNamaOpen = true" @mouseleave="oNamaOpen = false">
          <button class="nav-link inline-flex items-center gap-1">
            O nama
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <Transition
            enter-active-class="transition duration-150 ease-out"
            enter-from-class="opacity-0 -translate-y-1"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition duration-100 ease-in"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 -translate-y-1"
          >
            <div
              v-if="oNamaOpen"
              class="absolute left-0 top-full mt-1 w-52 bg-[#1a1a2e] border border-white/10 rounded shadow-xl py-1"
            >
              <router-link to="/o-nama/osnivanje-kluba" class="dropdown-link">Osnivanje kluba</router-link>
              <router-link to="/o-nama/pravila" class="dropdown-link">Pravila</router-link>
              <router-link to="/o-nama/anti-doping" class="dropdown-link">Anti doping</router-link>
              <router-link to="/o-nama/registracija-natjecatelja" class="dropdown-link">Registracija natjecatelja</router-link>
              <router-link to="/o-nama/clanstvo" class="dropdown-link">Članstvo</router-link>
              <router-link to="/o-nama/pristup-informacijama" class="dropdown-link">Pristup informacijama</router-link>
            </div>
          </Transition>
        </div>

        <router-link to="/dokumenti" class="nav-link">Dokumenti</router-link>
        <router-link to="/kontakt" class="nav-link">Kontakt</router-link>
        <router-link v-if="authStore.isAuthenticated" to="/admin" class="nav-link !text-[#f1c40f]">Admin</router-link>
      </nav>

      <!-- Search icon -->
      <button
        class="text-white p-2 hover:bg-white/10 rounded"
        @click="searchOpen = true"
        aria-label="Pretraži"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </button>
    </div>

    <!-- Mobile menu -->
    <MobileMenu v-model="mobileMenuOpen" />

    <!-- Search modal -->
    <SearchModal v-model="searchOpen" />
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import MobileMenu from './MobileMenu.vue'
import SearchModal from './SearchModal.vue'

const authStore = useAuthStore()
const mobileMenuOpen = ref(false)
const searchOpen = ref(false)
const oNamaOpen = ref(false)
</script>

<style scoped>
@reference "../style.css";
.nav-link {
  @apply text-gray-200 hover:text-[#f1c40f] px-3 py-2 rounded transition-colors duration-200;
}
.dropdown-link {
  @apply block px-4 py-2 text-sm text-gray-200 hover:text-[#f1c40f] hover:bg-white/5 transition-colors;
}
</style>
