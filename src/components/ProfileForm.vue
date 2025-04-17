<template>
  <div class="content">
    <br/>
    
    <form @submit.prevent="submitProfile" id="profileform">
      <div v-if="message" class="alert alert-success">{{ message }}</div>
    <div v-if="errors.length" class="alert alert-danger">
      <ul>
        <li v-for="(err, index) in errors" :key="index">{{ err }}</li>
      </ul>
    </div>
      <h1>Add New Profile</h1>
      <textarea v-model="description" placeholder="Description" rows="2"></textarea><br/>
      <select v-model="parish">
          <option disabled value="">Select Parish</option>
          <option>St. Thomas</option>
          <option>St. Andrew</option>
          <option>Kingston</option>
          <option>Portland</option>
          <option>St. Mary</option>
          <option>St. Ann</option>
          <option>Trelawny</option>
          <option>St. James</option>
          <option>Hanover</option>
          <option>Westmoreland</option>
          <option>St. Elizabeth</option>
          <option>Manchester</option>
          <option>Clarendon</option>
          <option>St. Catherine</option>
      </select>
      <br/>

      <input v-model="biography" placeholder="Biography" ><br/>
      <div class="radios">
      <label>
        <input id="radio" type="radio" value="male" v-model="sex" />
        Male
      </label>
      
      <label>
        <input id="radio" type="radio" value="female" v-model="sex" />
        Female
      </label></div>

      <br/>
      <input v-model="race" placeholder="Race"><br/>
      <input v-model="birthYear" type="number" placeholder="Birth Year"><br/>
      <input v-model="height" type="number" placeholder="Height in cm" min="90" max="245"><br/>

      <input v-model="favCuisine" placeholder="Favorite Cuisine"><br/>
      <input v-model="favColor" placeholder="Favorite Color"><br/>
      <input v-model="favSubject" placeholder="Favorite School Subject"><br/>
      
      <label>
        Political?      
        <select v-model="political">
          <option value="true">Yes</option>
          <option value="false">No</option>
        </select>
      </label><br/>

    <label>
      Religious?
      <select v-model="religious">
        <option value="true">Yes</option>
        <option value="false">No</option>
      </select>
    </label><br/>

    <label>
      Family Oriented?
      <select v-model="familyOriented">
        <option value="true">Yes</option>
        <option value="false">No</option>
      </select>
    </label><br/>

      <button type="submit">Save</button>
    </form>

    
  </div>
</template>

<script setup>
import { ref , onMounted} from 'vue';
import { getToken } from '../auth.js';


const description = ref('');
const parish = ref('');
const biography = ref('');
const sex = ref('');
const race = ref('');
const birthYear = ref('');
const height = ref('');
const favCuisine = ref('');
const favColor = ref('');
const favSubject = ref('');
const political = ref('');
const religious = ref('');
const familyOriented = ref('');
let csrf_token = ref("");
const token = getToken(); 

const message = ref('');
const errors = ref([]);

onMounted(() => {
  getCsrfToken();
});
function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(response => response.json())
    .then(data => {
      csrf_token.value = data.csrf_token;
    })
    .catch(error => console.log(error));
}

function submitProfile() {
  let form = document.getElementById("profileform");
  let form_data = new FormData(form);

  form_data.append("description", description.value);
  form_data.append("parish", parish.value);
  form_data.append("biography", biography.value);
  form_data.append("sex", sex.value);
  form_data.append("race", race.value);
  form_data.append("birth_year", birthYear.value);
  form_data.append("height", height.value);
  form_data.append("fav_cuisine", favCuisine.value);
  form_data.append("fav_color", favColor.value);
  form_data.append("fav_school_subject", favSubject.value);
  form_data.append("political",political.value);
  form_data.append("religious", religious.value);
  form_data.append("family_oriented", familyOriented.value);

  fetch('/api/profiles', {
    method: "POST",
    body: form_data,
    headers: {
      'Authorization': `Bearer ${token}`,
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then(async response => {
      const resData = await response.json();
      if (response.ok) {
        message.value = resData.message;
        resetForm();
      } 

      else if (response.status === 403) {
        errors.value = ['Maximum is 3 profiles per user'];
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
      
      
      else {
        errors.value = resData.errors || ['Something went wrong'];
      }
    })
    .catch(err => {
      errors.value = [err.message || 'Network error'];
    });
}

function resetForm() {
  description.value = '';
  parish.value = '';
  biography.value = '';
  sex.value = '';
  race.value = '';
  birthYear.value = '';
  height.value = '';
  favCuisine.value = '';
  favColor.value = '';
  favSubject.value = '';
  political.value = '';
  religious.value = '';
  familyOriented.value = '';
}
</script>

<style scoped>
.content{
 background-image: url(../assets/back2.jpg);
 background-repeat: no-repeat;
 background-position:center top ;
 background-size: cover;
 min-height:210vh;
 


}
@media (max-width: 600px) {
    .content {
        min-height: 150vh;  
        max-height: 210vh; 
        
    }
}

@media (min-width: 1200px) {
    .content {
        min-height: 150vh; 
        max-height: 210vh; 
        
    }
}

form {
  display: flex;
  flex-direction: column;
  margin:10% auto;
  width: 100%;
  max-width: 500px;
  
}
h1{
  color:#2b4f10;
}
input, textarea,select{
  width:100%;
  padding:8px;
  border:3px solid #90cd64;
  border-radius: 10px;
  
}
input:hover{
  background-color: #90cd64;
}

button{
  width:30%;
  background-color: #90cd64; 
  padding:7px;
  border-radius: 15px;
  font-size: 15px;
}
button:hover{
  background-color: #d1d114;
}
.alert-success {
  color: green;
  margin-top: 1em;
}
.alert-danger {
  color: red;
  margin-top: 1em;
}
</style>
