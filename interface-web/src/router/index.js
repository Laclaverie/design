import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Picture from '../views/Picture.vue'
import SearchResult from "@/views/SearchResult";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/pictures',
        name: 'Picture',
        component: Picture,
    },
    {
        path: '/picture',
        name: 'SearchResult',
        component: SearchResult,
        props: route => ({query: route.query.q})
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
