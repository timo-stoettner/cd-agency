const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = (env, argv) => [
  // Main thread (Figma sandbox) — code.ts
  {
    mode: argv.mode || "production",
    entry: "./src/code.ts",
    output: {
      filename: "code.js",
      path: path.resolve(__dirname, "dist"),
      clean: false,
    },
    module: {
      rules: [
        {
          test: /\.ts$/,
          use: "ts-loader",
          exclude: /node_modules/,
        },
      ],
    },
    resolve: {
      extensions: [".ts", ".js"],
    },
    target: "es2020",
  },

  // UI thread (iframe) — ui.ts + ui.html
  {
    mode: argv.mode || "production",
    entry: "./src/ui.ts",
    output: {
      filename: "ui.js",
      path: path.resolve(__dirname, "dist"),
      clean: false,
    },
    module: {
      rules: [
        {
          test: /\.ts$/,
          use: "ts-loader",
          exclude: /node_modules/,
        },
        {
          test: /\.css$/,
          use: ["style-loader", "css-loader"],
        },
      ],
    },
    resolve: {
      extensions: [".ts", ".js"],
    },
    plugins: [
      new HtmlWebpackPlugin({
        template: "./src/ui.html",
        filename: "ui.html",
        inject: "body",
        chunks: ["main"],
      }),
    ],
    target: "web",
  },
];
