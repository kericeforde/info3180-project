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
