import { createRouter, createWebHistory } from 'vue-router';

import AddCourse from '../components/AddCourse.vue';
import UserDashboard from '../components/UserDashboard.vue';
import UserLogin from '../components/UserLogin.vue';
import UserRegister from '../components/UserRegister.vue';

const routes = [
  { path: '/login', component: UserLogin },
  { path: '/register', component: UserRegister },
  { path: '/dashboard', component: UserDashboard },
  { path: '/add-course', component: AddCourse },
  { path: '/', redirect: '/login' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
