<template>
    <div class="reports-container">
      <h1>Favourite Users</h1>
  
      <div v-if="loading">Loading...</div>
      <div v-if="error" class="error-message">{{ error }}</div>
  
      <!-- Current User's Favourites -->
      <h2 class="section-label">My Favourites</h2>
      <div v-if="myFavourites.length" class="my-fav-grid">
        <div
          v-for="user in myFavourites" :key="user.user_id" class="fav-card" @click="goToProfile(user.profile_id, user.user_id)" title="Click to view profile">
          <img :src="user.photo" alt="User Photo" class="profile-photo" />
          <p><strong>Name:</strong> {{ user.name }}</p>
          <p><strong>Parish:</strong> {{ user.parish }}</p>
          <p><strong>Age:</strong> {{ user.age }}</p>
        </div>
      </div>
  
      <!-- Top 20 Jam-Date Favourites -->
      <h2 class="section-label">Top 20 Jam-Date Favourites</h2>
      <div v-if="report.length" class="top-fav-scroll">
        <div
          v-for="user in report" :key="user.user_id" class="top-fav-card" @click="goToProfile(user.profile_id, user.user_id)" title="Click to view profile">
          <img :src="user.photo" alt="User Photo" class="top-photo" />
          <p><strong>Name:</strong> {{ user.name }}</p>
          <p><strong>Parish:</strong> {{ user.parish }}</p>
          <p><strong>Age:</strong> {{ user.age }}</p>

        </div>
      </div>
  
      <!--Button: Sort Buttons-->
      <div class="sort-buttons">
        <button @click="sortBy('fav_count')">Sort by Favourite Count</button>
        <button @click="sortBy('name')">Sort by Name</button>
        <button @click="sortBy('parish')">Sort by Parish</button>
        <button @click="sortBy('age')">Sort by Age</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  import { ref, onMounted } from 'vue';
  import { getToken } from '../auth.js';
  
  const router = useRouter();
  const token = getToken();
  const csrf_token = ref("");
  const report = ref([]);
  const myFavourites = ref([]);
  const loading = ref(false);
  const error = ref("");
  const currentSort = ref("fav_count");
  const userId = localStorage.getItem('user_id'); //Used this to get id related to user mentioned in images
  
  function getCsrfToken() {
    fetch("/api/v1/csrf-token")
      .then((res) => res.json())
      .then((data) => (csrf_token.value = data.csrf_token))
      .catch((err) => console.error("CSRF error:", err));
  }

  //With the use of this function clicking on an image takes you to the persons profile
  function goToProfile(profile_id, user_id) {
    localStorage.setItem("user_details_id", user_id);
    router.push({ name: "profileDetailsView", params: { profile_id } });
  }
  
  //Fetches Favourites of the Current User
  async function fetchMyFavourites() {
    try {
      const res = await fetch(`/api/users/${userId}/favourites`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          "X-CSRFToken": csrf_token.value,
        }
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Error fetching your favourites.");
      myFavourites.value = data.favorites;
    } catch (err) {
      console.error(err);
    }
  }
  
  //Fetches Top 20 Favourites
  async function fetchReport() {
    loading.value = true;
    error.value = "";
    try {
      const res = await fetch(`/api/users/favourites/20?sort=${currentSort.value}`, {
        method: "GET",
        headers: {
          'Authorization': `Bearer ${token}`,
          "X-CSRFToken": csrf_token.value,
        },
      });
      const data = await res.json();
  
      if (!res.ok) {
        throw new Error(data.error || "Failed to fetch report");
      }
  
      report.value = data.top_favorites;
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }
  
  //function to sort by the specified paramater (Name, age, etc)
  function sortBy(param) 
  {
    currentSort.value = param;
    fetchReport();
  }
  
  onMounted(() => {
    getCsrfToken();
    fetchReport();
    fetchMyFavourites();
  });
  </script>
  
  <style scoped>
  .reports-container {
    padding: 2rem;
    background-image: url(../assets/back2.jpg);
    background-size: cover;
    min-height: 100vh;
    color: #333;
    text-align: center;
  }
  h1{
    margin-top: 5%;
  }
  .section-label {
    font-size: 24px;
    font-weight: bold;
    margin: 20px 0 10px;
    font-family: 'Georgia', serif;
  }
  
  .my-fav-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 30px;
  }
  
  .fav-card {
    background-color: #bdfa77;
    border-radius: 15px;
    padding: 1rem;
    text-align: center;
    text-decoration: none;
    color: #000;
    transition: transform 0.2s ease;
  }
  
  .fav-card:hover {
    transform: scale(1.05);
    cursor: pointer;

  }
  
  .top-fav-scroll {
    display: flex;
    overflow-x: auto;
    gap: 15px;
    padding: 10px 5px;
    margin-bottom: 30px;
    background-color: #bdfa77;
    width:fit-content;
  }
  
  .top-fav-card {
    flex: 0 0 auto;
    text-decoration: none;
  }
  
  .top-photo {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    transition: transform 0.2s ease;
  }
  
  .top-photo:hover {
    transform: scale(1.1);
    cursor: pointer;
  }
  
  .sort-buttons button {
    margin: 0.5rem;
    padding: 8px 15px;
    background-color: #000;
    color: #f1f1f1;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .sort-buttons button:hover {
    background-color: #333;
  }
  
  .error-message {
    color: red;
    font-weight: bold;
    margin-top: 1rem;
  }
  
  .profile-photo {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 50%;
    margin-bottom: 0.5rem;
  }
  </style>
  