<template>
    <div class="contents">
      <div class="search">
        <h1>SEARCH</h1>
        <div class="searchfields">
            <input v-if="namesearch" v-model="name" type="text" placeholder="Search by name">
            <input v-if="birthYearsearch" v-model="birthYear" type="number" placeholder="Search by birth year">
            <input v-if="sexsearch" v-model="sex" type="text" placeholder="Search by sex">
            <input v-if="racesearch" v-model="race" type="text" placeholder="Search by race">
            <br/>
            <button id="btn" @click="submitSearch">Search</button>
        </div>
      </div>  
      <br/>
      <div class="searchButtons">
       <button @click="namesearch = !namesearch">Name</button>
       <button @click="birthYearsearch = !birthYearsearch">BirthYear</button>
       <button @click="sexsearch = !sexsearch">Sex</button>
       <button @click="racesearch = !racesearch">Race</button>
       </div>

        <div class="display">
        <div v-if="message" class="alert alert-success">{{ message }}</div>
        <div v-if="errors.length" class="alert alert-danger">
         <ul>
        <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
      </ul>
    </div>
    <div v-if="results.length || prof4.length">
  <h2>Profiles</h2>

  <!-- Show last four profiles -->
  <div v-if="prof4.length && !results.length">
    <h4>Recent Profiles</h4>
    <div class="dis">
    <div v-for="prof in prof4" :key="prof.profile_id" class="result-card">
      <img :src="prof.photo" alt="Profile Photo" width="80" height="80" />
      <p><strong>Name:</strong> {{ prof.name }}</p>
      <button @click="goToProfile(prof.profile_id,prof.user_id)" class="view-button">
      
    View Profile
  </button>
    </div>
  </div></div>

  <!-- Show search results or whatever `results` is -->
  <div v-if="results.length">
    <h3>Search Results</h3>
    <div class="dis" >
    <div v-for="profile in results" :key="profile.profile_id" class="result-card">
      <img :src="profile.photo" alt="Profile Photo" />
      <p><strong>Name:</strong> {{ profile.name }}</p>
      <button @click="goToProfile(profile.profile_id,profile.user_id)" class="view-button">
    View Profile
  </button>
    </div>
  </div>
  </div>
</div>
     </div>
    </div>

</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router"; 
import { getToken } from '../auth.js'; 
const router = useRouter();
const token = getToken(); 
let csrf_token = ref("");
let prof4= ref([]);

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(response => response.json())
    .then(data => {
      csrf_token.value = data.csrf_token;
    })
    .catch(error => console.log(error));
}
  
onMounted(() => {
  fetch("/api/profiles", {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'X-CSRFToken': csrf_token.value
    }
  })
    .then(async (response) => {
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Failed to fetch profiles.");
      }
      prof4.value = data.profiles.slice(0, 4);
      

    })
    .catch((error) => console.error("Error fetching profiles:", error.message));

  getCsrfToken();});


const namesearch = ref(false);
const birthYearsearch = ref(false);
const sexsearch = ref(false);
const racesearch = ref(false);

const name = ref('');
const birthYear = ref('');
const sex = ref('');
const race = ref('');
const results=ref([])
const errors = ref('');
const message=ref('')


async function submitSearch() {
  // Clear previous search results
  message.value = "";
  results.value = [];

  const params = new URLSearchParams();

  // Append query parameters only if values are present
  if (namesearch.value && name.value) params.append('name', name.value);
  if (birthYearsearch.value && birthYear.value) params.append('birth_year', birthYear.value);
  if (sexsearch.value && sex.value) params.append('sex', sex.value);
  if (racesearch.value && race.value) params.append('race', race.value);

  // If no search options are selected, show an error and don't clear previous inputs
  if (!namesearch.value && !birthYearsearch.value && !sexsearch.value && !racesearch.value) {
    errors.value = ['Please select a search option'];
    return;
  }

  try {
    const response = await fetch(`/api/search?${params.toString()}`,{
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'X-CSRFToken': csrf_token.value
    }
  });
    const data = await response.json();

    if (response.status === 403) {
      errors.value = [data.error || 'Unauthorized access'];
    } else if (data.profiles && data.profiles.length > 0) {
      results.value = data.profiles;
      
      message.value = 'Search successful!';
    } else {
      // Show no profiles found if the array is empty
      results.value = [];
      message.value = 'No profiles found.';
    }
    errors.value = [];
  } catch (error) {
    errors.value = [error.message || 'Error occurred'];
  }
}

  function goToProfile(profile_id,user_id) {
   
    localStorage.setItem('user_details_id', user_id);
    
    router.push({ name: 'profileDetailsView', params: { profile_id: profile_id} });
  }




</script>

<style scoped>

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
.search{
    display: flex;
    flex-wrap: wrap;
    flex-direction: column;
    background-color: #FFD700 ;
    justify-content: center; 
    align-items: center;
    position:center top;
    padding:50px;
    max-width: 100%; 
    margin:4% 30% ;
    border-radius: 50px;
  
}
h1{
  color: #0a3206;
 
}
input{
   margin:5px;
   border-radius: 5px;
   padding:7px;
} 
.searchButtons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center; 
  margin-bottom: 20px;
  
  
}
 button {
  margin-left:7px;
  padding:7px;
  width:100px;
  border-radius: 6px;
  background-color: #0f0f0f;
  color: #f1f1f1;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #333333;
  transform: scale(1.02);
  transition: all 0.3s ease;
  cursor: pointer;
}


.display{
  display:flex;
  flex-direction:column;
  
  align-items: center;
}
.dis{
  display:grid;
  justify-content: center;
  grid-template-columns: auto auto auto auto;
  gap: 20px;
  
}
.dis button{
   font-size: 10px;
   padding:5px;
   margin:0px 15%;
}
.result-card{
  background-color: rgb(104, 227, 118);
  padding:10px;
  border-radius: 7px;
  /* border:solid 2px black; */
  margin-bottom: 50px;
  align-items: center;

}
.result-card:hover {
  background-color: #5dff58;
  transform: scale(1.02);
  transition: all 0.3s ease;
  cursor: pointer;
}
img{
  width:200px;
  height:auto;

}
</style>