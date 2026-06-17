import { svelte } from "@sveltejs/vite-plugin-svelte";
import { resolve } from "path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [svelte()],
  resolve: {
    alias: {
      $lib: resolve("./src/lib"),
    },
  },
  test: {
    environment: "jsdom",
    include: ["src/**/*.{test,spec}.{js,ts}"],
  },
});
