import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '首页', icon: 'dashboard' }
    }]
  },

  {
    path: '/blockchain',
    component: Layout,
    redirect: '/blockchain/blocks',
    name: 'BlockChain',
    meta: { title: '区块链信息', icon: 'el-icon-s-help', roles: ['admin'] },
    children: [
      {
        path: 'blocks',
        name: 'Blocks',
        component: () => import('@/views/blockchain/blocks/index'),
        meta: { title: '区块链', icon: 'table', roles: ['admin', 'producer', 'transporter', 'saler'] }
      },
      {
        path: 'out-blocks',
        name: 'OutBlocks',
        component: () => import('@/views/blockchain/outblocks/index'),
        meta: { title: '链外的区块', icon: 'table', roles: ['admin', 'producer', 'transporter', 'saler'] }
      },
    ]
  },
  // 404 page must be placed at the end !!!
  // { path: '*', redirect: '/404', hidden: true }
]


export const asyncRoutes = [
  
  {
    path: '/users',
    component: Layout,
    meta: {roles: ['admin'] },
    children: [
      {
        path: 'index',
        name: 'Users',
        component: () => import('@/views/users/index'),
        meta: { title: '用户汇总', icon: 'table'}
      },
    ]
  },

  {
    path: '/commodity',
    component: Layout,
    redirect: '/commodity/commodities',
    name: 'Commodity',
    meta: { title: '商品信息', icon: 'el-icon-s-help', roles: ['admin', 'saler', 'transporter', 'producer'] },
    children: [
      {
        path: 'commodities',
        name: 'Commodities',
        component: () => import('@/views/commodity/commodities/index'),
        meta: { title: '商品信息汇总', icon: 'table', roles: ['admin', 'saler', 'transporter', 'producer'] }
      },
      {
        path: 'logistics',
        name: 'Logistics',
        component: () => import('@/views/commodity/Logistics/index'),
        meta: { title: '物流信息', icon: 'tree', roles: ['admin', 'saler', 'transporter', 'producer']}
      }
    ]
  },

  {
    path: '/producer',
    component: Layout,
    redirect: '/producer/producers',
    name: 'Producer',
    meta: { title: '生产信息', icon: 'el-icon-s-help', roles: ['admin', 'producer'] },
    children: [
      {
        path: 'producers',
        name: 'Producers',
        component: () => import('@/views/producer/producers/index'),
        meta: { title: '生产者', icon: 'table', roles: ['admin'] }
      },
      {
        path: 'produceSummary',
        name: 'ProduceSummary',
        component: () => import('@/views/producer/produceSummary/index'),
        meta: { title: '生产汇总', icon: 'table', roles: ['admin', 'producer'] }
      },
      {
        path: 'producerDetail',
        name: 'ProducerDetail',
        component: () => import('@/views/producer/producerDetail/index'),
        meta: { title: '生产详情', icon: 'table', roles: ['admin', 'producer'] }
      },
      {
        path: 'produceTH',
        name: 'ProduceTH',
        component: () => import('@/views/producer/produceTH/index'),
        meta: { title: '温湿度', icon: 'table', roles: ['admin', 'producer'] }
      },
      {
        path: 'uploadInfo',
        name: 'UploadProduceInfo',
        component: () => import('@/views/producer/uploadProduceInfo/index'),
        meta: { title: '添加生产信息', icon: 'table', roles: ['admin', 'producer'] }
      },
    ]
  },

  {
    path: '/saler',
    component: Layout,
    redirect: '/saler/salers',
    name: 'Saler',
    meta: { title: '销售信息', icon: 'el-icon-s-help', roles: ['admin', 'saler'] },
    children: [
      {
        path: 'salers',
        name: 'Salers',
        component: () => import('@/views/saler/salers/index'),
        meta: { title: '销售商', icon: 'table', roles: ['admin'] }
      },
      {
        path: 'salerCommodity',
        name: 'SalerCommodity',
        component: () => import('@/views/saler/salerCommodity/index'),
        meta: { title: '销售商品汇总', icon: 'table', roles: ['admin', 'saler'] }
      },
    ]
  },


  {
    path: '/charts',
    component: Layout,
    redirect: '/charts/produce',
    name: 'Charts',
    meta: { title: '统计图表', icon: 'el-icon-s-help', roles: ['admin', 'producer'] },
    children: [
      {
        path: 'produce',
        name: 'ProduceChart',
        component: () => import('@/views/charts/produce/index'),
        meta: { title: '生产信息图表', icon: 'table', roles: ['admin', 'producer'] }
      },
    ]
  },
]


const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
