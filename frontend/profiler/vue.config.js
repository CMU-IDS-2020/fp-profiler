module.exports = {
  devServer: {
    proxy: {
      "/upload-file": {
        target: "http://localhost:5000"
      }
    }
  }
};