import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";
import fs from "fs";
import { protocol } from "socket.io-client";
// import { api, websocket } from './config.js'

export default defineConfig({
  plugins: [sveltekit()],
  envDir: "./env/",
  server: {
    host: "localhost",
    port: 8080,
    https: {
      key: fs.readFileSync("certs/localhost-key.pem"),
      cert: fs.readFileSync("certs/localhost.pem"),
    },
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        headers: {
          accept: "application/json",
        },
      },
      "/websocket": {
        target: "ws://localhost:8000",
        changeOrigin: true,
        ws: {
          protocol: "wss",
        }
      },
    },
  },
});
