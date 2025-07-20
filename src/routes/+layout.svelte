<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

<div class="flex min-h-screen flex-col bg-[#faf3e0] font-sans text-[#5d4037]">
	<main class="flex-grow">
		{@render children()}
	</main>

	<footer class="w-full flex-shrink-0 bg-[#faf3e0] p-4 text-center">
		<div class="mb-2 flex justify-center gap-6">
			<a href="/about" class="hover:underline">About</a>
			<a href="https://github.com/bernatGene/skbooks" class="hover:underline">Src</a>
			<a href="/guide" class="hover:underline">Guide</a>
		</div>
		<p class="text-sm text-[#a1887f]">© 2025 Bernat Gené Skrabec. All Rights Reserved.</p>
	</footer>
</div>
