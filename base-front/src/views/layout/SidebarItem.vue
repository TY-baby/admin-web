<template>
  <div v-if='!item.hidden && item.meta'>
    <el-submenu v-if='item.children && item.children.length' :index='basePath'>
      <template slot='title'>
        <i :class='item.meta.icon'></i>
        <span>{{ item.meta.title }}</span>
      </template>
      <el-menu-item v-for='child in visibleChildren' :key='child.path' :index='resolvePath(child.path)'>
        {{ child.meta && child.meta.title }}
      </el-menu-item>
    </el-submenu>
    <el-menu-item v-else :index='basePath'>
      <i :class='item.meta.icon'></i>
      <span slot='title'>{{ item.meta.title }}</span>
    </el-menu-item>
  </div>
</template>

<script>
export default {
  props: ['item', 'basePath'],
  computed: {
    visibleChildren() {
      return (this.item.children || []).filter(c => !c.hidden && c.meta)
    }
  },
  methods: {
    resolvePath(routePath) {
      return (this.basePath + '/' + routePath).replace(/\/+/g, '/')
    }
  }
}
</script>
