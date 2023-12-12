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
    path: '/option',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Option',
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
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
