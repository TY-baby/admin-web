<template>
  <div v-if='!item.hidden'>
    <el-submenu v-if='item.children && item.children.length' :index='basePath'>
      <template slot='title'>
        <i :class='item.meta && item.meta.icon'></i>
        <span>{{ item.meta.title }}</span>
      </template>
      <el-menu-item v-for='child in item.children' :key='child.path' :index='resolvePath(child.path)'>
        {{ child.meta.title }}
      </el-menu-item>
    </el-submenu>
    <el-menu-item v-else :index='basePath'>
      <i :class='item.meta && item.meta.icon'></i>
      <span slot='title'>{{ item.meta.title }}</span>
    </el-menu-item>
  </div>
</template>

<script>
export default {
  props: ['item', 'basePath'],
  methods: {
    resolvePath(routePath) {
      return (this.basePath + '/' + routePath).replace(/\/+/g, '/')
    }
  }
}
</script>
