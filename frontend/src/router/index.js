/**
 * Vue Router configuration.
 *
 * Defines all public and admin routes for the HPLS website.
 * Admin routes are protected by a `requiresAuth` meta flag that
 * is checked in the global `beforeEach` navigation guard.
 *
 * Static pages (Rekordi, Poredak, O nama sub-pages, Kontakt) all
 * reuse the generic PageView component — the slug is passed via
 * `route.meta.slug` so a single component handles all of them.
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// -- Public views -----------------------------------------------------------
import HomeView from '../views/HomeView.vue'
import NewsListView from '../views/NewsListView.vue'
import PostView from '../views/PostView.vue'
import CalendarView from '../views/CalendarView.vue'
import PageView from '../views/PageView.vue'
import DocumentsView from '../views/DocumentsView.vue'
import LoginView from '../views/LoginView.vue'
import NotFoundView from '../views/NotFoundView.vue'

// -- Admin views ------------------------------------------------------------
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import PostEditor from '../views/admin/PostEditor.vue'
import PagesList from '../views/admin/PagesList.vue'
import PageEditor from '../views/admin/PageEditor.vue'
import DocumentsManager from '../views/admin/DocumentsManager.vue'

const routes = [
  // ── Public routes ──────────────────────────────────────────────────────
  { path: '/', name: 'home', component: HomeView },
  { path: '/novosti', name: 'news', component: NewsListView },
  { path: '/novosti/:slug', name: 'post', component: PostView },
  { path: '/kalendar', name: 'calendar', component: CalendarView },
  { path: '/kalendar/:slug', name: 'calendar-post', component: PostView },

  // Static pages — each reuses PageView with a slug from route.meta.
  { path: '/rekordi', name: 'rekordi', component: PageView, meta: { slug: 'rekordi' } },
  { path: '/poredak', name: 'poredak', component: PageView, meta: { slug: 'poredak' } },

  // "O nama" sub-pages (grouped under the dropdown menu)
  {
    path: '/o-nama/osnivanje-kluba',
    name: 'osnivanje-kluba',
    component: PageView,
    meta: { slug: 'osnivanje-kluba' },
  },
  {
    path: '/o-nama/pravila',
    name: 'pravila',
    component: PageView,
    meta: { slug: 'pravila' },
  },
  {
    path: '/o-nama/anti-doping',
    name: 'anti-doping',
    component: PageView,
    meta: { slug: 'anti-doping' },
  },
  {
    path: '/o-nama/registracija-natjecatelja',
    name: 'registracija-natjecatelja',
    component: PageView,
    meta: { slug: 'registracija-natjecatelja' },
  },
  {
    path: '/o-nama/clanstvo',
    name: 'clanstvo',
    component: PageView,
    meta: { slug: 'clanstvo' },
  },
  {
    path: '/o-nama/pristup-informacijama',
    name: 'pristup-informacijama',
    component: PageView,
    meta: { slug: 'pristup-informacijama' },
  },

  { path: '/dokumenti', name: 'documents', component: DocumentsView },
  { path: '/kontakt', name: 'kontakt', component: PageView, meta: { slug: 'kontakt' } },
  { path: '/prijava', name: 'login', component: LoginView },

  // ── Admin routes (require authentication) ──────────────────────────────
  {
    path: '/admin',
    name: 'admin',
    component: AdminDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/posts/new',
    name: 'post-create',
    component: PostEditor,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/posts/:id/edit',
    name: 'post-edit',
    component: PostEditor,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/pages',
    name: 'pages-list',
    component: PagesList,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/pages/:id/edit',
    name: 'page-edit',
    component: PageEditor,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/documents',
    name: 'documents-manager',
    component: DocumentsManager,
    meta: { requiresAuth: true },
  },

  // ── Catch-all 404 ─────────────────────────────────────────────────────
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // Always scroll to the top when navigating to a new page.
  scrollBehavior() {
    return { top: 0 }
  },
})

/**
 * Global navigation guard — redirects unauthenticated users
 * away from admin routes to the login page.
 */
router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isAuthenticated) {
      return { name: 'login' }
    }
  }
})

export default router
