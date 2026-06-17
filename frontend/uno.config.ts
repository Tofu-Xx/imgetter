import { defineConfig, presetIcons, presetWind4 } from "unocss";

export default defineConfig({
  content: {
    filesystem: ["./src/**/*.{svelte,ts,js,html}"],
  },
  presets: [
    presetWind4({
      dark: "class",
    }),
    presetIcons({
      extraProperties: {
        display: "inline-block",
        "vertical-align": "middle",
      },
    }),
  ],
  shortcuts: {
    "btn-primary":
      "px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors cursor-pointer",
    "btn-ghost":
      "px-4 py-2 text-gray-500 dark:text-white/60 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/10 rounded-lg transition-colors cursor-pointer",
    card: "bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-lg overflow-hidden hover:border-blue-400 dark:hover:border-white/20 transition-all",
  },
});
