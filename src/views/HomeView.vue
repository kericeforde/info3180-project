<template>
  <div class="home">
    <h1>Jam-Date</h1>

    
    <button class="hello" @click="goToLogin">Login</button>

    
    <button class="hello" @click="goToRegister">Register</button>

    
    <div v-if="route.path === '/login'" class="form-container">
      <LoginForm />
    </div>

    
    <div v-if="route.path === '/register'" class="form-container">
      <RegisterForm />
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";
import LoginForm from "../components/LoginForm.vue";
import RegisterForm from "../components/RegisterForm.vue";

const route = useRoute();
const router = useRouter();

const goToLogin = () => {
  router.push("/login");
};

const goToRegister = () => {
  router.push("/register");
};
</script>

<style scoped>
.home {
  text-align: center;

  /* Background image styling */
  background-image: url(../assets/back.png);
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center top;
  background-attachment: fixed; /* Optional: for parallax effect */

  /* Fullscreen container */
  height: 100vh;
  width: 100vw;

  /* Flexbox to center content */
  display: flex;
  flex-direction: column;
  align-items: center;  /* Horizontally center content */
  justify-content: center; /* Vertically center content */

  overflow: auto;
 
  
 
  

 
}

.buttons {
  margin: 20px;
}

.form-container {
  margin-top: 30px;
 
  
}


button {
  margin: 10px;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
  background-color:black;
  color:rgb(217, 201, 27);
  font-size:18px ;
}
h1{
  font-size: 100px;
  padding-top:150px;
  color: rgb(117, 237, 32);
 
}
</style>
