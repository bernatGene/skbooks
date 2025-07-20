<script lang="ts">
	import type { BookInfo } from '$lib/client/types.gen';

	const UNKNOWN_BOOK: BookInfo = {
		title: 'Unknown Title',
		authors: ['Unknown Author'],
		publisher: 'Unknown Publisher',
		published_date: 'Unknown Date',
		thumbnail: '/no-image-placeholder.svg',
		identifier: ''
	};

	const { isbn, book }: { isbn: string; book: Promise<BookInfo> } = $props();
	let expanded = $state(false);

	function toggleExpanded() {
		expanded = !expanded;
	}
</script>

{#await book}
	<p class="animate-ping">{isbn}</p>
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
