import adapter from '@sveltejs/adapter-node';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({}),
		alias: {
			"stores": "./src/lib/stores",
			"$components": "./src/components",
			"$models": "./src/lib/models",
		},
	}
	
};

export default config;
