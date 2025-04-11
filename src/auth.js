import { reactive } from 'vue';

export const auth = reactive({
  isLoggedIn: localStorage.getItem('isLoggedIn') === 'true'
});

export function setLoginState(value) {
  auth.isLoggedIn = value;
  localStorage.setItem('isLoggedIn', value);
}

export function logoutUser() {
    auth.isLoggedIn = false;
    localStorage.removeItem('isLoggedIn');
  }


  // Function to get the JWT token from localStorage
export function getToken() {
  return localStorage.getItem('jwt_token');
}

// Function to set the JWT token in localStorage
export function setToken(token) {
  localStorage.setItem('jwt_token', token);
}

// Function to remove the JWT token from localStorage (logout)
export function removeToken() {
  localStorage.removeItem('jwt_token');
}

export function setUserId(userId) {
  localStorage.setItem('user_id', userId);
}

export function removeUserId() {
  localStorage.removeItem('user_id');
}