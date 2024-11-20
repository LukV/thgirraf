import { createRouter, createWebHistory } from 'vue-router';
import MainContent from '@/components/MainContent.vue';
import AuthOverlay from '@/components/AuthOverlay.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: MainContent,
  },
  {
    path: '/feed',
    name: 'Feed',
    component: MainContent,
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: AuthOverlay,
    props: { mode: 'signup' },
  },
  {
    path: '/login',
    name: 'Login',
    component: AuthOverlay,
    props: { mode: 'login' },
  },
  {
    path: '/request-password-reset',
    name: 'RequestPasswordReset',
    component: AuthOverlay,
    props: { mode: 'request-reset' },
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: AuthOverlay,
    props: { mode: 'reset' },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
