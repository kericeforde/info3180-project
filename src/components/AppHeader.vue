<template>
  <header>
    <nav class="navbar navbar-expand-lg  fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Jam-Date</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">

            <li class="nav-item" v-if="auth.isLoggedIn">
              <RouterLink to="/dashboard" class="nav-link">Dashboard</RouterLink>
            </li>
            <li class="nav-item" v-if="auth.isLoggedIn">
              <RouterLink to="/profiles/favourites" class="nav-link">View Reports</RouterLink>
            </li>
            <li class="nav-item" v-if="auth.isLoggedIn">
              <button @click="myprofile" class="nav-link btn btn-link text-white">My Profile</button>

            </li>
            <li class="nav-item" v-if="auth.isLoggedIn">
              <RouterLink to="/profiles/new" class="nav-link">Create Profile</RouterLink>

            </li>
            <li class="nav-item" v-if="auth.isLoggedIn">
              <button @click="logout" class="nav-link btn btn-link text-white">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, computed ,onMounted} from 'vue';
import { RouterLink,useRouter } from 'vue-router';
import { auth,logoutUser,removeToken,removeUserId, getToken} from '../auth.js';

let router = useRouter();



//   computed: {
//     userId() {
//       return localStorage.getItem('user_id');
//     }
//   }
// }
function logout() {
  let token = getToken(); 
  fetch('/api/auth/logout', {
    //method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,

    },
  } ) 
    .then(() => {
      logoutUser();  
      removeToken();
      token = null;
      removeUserId();
      router.push('/logout');
    });
}

function myprofile()
{
  let userIdRef = ref(localStorage.getItem('user_id'));
  router.push({ name: 'myProfileView', params: { users_id: userIdRef.value } });
}



</script>

<style >

.navbar,header {
  background-color: #108f21;
  
}

.navbar-nav .nav-link {
  color: white;
}

.navbar-nav .nav-link:hover {
  color: #f8f9fa;
}

.navbar-toggler-icon {
  background-color: white;
}

.navbar-nav .btn-link {
  text-decoration: none;
  color: white;
}

.navbar-nav .btn-link:hover {
  color: #f8f9fa;
}
</style>
