<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";

import { ref } from 'vue'
const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true')

</script>

<template>
  <div class="layout-wrapper">
  <AppHeader />

  <main class="main-content">
    <RouterView />
  </main>
  
  <!-- <AppFooter /> -->
</div>
</template>

<style>




</style>