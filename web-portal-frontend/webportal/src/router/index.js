import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../views/adminDashboard.vue'),
      meta: { title: 'Dashboard' },
    },
    {
      path: '/editbus/:id',
      name: 'EditBus',
      component: () => import('../views/editBus.vue'),
      meta: { title: 'EditBus' },
      props: true

    },
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/bus/:id',
      name: 'Bus',
      component: () => import('../views/BusView.vue'),
      meta: { title: 'Bus' },
      props: true
    }
    ,
    {
      path: '/bookedseats',
      name: 'BookedSeats',
      component: () => import('../views/bookedSeats.vue'),
      meta: { title: 'BookedSeats' },
    },
    {
      path: '/home',
      name: 'Home',
      component: () => import('../views/HomeView.vue'),
      meta: { title: 'Home' }
    },

    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/Register.vue'),
      meta: { title: 'Signup' },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
      meta: { title: 'Login' },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'notfound',
      component: () => import('../components/NotFound.vue'),
      meta: { title: 'Not Found' }

    }

  ],
})



export default router
