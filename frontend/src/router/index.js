// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import(/* webpackChunkName: "home" */ '@/views/Upload.vue'),
      },
    ],
  },
  {
    path: '/reader',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Reader',
        component: () => import(/* webpackChunkName: "home" */ '@/views/ReadingPane.vue'),
      },
    ],
  },
  {
    path: '/form',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Form',
        component: () => import(/* webpackChunkName: "home" */ '@/views/ToSpeechForm.vue'),
      },
    ],
  },
  {
    path: '/tts',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'TTS',
        component: () => import(/* webpackChunkName: "home" */ '@/views/TTS.vue'),
      },
    ],
  },
  {
    path: '/search',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Search',
        component: () => import(/* webpackChunkName: "home" */ '@/views/Search'),
      },
    ],
  },
  {
    // Not found handler
    path: '/:pathMatch(.*)*',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'NotFound',
        component: () => import('@/views/NotFound.vue'),
      },
    ],
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
