<template>
  <header>
    <nav class="navbar navbar-expand-lg  fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Jam-Date</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">

            <li class="nav-item" v-if="isLoggedIn">
              <RouterLink to="/dashboard" class="nav-link">Dashboard</RouterLink>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <RouterLink to="/reports" class="nav-link">View Reports</RouterLink>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <RouterLink to="/profile" class="nav-link">My Profile</RouterLink>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <button @click="logout" class="nav-link btn btn-link text-white">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const isLoggedIn = ref(false);


const router = useRouter();

const logout = () => {
  isLoggedIn.value = false; 
  router.push('/'); 
};
</script>

<style >

.navbar,header {
  background-color: #108f21;
  
}

.navbar-nav .nav-link {
  color: white;
}

.navbar-nav .nav-link:hover {
  color: #f8f9fa;
}

.navbar-toggler-icon {
  background-color: white;
}

.navbar-nav .btn-link {
  text-decoration: none;
  color: white;
}

.navbar-nav .btn-link:hover {
  color: #f8f9fa;
}
</style>
