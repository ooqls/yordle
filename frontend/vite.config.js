
import { sveltekit } from '@sveltejs/kit/vite'
import { defineConfig } from 'vite'
import config from './config.js'


export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/api': {
				target: config.urls.api,
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api/, ''),
				headers: {
					accept: 'application/json',
				}
			},
			'/websocket': {
				target: config.urls.websocket,
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/websocket/, ''),
			}
		}
	}
});
