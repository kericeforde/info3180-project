<template>
  <div v-if="user" class="profile-container">
    <br/>

      <div class="profile-header">
        <img :src="user.photo" alt="Profile Photo" class="profile-photo" />
        <h2>{{ user.name }}</h2>
        <p class="profile-id">Username: {{ user.username }}</p>
        <p class="profile-id">Date joined: {{ user.date_joined }}</p>
      </div>

      <div class="grid">
        <div v-for="(prof, index) in user.profiles" :key="prof.profile_id" class="profile-details">
          <p><strong>Profile:</strong> {{ index + 1 }}</p>
          <p><strong>Gender:</strong> {{ prof.sex }}</p>
          <p><strong>Birth Year:</strong> {{ prof.birth_year }}</p>
          <p><strong>Race:</strong> {{ prof.race }}</p>
          <p><strong>Parish:</strong> {{ prof.parish }}</p>
          <p><strong>Biography:</strong> {{ prof.biography }}</p>
          <p><strong>Description:</strong> {{ prof.description }}</p>
          <p><strong>Height:</strong> {{ prof.height }}</p>
          <p><strong>Favourite Cuisine:</strong> {{ prof.fav_cuisine }}</p>
          <p><strong>Favourite Colour:</strong> {{ prof.fav_color }}</p>
          <p><strong>Favourite School Subject:</strong> {{ prof.fav_school_subject }}</p>
          <p><strong>Political Views:</strong> {{ prof.political }}</p>
          <p><strong>Religious Views:</strong> {{ prof.religious }}</p>
          <p><strong>Family Oriented:</strong> {{ prof.family_oriented }}</p>
          <!-- Changed Button : To add functionality using @click-->
          <button @click = "goToMatch(prof.profile_id)">MatchMe</button>
        </div>
      </div>
  </div>

  <!-- Error handling -->
 <div v-else-if="error" class="error-message">
    <p>{{ error }}</p>
  </div>
</template> 


<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { getToken } from '../auth.js'; 

const router = useRouter();
const user = ref(null);
const error = ref('');
const current_user = ref(localStorage.getItem('user_id')); 
let csrf_token = ref("");
const token = getToken(); 

// There should be a function for the Match Me Button Which I'll add Here
// It's purpose is to access "MatchMeView.vue" when the button is pressed
function goToMatch(profile_id)
{
  router.push({ name: 'matchMeView', params: {profile_id: profile_id}});
}

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(response => response.json())
    .then(data => {
      csrf_token.value = data.csrf_token;
    })
    .catch(error => console.log(error));
}

onMounted(async () => {
  getCsrfToken();
  try {
    const res = await fetch(`/api/users/${current_user.value}`, {
      credentials: 'include',
      headers: {
      'Authorization': `Bearer ${token}`,
      'X-CSRFToken': csrf_token.value
    },
      method: 'GET',
    } );

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.error || 'Failed to fetch profile');
    }

    const data = await res.json();
    if (!data) {
      throw new Error('Empty response from server');
    }

    user.value = data;

  } catch (err) {
    error.value = err.message;
    console.error('Error fetching profile:', err);
  }
});
</script>

<style scoped>
.profile-container {
    background-image: url(../assets/back2.jpg);
    background-repeat: no-repeat;
    background-position: center top;
    background-size: cover;
    min-height: 100vh; 
    max-height: 100vh;  
    width: 100%;
    height: auto;  
    overflow-y: auto;  
}


@media (max-width: 600px) {
    .profile-container {
        min-height: 100vh; 
        max-height: 100vh; 
    }
}


@media (min-width: 1200px) {
    .profile-container {
        min-height: 100vh;  
        max-height: 100vh;  
    }
}

.profile-header {
  text-align: center;
  margin-top: 2%;
}

.profile-details {
  padding: 50px;
  max-width: 600px;
  margin: 40px auto;
  background-color: #bdfa77;
  border-radius: 100px;
  
}

.profile-details:hover {
  background-color: #fffc34;
  transform: scale(1.02);
  transition: all 0.3s ease;
  cursor: pointer;
}


.grid{
    display:grid;
    justify-content: center;
    grid-template-columns: auto auto auto;
    gap: 150px;
  }

  button{
    margin-left:40px;
    padding:7px;
    background-color: rgb(15, 152, 56);
    border-radius: 5px;
    color: #fff;
}
button:hover{
    background-color:rgb(42, 229, 98) ;
}



.profile-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
  padding: 30px;
  text-align: left;
}


.profile-photo {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 10px;
}

.profile-header h2 {
  font-size: 26px;
  margin: 10px 0 5px;
  color: #333;
}

.profile-id {
  color: #888;
  font-size: 14px;
}



  

</style>
