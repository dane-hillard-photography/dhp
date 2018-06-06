const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
    context: __dirname,
    entry: {
        blogPost: path.resolve('assets', 'js', 'blog-post.js'),
        facebookSdk: path.resolve('assets', 'js', 'fb_sdk.js'),
        googleAnalyticsTracking: path.resolve('assets', 'js', 'google_analytics_tracking.js'),
        googleAnalyticsTrackingFlicker: path.resolve('assets', 'js', 'google_analytics_tracking_flicker.js'),
        portfolio: path.resolve('assets', 'js', 'portfolio.js'),
        twitterSdk: path.resolve('assets', 'js', 'twitter_sdk.js'),
        main: path.resolve('assets', 'js', 'site.js')
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
                test: /\.scss$/,
                use: ExtractTextPlugin.extract({
                    use: ['css-loader', 'sass-loader'],
                    fallback: 'style-loader'
                })
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
        new UglifyJsPlugin({
            test: /\.js($|\?)/i,
            sourceMap: true,
            uglifyOptions: {
                warnings: false
            }
        }),
        new ExtractTextPlugin('[name]-[hash:6].css'),
        new BundleTracker({filename: './webpack-stats.json'})
    ]
};
