<script lang="ts">
	import type { BookcaseReadWithCounts, ShelfReadWithBookCount } from '$lib/client/types.gen';

	const {
		bookcase = $bindable(),
		isEditing = false
	}: { bookcase: BookcaseReadWithCounts; isEditing: boolean } = $props();

	function addShelf() {
		const newShelf: ShelfReadWithBookCount = {
			id: Date.now(), // Temporary ID
			number: bookcase.shelves ? bookcase.shelves.length + 1 : 1,
			bookcase_id: bookcase.id,
			book_count: 0
		};
		if (!bookcase.shelves) {
			bookcase.shelves = [];
		}
		bookcase.shelves = [newShelf, ...bookcase.shelves];
	}

	function removeShelf(shelfId: number) {
		if (bookcase.shelves) {
			bookcase.shelves = bookcase.shelves.filter((shelf) => shelf.id !== shelfId);
		}
	}
</script>

<div class="flex-shrink-0">
	{#if isEditing}
		<!-- Ghost Shelf for adding -->
		<div
			class="group flex-shrink-0 cursor-pointer"
			onclick={addShelf}
			onkeypress={addShelf}
			role="button"
			tabindex="0"
		>
			<div
				class="flex h-24 w-64 items-center justify-center border-4 border-dashed border-[#a1887f] bg-transparent text-[#a1887f] group-hover:border-[#5d4037] group-hover:text-[#5d4037]"
			>
				<span class="icon-[mdi--plus] size-10"></span>
			</div>
		</div>
	{/if}

	<div
		class="relative w-64 rounded-t-lg border-x-4 border-t-4 p-3"
		class:border-[#5d4037]={!isEditing}
		class:border-dashed={isEditing}
		class:border-[#a1887f]={isEditing}
	>
		<input
			type="text"
			bind:value={bookcase.name}
			class="w-full bg-transparent text-center text-2xl font-bold focus:outline-none"
			disabled={!isEditing}
		/>
	</div>
	<div class="flex flex-col-reverse">
		{#if bookcase.shelves}
			{#each bookcase.shelves as shelf}
				<div
					class="relative flex h-24 w-64 items-center justify-center border-4 bg-transparent"
					class:border-[#5d4037]={!isEditing}
					class:border-dashed={isEditing}
					class:border-[#a1887f]={isEditing}
				>
					{#if isEditing}
						<button
							onclick={() => removeShelf(shelf.id)}
							class="absolute -top-4 -right-4 rounded-full bg-[#faf3e0] p-1 text-[#a1887f] hover:text-red-500"
						>
							<span class="icon-[mdi--close] size-6">Cross</span>
						</button>
					{/if}
					<span class="text-xl font-bold">{shelf.book_count} books</span>
				</div>
			{/each}
		{/if}
	</div>
</div>
