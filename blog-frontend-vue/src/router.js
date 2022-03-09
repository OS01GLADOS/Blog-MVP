import { createWebHistory, createRouter } from 'vue-router'
import loginVue from './components/Authentification/login.vue';
import registrationVue from './components/Authentification/registration.vue';
import showBlogsVue from './components/Blogs/showBlogs.vue'
import showOneBlogVue from './components/Blogs/showOneBlog.vue';
import profileVue from './components/Authentification/profile.vue';
import authorBlogsVue from './components/Blogs/showAuthorPosts.vue';
import createUpdateBlogVue from './components/Blogs/CreateUpdateBlog.vue';
import deleteBlogVue from './components/Blogs/DeleteBlog.vue';

const routes = [
    { path: '/', name: 'Home', component: showBlogsVue},
    { path: '/login', name: 'login', component: loginVue },
    { path: '/register', name: 'register', component: registrationVue },
    { path: '/blog/:id', name: 'showBlog', component: showOneBlogVue},
    { path: '/profile/', name: 'userProfile', component: profileVue },
    { path: '/author/blogs/', name: 'authorBlog', component: authorBlogsVue },
    { path: '/blog/new/', name: 'createBlog', component: createUpdateBlogVue },
    { path: '/blog/:id/update', name: 'updateBlog', component: createUpdateBlogVue },
    { path: '/blog/:id/delete', name: 'deleteBlog', component: deleteBlogVue},
];

const router = createRouter({ history: createWebHistory(), routes });
export default router