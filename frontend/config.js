const config = {
  urls: {
    api: "",
    websocket: "",
  },
};

config.urls.api = process.env.API_URL || "http://127.0.0.1:8000";
config.urls.websocket = process.env.WEBSOCKET_URL || "ws://127.0.0.1:8000";

console.dir(config)
export default config;