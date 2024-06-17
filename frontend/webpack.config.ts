import path from 'path'
import {Configuration} from 'webpack'
import HtmlWebpackPlugin from 'html-webpack-plugin'

type CustomDevServer = {
  historyApiFallback: boolean
  port: number
}

interface CustomWebpackConfiguration extends Configuration {
  devServer?: CustomDevServer
}

const config: CustomWebpackConfiguration = {
  mode: (process.env.NODE_ENV as 'production' | 'development' | undefined) ?? 'production',
  entry: './src/index.tsx',
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  output: {
    filename: 'bundle.[contenthash].js',
    path: path.resolve(__dirname, 'dist'),
  },
  devServer: {
    historyApiFallback: true,
    port: 80,
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.resolve(__dirname, 'public/index.html'),
    }),
  ],
}

export default config
