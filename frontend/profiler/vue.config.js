const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin')


module.exports = {
  devServer: {
    proxy: {
      "/upload-file": {
        target: "http://localhost:5000"
      },
      "/mem-profile": {
        target: "http://localhost:5000"
      }
    }
  },
  configureWebpack: {
    plugins: [
      new MonacoWebpackPlugin({language: 'cpp'})
    ]
  }
};