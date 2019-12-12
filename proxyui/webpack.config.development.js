'use strict';

var webpack = require('webpack');
var config = require('./webpack.config.base.js');

if (process.env.NODE_ENV !== 'test') {
  config.entry = [
    'babel-polyfill',
    'react-hot-loader/patch',
    'webpack-dev-server/client?http://localhost:4000',
    'webpack/hot/dev-server'
  ].concat(config.entry);
} else {
  config.entry = [
    'babel-polyfill'
  ].concat(config.entry);
}

config.devtool = 'cheap-module-eval-source-map';

config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NamedModulesPlugin()
]);

config.module.rules = config.module.rules.concat([
  {test: /\.jsx?$/, loaders: [ 'babel-loader'], exclude: /node_modules/}
]);

module.exports = config;
