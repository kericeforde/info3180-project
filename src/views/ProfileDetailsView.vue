<template>
    <div class="contents">
      <div class="container py-4">
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-else-if="!profile" class="loading">Loading...</div>
        <ProfileDetails v-if="profile" :profile="profile" />
      </div>
      <div class="grid">
    <div v-if="profile" class="profile-details">
      <h1>{{ profile.name }}'s Profile</h1>
      <img :src="profile.photo" alt="Profile Photo" class="profile-photo" />
      <i class="bi bi-heart-fill text-danger fs-3" @click="addToFav(profile.user_id)"></i> 

      
      <button>Email</button>
      <p><strong>Description:</strong> {{ profile.description }}</p>
      <p><strong>Parish:</strong> {{ profile.parish }}</p>
      <p><strong>Biography:</strong> {{ profile.biography }}</p>
      <p><strong>Sex:</strong> {{ profile.sex }}</p>
      <p><strong>Race:</strong> {{ profile.race }}</p>
      <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
      <p><strong>Height:</strong> {{ profile.height }}</p>
      <p><strong>Favorite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
      <p><strong>Favorite Color:</strong> {{ profile.fav_color }}</p>
      <p><strong>Favorite Subject:</strong> {{ profile.fav_school_subject }}</p>
      <p><strong>Political Views:</strong> {{ profile.political ? 'Yes' : 'No' }}</p>
      <p><strong>Religious Views:</strong> {{ profile.religious ? 'Yes' : 'No' }}</p>
      <p><strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</p>
    </div>
    
    <div v-if="favProfiles" class="fav">
      <h1 class="favH1" >{{ profile.name }}'s favorite users</h1>
      <div v-for="fav in favProfiles.favorites" :key="fav.profile_id" class="fav-details">
      <img :src="fav.photo" alt="Profile Photo" class="profile-photo" />
      <p>{{ fav.name }}</p>
      
      </div>
    </div>
  </div>
</div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue';
  import { useRoute } from 'vue-router';
  import { getToken } from '../auth.js';

  const route = useRoute();
  const profile = ref(null);
  const favProfiles = ref(null);
  const error = ref('');
  const token = getToken(); 
  let csrf_token = ref("");
  const profile_id = ref(route.params.profile_id);
 

  function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(response => response.json())
    .then(data => {
      csrf_token.value = data.csrf_token;
    })
    .catch(error => console.log(error));
}

async function fetchData(url, errorMessage) {
    const res = await fetch(url, {
        credentials: 'include',
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'X-CSRFToken': csrf_token.value
        }
    });
    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || errorMessage);
    }
    return res.json();
}
  
  onMounted(async () => {
    getCsrfToken();
    profile_id.value = route.params.profile_id;
    
    try {
        profile.value = await fetchData(
            `/api/profiles/${profile_id.value}`,
            'Failed to fetch profile data'
        );
        let user_id = localStorage.getItem('user_details_id');
        console.log(user_id)
        favProfiles.value = await fetchData(
            `/api/users/${user_id}/favourites`,
            'Failed to fetch favorite profiles'
        );
        console.log(favProfiles.value);
    } catch (err) {
        error.value = err.message;
    }
   
  });
  
  function addToFav(userId) {
  fetch(`/api/profiles/${userId}/favorite`, {
    method: 'POST',
    headers: {
       
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token.value
    },
  })
  .then(response => response.json()) 
  .then(data => {
    if (data.message) {
      alert(data.message); 
    } else if (data.error) {
      alert(data.error); 
    }
  })
  .catch(error => {
    console.error('Error adding to favorites:', error);
  });
}


  </script>
  
  <style scoped>
  .profile-photo {
  width: 200px;
  height: 200px; 
  border-radius: 50%;
  object-fit: cover; 
  margin-bottom: 1rem;
}

  .profile-details {
    padding: 50px;
    max-width: 650px;
    margin: 40px auto;
    background-color: #bdfa77;
    border-radius: 100px;
    
  }
  .error-message {
    color: red;
    text-align: center;
    padding: 1rem;
  }
 
  
  

p{
    font-size: 1.2rem;
    margin: 0.5rem 0;
    font-size: 24px;
    font-family: 'Times New Roman', Times, serif;
}

.contents {
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
    .contents {
        min-height: 100vh;  
        max-height: 100vh;  
    }
}

@media (min-width: 1200px) {
    .contents {
        min-height: 100vh; 
        max-height: 100vh; 
    }
}
i{
    margin-left:26px; 
}
/* Add this in your styles section */
i:hover {
  cursor: pointer;

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
.fav-details{
  background-color:#bdfa77;
  margin-right:80%;
  padding: 20px;
  border-radius: 20px;
  margin-bottom: 5px;
  
}

.fav-details img{
  width: 100px;
  height: 100px; 
  border-radius: 50%;
  object-fit: cover; 
  margin-bottom: 1rem;
}
.favH1{
  margin-top:40px;
}
.grid{
    display:grid;
    grid-template-columns: auto auto ;
    gap:5px;
    /* align-items: center; */

}
  </style>
  