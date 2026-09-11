const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  // 关键：与 nginx 的 location /admin/ 保持一致
  publicPath: '/admin/',
  transpileDependencies: true,
  lintOnSave: false,
  devServer: {
    port: 8081,
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true }
    }
  }
})