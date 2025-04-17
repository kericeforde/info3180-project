<template>
    <div class="match-container">
      <h1>Match Me</h1>
  
      <div v-if="loading">Loading matches...</div>
      <div v-if="error" class="error-message">{{ error }}</div>
  
      <div v-if="matches" class="match-grid">
        
        <div v-for="match in matches" :key="match.profile_id" class="match-card" @click="goToProfile(match.profile_id, match.user_id)" >
          <img :src="match.photo" alt="Profile Photo" class="profile-photo" />
          <p><strong>Name:</strong> {{ match.name }}</p>

          <p><strong>Birth Year:</strong> {{ match.birth_year }}</p>
          <p><strong>Height:</strong> {{ match.height }}</p>
          <p><strong>Favorite Cuisine:</strong> {{ match.fav_cuisine }}</p>
          <p><strong>Favorite Color:</strong> {{ match.fav_color }}</p>
          <p><strong>Favorite Subject:</strong> {{ match.fav_school_subject }}</p>
          <p><strong>Political:</strong> {{ match.political ? 'Yes' : 'No' }}</p>
          <p><strong>Religious:</strong> {{ match.religious ? 'Yes' : 'No' }}</p>
          <p><strong>Family Oriented:</strong> {{ match.family_oriented ? 'Yes' : 'No' }}</p>
        </div>
      </div>
  
      <div v-if="!loading && !matches.length && !error" class="no-match">
        No matches found.
      </div>
    </div>
  </template>
  
  <script setup>

  import { ref, onMounted } from 'vue';
  import { useRouter,useRoute} from 'vue-router';
  import { getToken } from '../auth.js';
  
  const route = useRoute();
  const profileId = route.params.profile_id;
  const token = getToken();
  const router = useRouter();
  const csrf_token = ref("");
  const matches = ref([]);
  const loading = ref(true);
  const error = ref("");
  
  function getCsrfToken() {
    fetch('/api/v1/csrf-token')
      .then(res => res.json())
      .then(data => csrf_token.value = data.csrf_token)
      .catch(err => console.error("CSRF Error:", err));
  }
  
  //This function fetches matching profile:
  async function fetchMatches() {
    try {
      const res = await fetch(`/api/profiles/matches/${profileId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'X-CSRFToken': csrf_token.value
        }
      });
  
      const data = await res.json();
  
      if (!res.ok) {
        throw new Error(data.error || errorMessage);
      }
  
      matches.value = data.matching_profiles;
      console.log(data.matching_profiles)
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }

  //With the use of this function clicking on an image takes you to the persons profile
  function goToProfile(profile_id, user_id) {
    localStorage.setItem("user_details_id", user_id);
    router.push({ name: "profileDetailsView", params: { profile_id } });
  }
  
  
  onMounted(async () => {
    getCsrfToken();
    fetchMatches();
  });
  </script>
  
  <style scoped>
  .match-container {
    padding: 2rem;
    background-image: url(../assets/back2.jpg); 
    background-size: cover;
    min-height: 100vh;
    color: #333;
    text-align: center;
  }
  h1{
    margin-top:5%;
  }
  .match-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-top: 2rem;
  }
  .match-card {
    background: #bdfa77;
    border-radius: 15px;
    padding: 1rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
  }
  .match-card:hover {
    transform: scale(1.02);
  }
  .profile-photo {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 50%;
    margin-bottom: 0.5rem;
  }
  .error-message {
    color: red;
    font-weight: bold;
    margin-top: 1rem;
  }
  .no-match {
    margin-top: 2rem;
    font-size: 1.2rem;
    font-style: italic;
  }
  </style>
  