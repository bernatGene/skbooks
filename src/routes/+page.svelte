<script lang="ts">
	import type { BookcaseReadWithCounts } from '$lib/client/types.gen';
	import Bookcase from '$lib/components/Bookcase.svelte';

	const bookcases = $state<BookcaseReadWithCounts[]>([
		{
			id: 1,
			name: 'Living Room',
			shelves: [
				{ id: 1, number: 1, bookcase_id: 1, book_count: 12 },
				{ id: 2, number: 2, bookcase_id: 1, book_count: 23 },
				{ id: 3, number: 3, bookcase_id: 1, book_count: 5 }
			]
		},
		{
			id: 2,
			name: 'Office',
			shelves: [
				{ id: 4, number: 1, bookcase_id: 2, book_count: 30 },
				{ id: 5, number: 2, bookcase_id: 2, book_count: 18 }
			]
		}
	]);

	let editingBookcaseId = $state<number | null>(null);

	function startEditing(bookcaseId: number) {
		editingBookcaseId = bookcaseId;
	}

	function stopEditing() {
		editingBookcaseId = null;
	}

	function createNewBookcase() {
		const newBookcase: BookcaseReadWithCounts = {
			id: Date.now(), // Temporary ID
			name: 'New Bookcase',
			shelves: [{ id: Date.now() + 1, number: 1, bookcase_id: Date.now(), book_count: 0 }]
		};
		bookcases.push(newBookcase);
		editingBookcaseId = newBookcase.id;
	}
</script>

<div class="flex h-full flex-col bg-[#faf3e0] font-sans text-[#5d4037]">
	<header class="p-6 text-center">
		<h1 class="text-5xl font-bold">škbooks</h1>
	</header>

	<main class="flex flex-grow flex-col justify-end overflow-hidden">
		<div class="flex items-end gap-12 overflow-x-auto px-16 pb-0">
			<!-- Bookcases -->
			{#each bookcases as bookcase (bookcase.id)}
				<div class="relative">
					<Bookcase {bookcase} isEditing={editingBookcaseId === bookcase.id} />
					{#if editingBookcaseId === bookcase.id}
						<button
							onclick={stopEditing}
							class="absolute -top-4 -right-4 rounded-full bg-green-200 p-2 text-green-800"
						>
							<span class="icon-[mdi--check] size-6">Done</span>
						</button>
					{:else}
						<button
							onclick={() => startEditing(bookcase.id)}
							class="absolute -top-4 -right-4 rounded-full bg-blue-200 p-2 text-blue-800 opacity-0 transition-opacity hover:opacity-100"
						>
							<span class="icon-[mdi--pencil] size-6">Edit</span>
						</button>
					{/if}
				</div>
			{/each}

			<!-- Ghost Bookcase -->
			<div
				class="group flex-shrink-0 cursor-pointer"
				onclick={createNewBookcase}
				onkeypress={createNewBookcase}
				role="button"
				tabindex="0"
			>
				<div
					class="relative w-64 rounded-t-lg border-x-4 border-t-4 border-dashed border-[#a1887f] bg-transparent p-3 text-[#a1887f] group-hover:border-[#5d4037] group-hover:text-[#5d4037]"
				>
					<h2 class="text-center text-2xl font-bold">New Bookcase</h2>
				</div>
				<div
					class="flex h-24 w-64 items-center justify-center border-4 border-dashed border-[#a1887f] bg-transparent text-[#a1887f] group-hover:border-[#5d4037] group-hover:text-[#5d4037]"
				>
					<span class="icon-[mdi--plus] size-10"></span>
				</div>
			</div>
		</div>

		<!-- Floor Container -->
		<div class="w-full flex-shrink-0 px-16 pt-0 pb-8">
			<div class="floor-line relative w-full"></div>
		</div>
	</main>
</div>

<style>
	.floor-line {
		border-top: 4px solid #5d4037;
	}
	.floor-line::after {
		content: '';
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		height: 1rem;
		background-image: repeating-linear-gradient(
			-45deg,
			transparent,
			transparent 6px,
			#a1887f 6px,
			#a1887f 8px
		);
		opacity: 0.6;
		mask-image: linear-gradient(to bottom, black, transparent);
	}
</style>
