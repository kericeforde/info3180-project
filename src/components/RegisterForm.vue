<template>
    <form @submit.prevent="register" id="reg-form">
      <br/>
      <div class="form-container">
      <h2>Register</h2>
      <div v-if="message" class="alert alert-success">{{ message }}</div>
      <div v-if="errors.length" class="alert alert-danger">
        <ul>
          <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </ul>
      </div>
      <input v-model="username" type="text" placeholder="Username" required />
      <br/>
      <input v-model="password" type="password" placeholder="Password" required />
      <br/>
      <input v-model="name" type="name" placeholder="Full Name" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input type="file" @change="handleFileUpload" placeholde="Photo of yourself" name="photo" class="form-control" required />
      <br/>
      <button type="submit">Register</button>
      </div>
      
    </form>
  </template>
<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";  


let username = ref("");
let password = ref("");
let email = ref("")
let name = ref("")
let photo =ref(null)
let csrf_token = ref("");
let message = ref("");
let errors = ref([]);

const router = useRouter();

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


function handleFileUpload(event) {
    poster.value = event.target.files[0];
  }

function register() {
  let form = document.getElementById("reg-form");
  let form_data = new FormData(form);
  form_data.append("username", username.value);
  form_data.append("password", password.value);
  form_data.append("name", name.value);
  form_data.append("email", email.value);
  form_data.append("photo", photo.value);


  fetch("/api/register", {
    method: 'POST',
    body: form_data,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.errors) {
      errors.value = Object.values(data.errors).flat(); 
      message.value = "";
    } else {
      message.value = data.message;
      errors.value = [];
      username.value = "";
      password.value = "";
      name.value = "";
      email.value="";
      photo.value=null;


      router.push({ name: 'login' });
    }
  })
  .catch(error => console.log(error));
}
</script>

<style scoped>

#reg-form {
  display: flex;
  justify-content: center;
  align-items: center;
  
 
  margin-bottom: 20px;
}

.form-container {
  background-color: white;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
  width: 100%;
  max-width: 280px;
  
  text-align: center;
  margin: auto;
  
}

h2 {
  margin-bottom: 5px;
  font-size: 18px;
  color: #333;
}

input {
  width: 100%;
  padding: 3px;
  margin: 2px 0;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 16px;
  transition: all 0.3s ease;
}


button {
  width: 100%;
  padding: 3px;
  background-color: #4CAF50; 
  color: white;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049; 
}

button:active {
  background-color: #388e3c; 
}

input,
button {
  box-sizing: border-box;
}
.alert {
    padding:0px;
    font-size: 9px;
    
  }
</style>