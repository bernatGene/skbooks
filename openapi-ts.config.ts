import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
	input: {
		path: 'http://localhost:8000/openapi.json',
		filters: {
			tags: { exclude: ['admin'] }
		}
	},
	output: { path: 'src/lib/client', format: 'prettier' },
	plugins: ['@hey-api/client-fetch']
});
