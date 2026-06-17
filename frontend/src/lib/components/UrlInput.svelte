<script lang="ts">
  import { store } from "$lib/stores/collector.svelte";

  // oxlint-disable-next-line eslint-no-unassigned-vars -- bind:this assigns at runtime
  let inputEl: HTMLInputElement;
  let displayUrl = $state("");

  function fixUrl(raw: string): string {
    let url = raw.trim();
    if (!url) return "";
    if (/^[a-zA-Z]+:\/\//.test(url)) return url;
    if (/^localhost(:\d+)?(\/.*)?$/.test(url)) return "http://" + url;
    return "https://" + url;
  }

  function handleSubmit(e: Event) {
    e.preventDefault();
    const fixed = fixUrl(displayUrl);
    if (!fixed || store.isLoading) return;
    store.url = fixed;
    store.parse(fixed);
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Escape") {
      displayUrl = "";
      inputEl?.focus();
    }
  }
</script>

<form class="flex gap-2" onsubmit={handleSubmit}>
  <div class="flex-1 relative">
    <div class="i-mdi-link absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-white/40"></div>
    <input
      bind:this={inputEl}
      bind:value={displayUrl}
      type="text"
      placeholder="输入网址，如 baidu.com、example.com/gallery"
      class="w-full pl-10 pr-4 py-3 bg-gray-100 dark:bg-white/5 border border-gray-300 dark:border-white/10 rounded-lg text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-white/30 focus:outline-none focus:border-blue-500 transition-colors"
      disabled={store.isLoading}
      onkeydown={handleKeydown}
    />
  </div>
  <button
    type="submit"
    class="btn-primary flex items-center gap-2"
    disabled={store.isLoading || !displayUrl.trim()}
  >
    {#if store.isLoading}
      <div class="i-mdi-loading animate-spin"></div>
      解析中...
    {:else}
      <div class="i-mdi-magnify"></div>
      解析
    {/if}
  </button>
</form>

{#if store.error}
  <div class="mt-2 p-3 bg-red-50 dark:bg-red-500/10 border border-red-300 dark:border-red-500/30 rounded-lg text-red-600 dark:text-red-400 text-sm flex items-center gap-2">
    <div class="i-mdi-alert-circle"></div>
    {store.error}
  </div>
{/if}
