const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCssPlugin = require('optimize-css-assets-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const TerserPlugin = require('terser-webpack-plugin');
const webpack = require('webpack');

module.exports = {
    context: __dirname,
    mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
    optimization: {
        minimize: process.env.NODE_ENV === 'production',
        minimizer: [
            new TerserPlugin({
                test: /\.js($|\?)/i
            }),
            new OptimizeCssPlugin()
        ]
    },
    entry: {
        blogPost: path.resolve('assets', 'js', 'blog-post.js'),
        facebookSdk: path.resolve('assets', 'js', 'fb_sdk.js'),
        portfolio: path.resolve('assets', 'js', 'portfolio.js'),
        twitterSdk: path.resolve('assets', 'js', 'twitter_sdk.js'),
        main: path.resolve('assets', 'js', 'index.js')
    },
    output: {
        path: path.resolve('assets', 'dist'),
        filename: '[name]-bundle-[hash:6].js'
    },
    module: {
        rules: [
            {
                enforce: 'pre',
                test: /\.js$/,
                loader: 'eslint-loader',
                exclude: /node_modules/
            },
            {
                test: /\.s?css$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                    },
                    'css-loader',
                    'sass-loader',
                ],
            },
            {
                test: /\.(png|jpg|jpeg|gif|svg|woff|woff2|eot|ttf)$/,
                loader: 'file-loader'
            },
            {
                test: /\.js$/,
                use: ['babel-loader']
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jquery: 'jquery',
            'window.jQuery': 'jquery',
            jQuery:'jquery'
        }),
        new MiniCssExtractPlugin('[name]-[hash:6].css'),
        new BundleTracker({filename: './webpack-stats.json'})
    ]
};
