/**
 * Vite configuration for the HPLS frontend.
 *
 * - Vue 3 SFC support via @vitejs/plugin-vue
 * - TailwindCSS v4 integration via @tailwindcss/vite
 * - "@" path alias pointing to src/ for clean imports
 * - Dev proxy: /api and /uploads forwarded to the FastAPI backend on :8000
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue(), tailwindcss()],

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },

  server: {
    // Forward API and upload requests to the FastAPI backend during development.
    proxy: {
      '/api': 'http://localhost:8000',
      '/uploads': 'http://localhost:8000',
    },
  },

  // Vitest configuration (inline to avoid a separate vitest.config.js).
  test: {
    environment: 'happy-dom',
    globals: true,
  },
})
