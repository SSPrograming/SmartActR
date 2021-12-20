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
        target: 'http://120.53.231.51:8888/',
        ws: true,
        changeOrigin: true
      }
    }
  }
}