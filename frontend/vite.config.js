import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  
  server: {
    host: true,          // 👈 this makes Vite listen on all network interfaces
    port: 5173,          // optional, default is 5173
    strictPort: false , // optional, allows the server to start on a different port if 5173 is already in use
    proxy:{
      '/api': {
        target: 'http://localhost:8000', // replace with your backend server URL
        changeOrigin: true,
        secure: false
      } 
    }    // optional, allows the server to start on a different port if 5173 is already in use
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  }
})
