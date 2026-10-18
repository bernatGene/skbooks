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
		const id = Date.now();
		const newBookcase: BookcaseReadWithCounts = {
			id,
			name: 'New Bookcase',
			shelves: [{ id: id + 1, number: 1, bookcase_id: id, book_count: 0 }]
		};
		bookcases.push(newBookcase);
		editingBookcaseId = id;
	}
</script>

<div class="page">
	<header class="header">
		<div class="title-block">
			<h1>škbooks</h1>
			<span class="subtitle">library floor plan</span>
		</div>
	</header>

	<main class="stage">
		<div class="row">
			{#each bookcases as bookcase (bookcase.id)}
				{@const isEditing = editingBookcaseId === bookcase.id}
				<div class="slot" class:editing={isEditing}>
					<Bookcase {bookcase} {isEditing} />
					<div class="toolbar">
						{#if isEditing}
							<button type="button" class="tool" onclick={stopEditing} aria-label="Done">
								<span class="icon-[mdi--check] size-4" aria-hidden="true"></span>
							</button>
						{:else}
							<button
								type="button"
								class="tool"
								onclick={() => startEditing(bookcase.id)}
								aria-label="Edit bookcase"
							>
								<span class="icon-[mdi--pencil] size-4" aria-hidden="true"></span>
							</button>
							<a class="tool" href="/scanner" aria-label="Search books">
								<span class="icon-[mdi--magnify] size-4" aria-hidden="true"></span>
							</a>
						{/if}
					</div>
				</div>
			{/each}

			<button type="button" class="ghost-case" onclick={createNewBookcase}>
				<span class="icon-[mdi--plus] size-7" aria-hidden="true"></span>
				<span class="ghost-label">create new bookcase</span>
			</button>
		</div>

		<div class="floor"></div>
	</main>
</div>

<style>
	.page {
		display: flex;
		flex-direction: column;
		height: 100%;
	}

	.header {
		padding: 1.25rem 2rem;
		border-bottom: 1px solid rgba(93, 64, 55, 0.18);
	}
	.title-block {
		display: flex;
		align-items: baseline;
		gap: 0.75rem;
	}
	.title-block h1 {
		font-size: 1.75rem;
		font-weight: 700;
		letter-spacing: -0.01em;
	}
	.subtitle {
		font-size: 0.8rem;
		color: #a1887f;
		letter-spacing: 0.08em;
	}

	.stage {
		flex-grow: 1;
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
		overflow: hidden;
		padding-bottom: 1.5rem;
		background-image:
			linear-gradient(to right, rgba(93, 64, 55, 0.05) 1px, transparent 1px),
			linear-gradient(to bottom, rgba(93, 64, 55, 0.05) 1px, transparent 1px);
		background-size: 24px 24px;
	}

	.row {
		display: flex;
		align-items: flex-end;
		gap: 2.5rem;
		overflow-x: auto;
		padding: 2rem 2rem 0;
	}

	.slot {
		position: relative;
		flex-shrink: 0;
	}
	.toolbar {
		position: absolute;
		top: -2.25rem;
		right: 0;
		display: flex;
		gap: 0.375rem;
		opacity: 0;
		pointer-events: none;
		transition: opacity 0.15s ease;
	}
	.slot:hover .toolbar,
	.slot.editing .toolbar {
		opacity: 1;
		pointer-events: auto;
	}
	.tool {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 2rem;
		height: 2rem;
		border: 1px solid #5d4037;
		border-radius: 9999px;
		background: #faf3e0;
		color: #5d4037;
		transition:
			background 0.15s,
			color 0.15s;
	}
	.tool:hover {
		background: #5d4037;
		color: #faf3e0;
	}

	.ghost-case {
		flex-shrink: 0;
		width: 16rem;
		min-height: 5rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		padding: 1rem;
		border: 2px dashed #a1887f;
		border-bottom: none;
		border-radius: 4px 4px 0 0;
		background: transparent;
		color: #a1887f;
		cursor: pointer;
		transition:
			border-color 0.15s,
			color 0.15s;
	}
	.ghost-case:hover {
		border-color: #5d4037;
		color: #5d4037;
	}
	.ghost-label {
		font-size: 0.8rem;
		letter-spacing: 0.03em;
	}

	.floor {
		border-top: 2px solid #5d4037;
		position: relative;
		flex-shrink: 0;
	}
	.floor::after {
		content: '';
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		height: 1.5rem;
		background-image: repeating-linear-gradient(
			-45deg,
			transparent,
			transparent 5px,
			#a1887f 5px,
			#a1887f 7px
		);
		opacity: 0.5;
		mask-image: linear-gradient(to bottom, black, transparent);
		-webkit-mask-image: linear-gradient(to bottom, black, transparent);
	}
</style>
