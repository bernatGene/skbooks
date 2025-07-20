<script lang="ts">
	import { getBookByIsbnGet } from '$lib/client/sdk.gen';
	import type { BookInfo } from '$lib/client/types.gen';
	import BookCard from '$lib/components/BookCard.svelte';
	import BarcodeScanner from '$lib/components/BarcodeScanner.svelte';

	const books = $state<Promise<BookInfo>[]>([]);
	const scannedBarcodes = new Set<string>();
	let scannedIsbn = $state('');

	const fetchBookInfo = async (isbn: string): Promise<BookInfo> => {
		const { data, error } = await getBookByIsbnGet({ path: { isbn: isbn } });
		if (data) return data;
		throw error;
	};
	let fetchInfo: null | Promise<BookInfo> = $state(null);

	$effect(() => {
		async function handleNewIsbn() {
			if (scannedIsbn && !scannedBarcodes.has(scannedIsbn)) {
				scannedBarcodes.add(scannedIsbn);
				fetchInfo = fetchBookInfo(scannedIsbn);
				books.push(fetchInfo);
			}
		}
		handleNewIsbn();
	});
</script>

<div class="container mx-auto flex max-w-4xl flex-col items-center gap-8 p-4">
	<h1 class="text-3xl font-bold">Svelte Barcode Scanner</h1>

	<BarcodeScanner bind:isbn={scannedIsbn} />

	{#if books.length > 0}
		<div class="w-full">
			<h2 class="mb-4 text-center text-2xl font-semibold">Scanned Books</h2>
			<div class="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
				{#each books as book}
					<BookCard isbn={scannedIsbn} {book} />
				{/each}
			</div>
		</div>
	{/if}
</div>
