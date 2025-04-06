<template>
  <div class="items-center justify-center flex flex-col min-h-screen bg-gray-100 gap-4">
    <div class="bg-gray-300 rounded-full p-6">
      <img :src="vueLogoUrl" alt="Vue logo" class="w-16 h-16" />
    </div>
    <div class="bg-white shadow-lg rounded-lg p-6 max-w-lg mx-auto">
      <div v-if="book">
      <h2 class="text-xl font-bold text-gray-800 mb-4">{{ book.title }}</h2>
      <h3 class="text-md font-medium text-gray-600 mb-4">
        By: <span v-for="(author, index) in book.authors" :key="index">
        {{ author }}<span v-if="index < book.authors.length - 1">, </span>
        </span>
      </h3>
      <div class="text-gray-700 space-y-2">
        <p><strong>Token:</strong> {{ book.token }}</p>
        <p><strong>Published:</strong> {{ book.published }}</p>
      </div>
      </div>
      <div v-else class="text-gray-500 text-center">Loading...</div>
    </div>
  </div>
</template>

<script setup>
const vueLogoUrl = new URL('./assets/vue.svg', import.meta.url).href
import { ref, onMounted } from 'vue'

const book = ref(null) 

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/book/1')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    book.value = await response.json()
  } catch (error) {
    console.error('Error fetching the book:', error)
  }
})
</script>