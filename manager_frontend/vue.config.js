module.exports = {
  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args => {
        args[0].title = '智慧活动室'
        return args
      })
  },
  devServer: {
    proxy: {
      '/api': {
        target: '', // ！本机调试时填写的后端url
        ws: true,
        changeOrigin: true
      }
    }
  }
}