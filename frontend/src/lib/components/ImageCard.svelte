<script lang="ts">
  import type { ImageInfo } from "$lib/types";
  import { store } from "$lib/stores/collector.svelte";

  let { image }: { image: ImageInfo } = $props();

  const isSelected = $derived(store.selectedImages.includes(image.src));
</script>

<button
  class="card relative group cursor-pointer text-left {isSelected ? 'border-blue-500 bg-blue-500/10' : ''}"
  onclick={() => store.toggleSelection(image.src)}
>
  <div class="aspect-square overflow-hidden bg-gray-100 dark:bg-white/5">
    {#if image.thumbnail_url}
      <img
        src={image.thumbnail_url}
        alt={image.alt}
        loading="lazy"
        class="w-full h-full object-cover transition-transform group-hover:scale-105"
        onerror={(e) => { (e.target as HTMLImageElement).style.display = "none"; }}
      />
    {:else}
      <div class="w-full h-full flex items-center justify-center text-gray-400">
        <div class="i-mdi-image-off text-2xl"></div>
      </div>
    {/if}
  </div>

  <div class="absolute top-2 right-2">
    <div
      class="w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all {isSelected ? 'border-blue-500 bg-blue-500' : 'border-gray-300 dark:border-white/30 bg-gray-200 dark:bg-black/30'}"
    >
      {#if isSelected}
        <div class="i-mdi-check text-white text-xs"></div>
      {/if}
    </div>
  </div>

  <div class="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
    <div class="i-mdi-eye text-white text-2xl"></div>
  </div>
</button>
