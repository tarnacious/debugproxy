'use strict';

var webpack = require('webpack');
var config = require('./webpack.config.base.js');

var SaveAssetsJson = require('assets-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');


config.bail = true;
config.profile = false;
config.devtool = '#source-map';

config.output = {
  path: './dist/client',
  publicPath: '/',
  filename: 'main.js'
};

config.entry = [
  'babel-polyfill'
].concat(config.entry);

config.plugins = config.plugins.concat([
  new webpack.LoaderOptionsPlugin({
       debug: false
     }),
  new webpack.optimize.OccurrenceOrderPlugin(true),
  new webpack.optimize.UglifyJsPlugin({
    output: {
      comments: false
    },
    compress: {
      warnings: false,
      screw_ie8: true
    }
  }),
  new SaveAssetsJson({
    path: process.cwd(),
    filename: 'assets.json'
  }),
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('production')
    }
  })
]);

config.module.rules = config.module.rules.concat([
  {
    test: /\.(js|jsx)$/,
    exclude: /node_modules/,
    loader: "babel-loader",
    query: {
        presets: ['es2015', 'react']
    }
  }
]);

module.exports = config;
