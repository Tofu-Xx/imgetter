import { svelte } from "@sveltejs/vite-plugin-svelte";
import UnoCSS from "unocss/vite";
import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [UnoCSS(), svelte()],
  resolve: {
    alias: {
      $lib: resolve("./src/lib"),
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8002",
        changeOrigin: true,
      },
    },
  },
});
