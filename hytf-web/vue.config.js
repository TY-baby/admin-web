const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: '/',
  outputDir: 'dist',
  assetsDir: 'static',
  lintOnSave: false,
  productionSourceMap: false,
  devServer: {
    host: '0.0.0.0',
    port: 8081,
    open: true,
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_BASE || 'http://127.0.0.1:8080',
        changeOrigin: true
      }
    }
  }
})