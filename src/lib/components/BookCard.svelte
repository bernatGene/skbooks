<script lang="ts">
	import type { BookInfo } from '$lib/client/types.gen';

	const { isbn, book }: { isbn: string; book: Promise<BookInfo> } = $props();
	let expanded = $state(false);

	function toggleExpanded() {
		expanded = !expanded;
	}
</script>

{#await book}
	<div
		class="flex h-full flex-col items-center justify-center rounded-lg bg-gray-200 p-4 shadow-md"
	>
		<div class="relative flex h-32 w-full items-center justify-center rounded bg-gray-300">
			<span class="icon-[mdi--loading] size-8 animate-spin text-gray-500"></span>
		</div>
		<div class="mt-2 h-4 w-3/4 rounded bg-gray-300"></div>
		<div class="mt-2 h-3 w-1/2 rounded bg-gray-300"></div>
		<p class="mt-2 text-xs text-gray-500">{isbn}</p>
	</div>
{:then book}
	<div
		class="cursor-pointer overflow-hidden rounded-lg bg-white shadow-md transition-all duration-300"
		onclick={toggleExpanded}
		role="button"
		tabindex="0"
		onkeypress={toggleExpanded}
	>
		<img src={book.thumbnail} alt="Cover of {book.title}" class="h-auto w-full" />
		<div class="p-2">
			<p class="truncate text-center text-sm font-semibold" title={book.title}>
				{book.title}
			</p>
			{#if !expanded}
				<p class="text-center text-xs text-gray-600">{book.identifier}</p>
			{/if}
		</div>

		{#if expanded}
			<div class="border-t border-gray-200 p-2">
				<p class="text-xs"><strong>Authors:</strong> {book.authors.join(', ')}</p>
				<p class="text-xs"><strong>Published:</strong> {book.published_date}</p>
				<p class="text-xs"><strong>Publisher:</strong> {book.publisher}</p>
				<p class="text-xs"><strong>ISBN:</strong> {book.identifier}</p>
			</div>
		{/if}
	</div>
{:catch}
	<div class="text-red-700">Error</div>
{/await}
