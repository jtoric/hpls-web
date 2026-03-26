<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="modelValue"
        class="fixed inset-0 z-[100] bg-black/60"
        @click.self="close"
      >
        <Transition
          enter-active-class="transition duration-300 ease-out"
          enter-from-class="-translate-x-full"
          enter-to-class="translate-x-0"
          leave-active-class="transition duration-200 ease-in"
          leave-from-class="translate-x-0"
          leave-to-class="-translate-x-full"
        >
          <aside
            v-if="modelValue"
            class="absolute inset-y-0 left-0 w-72 max-w-[85vw] bg-[#1a1a2e] shadow-2xl flex flex-col overflow-y-auto"
          >
            <!-- Header -->
            <div class="flex items-center justify-between px-4 h-16 border-b border-white/10">
              <router-link
                v-if="authStore.isAuthenticated"
                to="/admin"
                class="text-[#f1c40f] font-semibold text-sm hover:underline"
                @click="close"
              >
                Admin
              </router-link>
              <router-link
                v-else
                to="/prijava"
                class="text-gray-300 text-sm hover:text-white"
                @click="close"
              >
                Prijava
              </router-link>

              <button
                class="text-white p-2 hover:bg-white/10 rounded"
                @click="close"
                aria-label="Zatvori izbornik"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Nav items -->
            <nav class="flex-1 py-4">
              <router-link to="/" class="mobile-link" @click="close">Naslovnica</router-link>
              <router-link to="/novosti" class="mobile-link" @click="close">Novosti</router-link>
              <router-link to="/rekordi" class="mobile-link" @click="close">Rekordi</router-link>
              <router-link to="/poredak" class="mobile-link" @click="close">Poredak</router-link>
              <router-link to="/kalendar" class="mobile-link" @click="close">Kalendar</router-link>

              <!-- O nama expandable -->
              <div>
                <button
                  class="mobile-link w-full flex items-center justify-between"
                  @click="oNamaExpanded = !oNamaExpanded"
                >
                  <span>O nama</span>
                  <svg
                    class="w-4 h-4 transition-transform duration-200"
                    :class="{ 'rotate-180': oNamaExpanded }"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <Transition
                  enter-active-class="transition duration-200 ease-out"
                  enter-from-class="opacity-0 max-h-0"
                  enter-to-class="opacity-100 max-h-48"
                  leave-active-class="transition duration-150 ease-in"
                  leave-from-class="opacity-100 max-h-48"
                  leave-to-class="opacity-0 max-h-0"
                >
                  <div v-if="oNamaExpanded" class="overflow-hidden bg-white/5">
                    <router-link to="/o-nama/osnivanje-kluba" class="mobile-link pl-8 text-sm" @click="close">Osnivanje kluba</router-link>
                    <router-link to="/o-nama/pravila" class="mobile-link pl-8 text-sm" @click="close">Pravila</router-link>
                    <router-link to="/o-nama/anti-doping" class="mobile-link pl-8 text-sm" @click="close">Anti doping</router-link>
                    <router-link to="/o-nama/registracija-natjecatelja" class="mobile-link pl-8 text-sm" @click="close">Registracija natjecatelja</router-link>
                    <router-link to="/o-nama/clanstvo" class="mobile-link pl-8 text-sm" @click="close">Članstvo</router-link>
                    <router-link to="/o-nama/pristup-informacijama" class="mobile-link pl-8 text-sm" @click="close">Pristup informacijama</router-link>
                  </div>
                </Transition>
              </div>

              <router-link to="/dokumenti" class="mobile-link" @click="close">Dokumenti</router-link>
              <router-link to="/kontakt" class="mobile-link" @click="close">Kontakt</router-link>
            </nav>
          </aside>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])
const authStore = useAuthStore()
const oNamaExpanded = ref(false)

function close() {
  emit('update:modelValue', false)
}
</script>

<style scoped>
@reference "../style.css";
.mobile-link {
  @apply block px-4 py-3 text-gray-200 hover:text-[#f1c40f] hover:bg-white/5 transition-colors duration-150;
}
</style>
