function api() {
  return import.meta.env.VITE_API_URL
}

function websocket() { 
  return import.meta.env.VITE_WEBSOCKET_URL
}

export { api, websocket }