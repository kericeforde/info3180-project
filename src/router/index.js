import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProfileForm from '../components/ProfileForm.vue'
import DashboardView from '../views/DashboardView.vue'
import MyProfileView from '../views/MyProfileView.vue'
import ProfileDetailsView from '../views/ProfileDetailsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: HomeView
    },
    {
      path: '/logout',
      name: 'logout',
      component: HomeView
    },
    {
      path: '/register',
      name: 'register',
      component: HomeView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/profiles/new',
      name: 'profileForm',
      component: ProfileForm,
      meta: { requiresAuth: true }
    },
    {
      path: '/users/:users_id',
      name: 'myProfileView',
      component: MyProfileView,
      meta: { requiresAuth: true }
    },
    {path: '/profiles/:profile_id',
      name: 'profileDetailsView',
      component: ProfileDetailsView,
      meta: { requiresAuth: true }
      
    }

  ]
   
})
router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('isLoggedIn')==='true'; 

  if (to.meta.requiresAuth && !loggedIn) {
    next({ name: 'home' }); 
  } else {
    next();
  }})
export default router
