<script lang="ts">
  import UrlInput from "$lib/components/UrlInput.svelte";
  import ImageGrid from "$lib/components/ImageGrid.svelte";
  import ActionBar from "$lib/components/ActionBar.svelte";
  import StatusBar from "$lib/components/StatusBar.svelte";
  import { store } from "$lib/stores/collector.svelte";

  let dark = $state(true);

  function initDark() {
    if (typeof localStorage !== "undefined") {
      dark = localStorage.theme === "dark" || !localStorage.theme;
    }
    applyDark();
  }

  function applyDark() {
    document.documentElement.classList.toggle("dark", dark);
    if (typeof localStorage !== "undefined") {
      localStorage.theme = dark ? "dark" : "light";
    }
  }

  function toggleDark() {
    dark = !dark;
    applyDark();
  }

  initDark();
</script>

<div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white flex flex-col">
  <header class="border-b border-gray-200 dark:border-white/10 p-4">
    <div class="max-w-6xl mx-auto flex items-center gap-3">
      <div class="i-mdi-image-multiple text-2xl text-blue-500 dark:text-blue-400"></div>
      <h1 class="text-xl font-bold">imgetter</h1>
      <span class="text-sm text-gray-400 dark:text-white/40">网页图片采集工具</span>
      <div class="ml-auto flex items-center gap-2">
        <a
          href="https://github.com/Tofu-Xx/imgetter"
          target="_blank"
          rel="noopener noreferrer"
          class="p-2 rounded-lg border border-gray-300 dark:border-white/20 hover:bg-gray-100 dark:hover:bg-white/10 transition-colors"
        >
          <div class="i-mdi-github text-xl text-gray-600 dark:text-white/70"></div>
        </a>
        <button
          class="p-2 rounded-lg border border-gray-300 dark:border-white/20 hover:bg-gray-100 dark:hover:bg-white/10 transition-colors"
          onclick={toggleDark}
        >
          {#if dark}
            <div class="i-mdi-weather-sunny text-yellow-400 text-xl"></div>
          {:else}
            <div class="i-mdi-weather-night text-gray-600 text-xl"></div>
          {/if}
        </button>
      </div>
    </div>
  </header>

  <main class="flex-1 max-w-6xl mx-auto w-full p-4 flex flex-col gap-4">
    <UrlInput />
    {#if store.images.length > 0}
      <ImageGrid />
    {:else if !store.isLoading && store.pageUrl}
      <div class="text-center py-16">
        <div class="i-mdi-image-search text-6xl text-gray-300 dark:text-white/20 mb-4 mx-auto"></div>
        <p class="text-gray-500 dark:text-white/40 text-lg">未找到图片</p>
        <p class="text-gray-400 dark:text-white/30 text-sm mt-2">该页面没有可提取的图片</p>
      </div>
    {/if}
  </main>

  {#if store.selectedCount > 0}
    <ActionBar />
  {/if}

  <StatusBar />
</div>
