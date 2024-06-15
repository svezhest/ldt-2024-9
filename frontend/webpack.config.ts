import path from 'path'
import {Configuration} from 'webpack'
import CopyWebpackPlugin from 'copy-webpack-plugin'

type CustomDevServer = {
  historyApiFallback: boolean
}

interface CustomWebpackConfiguration extends Configuration {
  devServer?: CustomDevServer
}

const config: CustomWebpackConfiguration = {
  mode: (process.env.NODE_ENV as 'production' | 'development' | undefined) ?? 'production',
  entry: './src/index.tsx',
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
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  devServer: {
    historyApiFallback: true,
  },
  plugins: [
    new CopyWebpackPlugin({
      patterns: [{from: 'public'}],
    }),
  ],
}

export default config
