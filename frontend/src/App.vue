<template>
  <div class="word-cloud">
    <span v-for="(word, index) in words" :key="index" :style="{ fontSize: `${sizes[index]}px` }"
      class="inline-block bg-blue-500 text-white rounded-full px-3 py-1 m-1">
      {{ word }}
    </span>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue';
const words = ref([]);
const sizes = ref([]);

const props = defineProps({
  words: {
    type: Array,
    required: true
  }
});

onMounted(() => {
  // Example data, replace with your logic
  // words.value = props.words || ['Vue', 'JavaScript', 'CSS', 'HTML'];
  fetch('http://localhost:8000/api/v1/person', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  })
    .then(response => response.json())
    .then(data => {
      words.value = data.words || [];
    })
    .catch(error => {
      console.error('Error fetching words:', error);
    });
  sizes.value = [20, 25, 18, 22];
});
</script>
