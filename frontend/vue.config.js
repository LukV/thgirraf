const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: (config) => {
    config.plugin('html').tap((args) => {
      args[0].title = 'Standout & Deliver'; // Set your custom page title
      args[0].templateParameters = {
        BASE_URL: process.env.BASE_URL || '/' // Set BASE_URL for use in the HTML template
      };
      return args;
    });
  }
});
