import { defineConfig } from 'vite'

// Proxy API calls from the dev server to backend at localhost:8000
export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      '/health': 'http://localhost:8000',
      '/predict': 'http://localhost:8000',
      '/reload-model': 'http://localhost:8000'
    }
  }
})
