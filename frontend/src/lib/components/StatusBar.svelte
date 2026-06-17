<script lang="ts">
  import { store } from "$lib/stores/collector.svelte";
</script>

<div class="fixed bottom-0 left-0 bg-gray-100/95 dark:bg-gray-800/95 backdrop-blur border-t border-r border-gray-300 dark:border-white/10 px-3 py-1.5 text-xs text-gray-400 dark:text-white/40 z-40 rounded-tr-lg">
  {#if store.isLoading}
    <span class="text-blue-500 dark:text-blue-400">{store.loadingMessage}</span>
  {:else if store.pageTitle}
    <span>{store.pageTitle}</span>
    <span class="mx-1">·</span>
    <span>{store.images.length} 张图片</span>
  {:else}
    <span>ImGetter v0.1.0</span>
  {/if}
</div>
