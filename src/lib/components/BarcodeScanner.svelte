<script lang="ts">
	import { onMount } from 'svelte';
	import { BrowserMultiFormatReader, BarcodeFormat, DecodeHintType } from '@zxing/library';

	let { isbn = $bindable('') }: { isbn: string } = $props();

	let video: HTMLVideoElement;
	let codeReader: BrowserMultiFormatReader;

	function isIsbn13(ean: string): boolean {
		/**
		 * Checks if a 13-digit EAN string is an ISBN.
		 */
		if (ean.length !== 13 || !/^\d+$/.test(ean)) {
			return false;
		}
		return ean.startsWith('978') || ean.startsWith('979');
	}

	onMount(() => {
		const hints = new Map();
		const formats = [BarcodeFormat.EAN_13];
		hints.set(DecodeHintType.POSSIBLE_FORMATS, formats);
		codeReader = new BrowserMultiFormatReader(hints);

		async function startDecoding() {
			try {
				await codeReader.decodeFromVideoDevice(null, video, (result, err) => {
					if (result) {
						const resultNum = result.getText();
						if (isIsbn13(resultNum)) {
							isbn = resultNum;
						}
					}
					if (err) {
						// zxing-js throws NotFoundException pretty often, so we swallow up the error
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
