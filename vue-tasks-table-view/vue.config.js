const { defineConfig } = require('@vue/cli-service')
const path = require('path');

module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: '/Users/hazadus/PycharmProjects/journal/static/vue/tasks-table-view/',  // STATIC_PATH + path to build
  outputDir: path.resolve(__dirname, '../static/vue/tasks-table-view/'), // output to 'static' directory
  filenameHashing: false,
  runtimeCompiler: true,
  devServer: {
    devMiddleware: {
      writeToDisk: true,
    }
  },
});
