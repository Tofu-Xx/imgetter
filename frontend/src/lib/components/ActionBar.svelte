<script lang="ts">
  import { store } from "$lib/stores/collector.svelte";

  let downloading = $state(false);

  async function handleDownload() {
    downloading = true;
    try {
      await store.downloadSelected();
    } catch (e) {
      console.error(e);
    } finally {
      downloading = false;
    }
  }
</script>

<div class="fixed bottom-0 left-0 right-0 bg-gray-100/95 dark:bg-gray-800/95 backdrop-blur border-t border-gray-300 dark:border-white/10 p-4 z-50">
  <div class="max-w-6xl mx-auto flex items-center justify-between">
    <div class="flex items-center gap-4">
      <span class="text-sm text-gray-500 dark:text-white/60">
        已选择 <span class="text-blue-500 dark:text-blue-400 font-bold">{store.selectedCount}</span> 张图片
      </span>
      <button class="btn-ghost text-sm" onclick={() => store.selectAll()}>
        <div class="i-mdi-checkbox-marked mr-1"></div>
        全选
      </button>
      <button class="btn-ghost text-sm" onclick={() => store.deselectAll()}>
        <div class="i-mdi-checkbox-blank-outline mr-1"></div>
        取消
      </button>
    </div>

    <button
      class="btn-primary flex items-center gap-2"
      onclick={handleDownload}
      disabled={downloading}
    >
      {#if downloading}
        <div class="i-mdi-loading animate-spin"></div>
        下载中...
      {:else}
        <div class="i-mdi-download"></div>
        下载选中
      {/if}
    </button>
  </div>
</div>
