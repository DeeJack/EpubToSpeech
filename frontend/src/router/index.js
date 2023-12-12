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
    path: '/reading',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Reading',
        component: () => import(/* webpackChunkName: "home" */ '@/views/ReadingPane.vue'),
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
        component: () => import(/* webpackChunkName: "home" */ '@/views/ToSpeechForm.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
