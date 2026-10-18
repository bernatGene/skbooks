<script lang="ts">
	import type { BookcaseReadWithCounts, ShelfReadWithBookCount } from '$lib/client/types.gen';

	const {
		bookcase = $bindable(),
		isEditing = false
	}: { bookcase: BookcaseReadWithCounts; isEditing: boolean } = $props();

	const sortedShelves = $derived(
		[...(bookcase.shelves ?? [])].sort((a, b) => b.number - a.number)
	);

	function addShelf() {
		const nextNumber = (bookcase.shelves?.length ?? 0) + 1;
		const newShelf: ShelfReadWithBookCount = {
			id: Date.now(),
			number: nextNumber,
			bookcase_id: bookcase.id,
			book_count: 0
		};
		bookcase.shelves = [...(bookcase.shelves ?? []), newShelf];
	}

	function removeShelf(shelfId: number) {
		bookcase.shelves = (bookcase.shelves ?? []).filter((s) => s.id !== shelfId);
	}
</script>

<div class="bookcase" class:editing={isEditing}>
	<div class="name">
		<input type="text" bind:value={bookcase.name} disabled={!isEditing} />
	</div>

	<div class="shelves">
		{#if isEditing}
			<button type="button" class="ghost-shelf" onclick={addShelf} aria-label="Add shelf">
				<span class="icon-[mdi--plus] size-7" aria-hidden="true"></span>
			</button>
		{/if}

		{#each sortedShelves as shelf (shelf.id)}
			<div class="shelf">
				<span class="shelf-number">#{shelf.number}</span>
				<span class="shelf-count">{shelf.book_count}</span>
				<span class="shelf-label">books</span>
				{#if isEditing}
					<button
						type="button"
						class="remove-shelf"
						onclick={() => removeShelf(shelf.id)}
						aria-label="Remove shelf"
					>
						<span class="icon-[mdi--close] size-4" aria-hidden="true"></span>
					</button>
				{/if}
			</div>
		{/each}
	</div>
</div>

<style>
	.bookcase {
		--line: #5d4037;
		--line-style: solid;
		width: 16rem;
		background: #faf3e0;
		border: 2px var(--line-style) var(--line);
		border-bottom: none;
		border-radius: 4px 4px 0 0;
		user-select: none;
	}
	.bookcase.editing {
		--line: #a1887f;
		--line-style: dashed;
	}

	.name {
		border-bottom: 2px var(--line-style) var(--line);
		padding: 0.5rem 0.75rem;
	}
	.name input {
		width: 100%;
		background: transparent;
		text-align: center;
		font-size: 1.05rem;
		font-weight: 600;
		letter-spacing: 0.02em;
		color: #5d4037;
		outline: none;
	}
	.name input:disabled {
		cursor: default;
	}

	.shelves {
		display: flex;
		flex-direction: column;
	}
	.shelf,
	.ghost-shelf {
		height: 5rem;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		border-top: 2px var(--line-style) var(--line);
		color: #5d4037;
	}
	.ghost-shelf {
		color: #a1887f;
		background: transparent;
		cursor: pointer;
		transition: color 0.15s;
	}
	.ghost-shelf:hover {
		color: #5d4037;
	}

	.shelf-number {
		position: absolute;
		top: 0.25rem;
		left: 0.5rem;
		font-size: 0.625rem;
		font-family: ui-monospace, monospace;
		color: #a1887f;
		letter-spacing: 0.05em;
	}
	.shelf-count {
		font-size: 1.5rem;
		font-weight: 600;
	}
	.shelf-label {
		margin-left: 0.25rem;
		font-size: 0.75rem;
		color: #a1887f;
	}

	.remove-shelf {
		position: absolute;
		top: -0.625rem;
		right: -0.625rem;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 1.25rem;
		height: 1.25rem;
		border: 1px solid #a1887f;
		border-radius: 9999px;
		background: #faf3e0;
		color: #a1887f;
	}
	.remove-shelf:hover {
		border-color: #b91c1c;
		color: #b91c1c;
	}
</style>
