<script lang="ts">
	import { onMount } from 'svelte';
	import { BrowserMultiFormatReader, BarcodeFormat, DecodeHintType } from '@zxing/library';
	import { getBookByIsbnGet } from '$lib/client/sdk.gen';
	import type { BookInfo } from '$lib/client/types.gen';
	import BookCard from '$lib/components/BookCard.svelte';

	let video: HTMLVideoElement;
	const books = $state<BookInfo[]>([]);
	const scannedBarcodes = new Set<string>();
	let codeReader: BrowserMultiFormatReader;

	const UNKNOWN_BOOK: BookInfo = {
		title: 'Unknown Title',
		authors: ['Unknown Author'],
		publisher: 'Unknown Publisher',
		published_date: 'Unknown Date',
		thumbnail: '/no-image-placeholder.svg',
		identifier: ''
	};

	onMount(() => {
		const hints = new Map();
		const formats = [BarcodeFormat.EAN_13];
		hints.set(DecodeHintType.POSSIBLE_FORMATS, formats);
		codeReader = new BrowserMultiFormatReader(hints);

		async function startDecoding() {
			try {
				await codeReader.decodeFromVideoDevice(null, video, async (result, err) => {
					if (result) {
						const barcode = result.getText();
						if (!scannedBarcodes.has(barcode)) {
							scannedBarcodes.add(barcode);
							const { data, error } = await getBookByIsbnGet({ path: { isbn: barcode } });

							if (error || !data) {
								console.error('Error fetching book info:', error);
								books.push({
									...UNKNOWN_BOOK,
									identifier: barcode,
									title: 'Error Fetching Data'
								});
							} else {
								books.push(data);
							}
						}
					}
					if (err) {
						// zxing-js throws NotFoundException pretty often, so we swallow up the error
						// unless we want to debug something.
					}
				});
			} catch (err) {
				console.error('Error starting video stream:', err);
				alert('Could not start video stream. Please allow camera access and refresh the page.');
			}
		}

		startDecoding();

		return () => {
			codeReader?.reset();
		};
	});
</script>

<div class="container mx-auto flex max-w-4xl flex-col items-center gap-8 p-4">
	<h1 class="text-3xl font-bold">Svelte Barcode Scanner</h1>

	<div class="relative w-full max-w-2xl rounded-lg bg-black shadow-lg">
		<!-- svelte-ignore a11y_media_has_caption -->
		<video
			bind:this={video}
			autoplay
			playsinline
			class="aspect-video w-full rounded-md"
			style="transform: scaleX(-1);"
			aria-label="Webcam live feed"
		></video>
	</div>

	{#if books.length > 0}
		<div class="w-full">
			<h2 class="mb-4 text-center text-2xl font-semibold">Scanned Books</h2>
			<div class="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
				{#each books as book}
					<BookCard {book} />
				{/each}
			</div>
		</div>
	{/if}
</div>
