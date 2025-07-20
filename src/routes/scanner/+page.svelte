<script lang="ts">
	import { getBookByIsbnGet } from '$lib/client/sdk.gen';
	import type { BookInfo } from '$lib/client/types.gen';
	import BarcodeScanner from '$lib/components/BarcodeScanner.svelte';
	import ScannedBookGallery from '$lib/components/ScannedBookGallery.svelte';

	const books = $state<{ isbn: string; bookPromise: Promise<BookInfo> }[]>([]);
	const scannedBarcodes = new Set<string>();
	let scannedIsbn = $state('');

	const fetchBookInfo = async (isbn: string): Promise<BookInfo> => {
		const { data, error } = await getBookByIsbnGet({ path: { isbn: isbn } });
		if (data) return data;
		throw error;
	};

	$effect(() => {
		function handleNewIsbn() {
			if (scannedIsbn && !scannedBarcodes.has(scannedIsbn)) {
				scannedBarcodes.add(scannedIsbn);
				const bookPromise = fetchBookInfo(scannedIsbn);
				books.push({ isbn: scannedIsbn, bookPromise });
			}
		}
		handleNewIsbn();
	});
</script>

<div class="container mx-auto flex max-w-4xl flex-col items-center gap-8 p-4">
	<h1 class="text-3xl font-bold">Svelte Barcode Scanner</h1>

	<BarcodeScanner bind:isbn={scannedIsbn} />

	<ScannedBookGallery {books} />
</div>
