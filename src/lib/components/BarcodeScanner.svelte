<script lang="ts">
	import { onMount } from 'svelte';
	import { scanImageData, ZBarSymbolType, setModuleArgs } from '@undecaf/zbar-wasm';
	import zbarWasmUrl from '@undecaf/zbar-wasm/dist/zbar.wasm?url';

	let { isbn = $bindable('') }: { isbn: string } = $props();

	let video: HTMLVideoElement;
	let stream: MediaStream | null = null;
	let rafId = 0;

	let resolution = $state('');
	let lastError = $state('');
	let lastRejected = $state('');
	let detectionCount = $state(0);

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
		setModuleArgs({ locateFile: () => zbarWasmUrl });

		const canvas = document.createElement('canvas');
		const ctx = canvas.getContext('2d', { willReadFrequently: true })!;

		async function startScanning() {
			try {
				const constraints: MediaStreamConstraints = {
					video: {
						facingMode: 'environment',
						width: { ideal: 1280 },
						height: { ideal: 720 }
					}
				};
				stream = await navigator.mediaDevices.getUserMedia(constraints);
				video.srcObject = stream;
				await new Promise<void>((resolve) => {
					video.addEventListener('loadedmetadata', () => resolve(), { once: true });
				});
				await video.play();

				canvas.width = video.videoWidth;
				canvas.height = video.videoHeight;
				resolution = `${video.videoWidth}x${video.videoHeight}`;

				async function scanLoop() {
					try {
						ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
						const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
						const symbols = await scanImageData(imageData);
						for (const sym of symbols) {
							if (
								sym.type === ZBarSymbolType.ZBAR_EAN13 ||
								sym.type === ZBarSymbolType.ZBAR_ISBN13
							) {
								const code = sym.decode();
								if (isIsbn13(code)) {
									isbn = code;
									detectionCount++;
								} else {
									lastRejected = code;
								}
							}
						}
					} catch (err) {
						lastError = `${(err as Error).name}: ${(err as Error).message}`;
					}
					rafId = requestAnimationFrame(scanLoop);
				}

				scanLoop();
			} catch (err) {
				console.error('Error starting video stream:', err);
				lastError = `${(err as Error).name}: ${(err as Error).message}`;
				alert('Could not start video stream. Please allow camera access and refresh the page.');
			}
		}

		startScanning();

		return () => {
			cancelAnimationFrame(rafId);
			stream?.getTracks().forEach((t) => t.stop());
		};
	});
</script>

<div class="relative w-full max-w-2xl rounded-lg bg-black shadow-lg">
	<!-- svelte-ignore a11y_media_has_caption -->
	<video
		bind:this={video}
		autoplay
		playsinline
		muted
		class="aspect-video w-full rounded-md"
		style="transform: scaleX(-1);"
		aria-label="Webcam live feed"
	></video>

	<div
		class="pointer-events-none absolute left-2 top-2 rounded bg-black/60 px-2 py-1 font-mono text-[11px] leading-tight text-green-400"
	>
		<div>res: {resolution || '...'}</div>
		<div>scans: {detectionCount}</div>
		{#if lastRejected}
			<div class="text-yellow-400">rejected: {lastRejected}</div>
		{/if}
		{#if lastError}
			<div class="text-red-400">err: {lastError}</div>
		{/if}
	</div>
</div>
