<script lang="ts">
	import type { BookInfo } from '$lib/client/types.gen';
	import BookCard from './BookCard.svelte';

	const { books }: { books: { isbn: string; bookPromise: Promise<BookInfo> }[] } = $props();

	let gallery: HTMLDivElement | undefined = $state();

	$effect(() => {
		if (gallery && books.length) {
			gallery.scrollLeft = gallery.scrollWidth;
		}
	});
</script>

{#if books.length > 0}
	<div class="w-full">
		<h2 class="mb-4 text-center text-2xl font-semibold">Scanned Books</h2>
		<div
			bind:this={gallery}
			class="flex w-full gap-4 overflow-x-auto p-4"
			style="scroll-behavior: smooth;"
		>
			{#each books as { isbn, bookPromise } (isbn)}
				<div class="w-40 flex-shrink-0">
					<BookCard {isbn} book={bookPromise} />
				</div>
			{/each}
		</div>
	</div>
{/if}
