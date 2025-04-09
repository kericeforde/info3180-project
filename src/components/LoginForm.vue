<template>
  
    <form @submit.prevent="login" id="login-form">
      <br/>
      <div class="form-container">
      <h2>Login</h2>
      <div v-if="message" class="alert alert-success">{{ message }}</div>
      <div v-if="errors.length" class="alert alert-danger">
        <ul>
          <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </ul>
      </div>
      <input v-model="username" type="text" placeholder="Username" class="form-control" required /><br/>
      <input v-model="password" type="password" placeholder="Password" class="form-control" required /><br/>
      <button type="submit">Login</button>
    </div>
    </form>
  </template>
<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";  
import { setLoginState } from '../auth.js';

let username = ref("");
let password = ref("");
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


function login() {
  let form = document.getElementById("login-form");
  let form_data = new FormData(form);
  form_data.append("username", username.value);
  form_data.append("password", password.value);

  fetch("/api/auth/login", {
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
      
      setLoginState(true);
      router.push({ name: 'dashboard' });
      
    }
  })
  .catch(error => console.log(error));
}
</script>


<style scoped>

#login-form {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.form-container {
  background-color: white;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
  width: 100%;
  max-width: 250px;
  
  text-align: center;
  margin: auto;
  
}

h2 {
  margin-bottom: 5px;
  font-size: 20px;
  color: #333;
}

input {
  width: 100%;
  padding: 7px;
  margin: 3px 0;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 16px;
  transition: all 0.3s ease;
}


button {
  width: 100%;
  padding: 5px;
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