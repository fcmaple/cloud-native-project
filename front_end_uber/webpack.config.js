const path = require("path");
const webpack = require("webpack");
const CopyPlugin = require('copy-webpack-plugin');
const TransferWebpackPlugin = require('transfer-webpack-plugin')
module.exports = {
  entry: ["regenerator-runtime/runtime.js", "./src/index.jsx"],
  mode: "development",
  module: {
    rules: [{
      test: /\.(js|jsx)$/,
      exclude: /(node_modules|bower_components)/,
      loader: "babel-loader",
      options: {
        presets: ["@babel/env"]
      }
    },
    {
      test: /\.css$/,
      use: ["style-loader", "css-loader"]
    }, {
      test: /\.(png|jpg|gif|svg|eot|ttf|woff|woff2)$/,
      loader: 'url-loader',
      options: {
        limit: 10000
      }
    }
    ]
  },
  resolve: {
    extensions: ["*", ".js", ".jsx"],
  },
  output: {
    path: path.resolve(__dirname, "dist/"),
    publicPath: '/',
    filename: "bundle.js"
  },
  devServer: {
    contentBase: path.join(__dirname, "www/"),
    port: 3000,
    publicPath: "http://localhost:3000/",
    historyApiFallback:true,
    hotOnly: true
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new TransferWebpackPlugin([{
      from: 'www'
    },], path.resolve(__dirname)),
    new CopyPlugin([{
        from: './src/lib/config.json',
    }]),
  ]
};