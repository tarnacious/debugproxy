'use strict';

var path = require('path');
var webpack = require('webpack');
var config = require('./webpack.config.base.js');

var SaveAssetsJson = require('assets-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');


config.bail = true;
config.profile = false;
config.devtool = '#source-map';
config.mode = 'production';

config.output = {
  path: path.join(process.cwd(), '/dist/client'),
  publicPath: '/',
  filename: 'main.js'
};

config.entry = [
].concat(config.entry);

config.plugins = config.plugins.concat([
  new webpack.LoaderOptionsPlugin({
       debug: false
     }),
  new webpack.optimize.OccurrenceOrderPlugin(true),
  new SaveAssetsJson({
    path: process.cwd(),
    filename: 'assets.json'
  })
]);

config.module.rules = config.module.rules.concat([
  {
    test: /\.(js|jsx)$/,
    exclude: /node_modules/,
    loader: "babel-loader",
    query: {
        presets: ['@babel/preset-env', '@babel/preset-react', '@babel/preset-flow']
    }
  }
]);

module.exports = config;
