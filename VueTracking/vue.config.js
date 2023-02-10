module.exports={
  productionSourceMap: true,
  devServer: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:3000",
        changOrigin: true,
        pathRewrite: {
          "^/api": "",
        }
      }
    }
}
}