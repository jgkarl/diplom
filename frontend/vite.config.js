import { defineConfig } from "vite";
import { resolve } from "path";
import vue from "@vitejs/plugin-vue";
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  base: "/static/",
  plugins: [vue(), tailwindcss()],
  build: {
    manifest: "manifest.json",
    outDir: resolve("./frontend/dist"),
    rollupOptions: {
      input: {
        main: resolve("./frontend/src/main.js"),
      },
    },
    assetsInlineLimit: 0, // Ensure all assets are copied to the output directory
  },
  assetsInclude: ["./frontend/src/assets"],
  resolve: {
    alias: {
      '@': resolve(__dirname, './frontend/src'),
    },
  },
});
