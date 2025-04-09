<template>
    <div class="contents">
      <div class="search">
        <h1>Search</h1>
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
    <div v-if="results.length">
      <h3>Results:</h3>
      <div v-for="profile in results" :key="profile.id" class="result-card">
        <img :src="profile.photo" alt="Profile Photo" width="80" height="80" />
        <p><strong>Name:</strong> {{ profile.name }}</p>
        <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
        <p><strong>Sex:</strong> {{ profile.sex }}</p>
        <p><strong>Race:</strong> {{ profile.race }}</p>
        <p><strong>Bio:</strong> {{ profile.biography }}</p>
      </div>
       </div>
     </div></div>

</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";  

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
function submitSearch(){

  const params =new URLSearchParams();
  
  if (namesearch.value && name.value) params.append('name', name.value);

  if (birthYearsearch.value && birthYear.value) params.append('birth_year', birthYear.value);

  if (sexsearch.value && sex.value) params.append('sex', sex.value);

  if (racesearch.value && race.value) params.append('race', race.value);

  fetch(`/api/search?${params.toString()}`)
  .then(response => response.json().then(data => {
      if (response.status === 403) {
        errors.value = [data.error || 'Error'];
        message.value = "";
        results.value = [];
      } else {
        if (data.profiles) {
          results.value = data.profiles;
          message.value = 'Search successful!';
        }
        errors.value = [];
      }
    }))
    .catch(error => {
      errors.value = [error.message || 'Error occurred'];
      message.value = "";
      results.value = [];
    });
}


</script>

<style scoped>

.contents{
    /* display: flex;
    justify-content: center;
    align-items: center; */
    /* margin-top:15%; */
    /* flex-direction: column; */
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
    margin:5% 5% ;
    border-radius: 10px;
  
}
h1{
  
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

.searchButtons input:hover {
  background-color: #1e1e1e;
}


</style>