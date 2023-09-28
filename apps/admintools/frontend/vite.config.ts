import { resolve } from 'path';
import fsExtra from 'fs-extra';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    base: '/static/',
    server: {
        host: 'localhost',
        port: 3000,
        open: false,
        https: {
            key: fsExtra.readFileSync(
                '../../../../docker/nginx/certs/cert.key',
            ),
            cert: fsExtra.readFileSync(
                '../../../../docker/nginx/certs/cert.crt',
            ),
        },
        // watch: {
        //     usePolling: true,
        //     disableGlobbing: false,
        // },
    },
    resolve: {
        alias: {
            '@': resolve(__dirname, './src'),
        },
    },
    build: {
        outDir: resolve(__dirname, '../static/admintools'),
        assetsDir: '',
        manifest: true,
        emptyOutDir: true,
        target: 'esnext',
        rollupOptions: {
            input: {
                main: resolve(__dirname, './src/main.tsx'),
            },
        },
    },
});
