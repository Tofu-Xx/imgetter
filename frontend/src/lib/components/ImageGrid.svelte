<script lang="ts">
  import ImageCard from "./ImageCard.svelte";
  import { store } from "$lib/stores/collector.svelte";
</script>

<div class="flex items-center justify-between mb-2">
  <h2 class="text-sm text-gray-500 dark:text-white/50">
    共 {store.filteredImages.length} 张图片
    {#if store.filteredImages.length !== store.images.length}
      （已过滤 {store.images.length - store.filteredImages.length} 张）
    {/if}
  </h2>
  <button class="btn-ghost text-sm" onclick={() => store.selectAll()}>
    <div class="i-mdi-checkbox-marked mr-1"></div>
    全选
  </button>
</div>

<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
  {#each store.filteredImages as image (image.src)}
    <ImageCard {image} />
  {/each}
</div>

{#if store.filteredImages.length === 0 && !store.isLoading}
  <div class="text-center py-12 text-gray-400 dark:text-white/30">
    <div class="i-mdi-image-off text-4xl mb-2 mx-auto"></div>
    <p>没有找到符合条件的图片</p>
  </div>
{/if}
