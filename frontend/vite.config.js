
import { sveltekit } from '@sveltejs/kit/vite'
import { defineConfig } from 'vite'
// import { api, websocket } from './config.js'


export default defineConfig({
	plugins: [sveltekit()],
	envDir: './env/',
	server: {
		port: 8080,
		proxy: {
			'/api': {
				target: 'http://localhost:8000',
				changeOrigin: true,
				headers: {
					accept: 'application/json',
				}
			},
			'/websocket': {
				target: 'ws://localhost:8000',
				changeOrigin: true,
			}
		}
	}
});
