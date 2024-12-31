<script lang="ts">
	import { fade } from 'svelte/transition';

	import VirtualList from 'svelte-tiny-virtual-list';

	import { wordsFoundWritable, getWordsFound, updateToFull, foundWordUpdate } from '$lib/wordStore';

	import { optimalWordSequence, getAllWordsSequence } from '$lib/utils';
	import { onMount } from 'svelte';

	let innerHeight = $state(0);

	const { numberOfRows = $bindable() } = $props();
	let grid: string[][] = $state([]);
	let wordEnds: { [key: string]: any[] } = $state({});
	let words: string[] = $state([]);

	let wordsFound: boolean[] | undefined = $state();
	let foundWords: { [key: string]: number } = $state({});
	let numFound: number = $state(0);

	function getJson() {
		fetch('/wordgrid-' + numberOfRows + '.json')
			.then((response) => response.json())
			.then((json) => {
				grid = json.grid;
				wordEnds = json.wordsEnds;
				words = json.words;

				getWordsFound(numberOfRows);
			});
	}

	onMount(() => {
		getJson();

		wordsFoundWritable.subscribe((value) => {
			wordsFound = value as boolean[];
			if (wordsFound && words.length > 0) {
				updateToFull(wordsFound.length, words.length, numberOfRows);

				foundWords = getAllWordsSequence(
					wordsFound.reduce((acc: string[], val: boolean, idx: number) => {
						if (val) {
							acc = [...acc, words[idx]];
						}
						return acc;
					}, [])
				);

				numFound = wordsFound.reduce((acc, val) => (val ? acc + 1 : acc), 0);
			}
		});
	});

	$effect(() => {
		getJson();
	});

	let scrollToIndex: number | undefined = $state();

	let wordSequence: { [key: string]: boolean } = $state({});
	let begEndString: number[][] = $state([]);

	let start: number[] = $state([]);
	let mouseDown: boolean = $state(false);

	function onMouseDown(i: number, j: number) {
		start = [i, j];
		mouseDown = true;
	}

	function onMouseDrag(i: number, j: number) {
		if (!mouseDown) return;

		const cur = [i, j];

		wordSequence = optimalWordSequence(start, cur);
		begEndString = [start, cur];
	}

	function onMouseUp() {
		mouseDown = false;
		wordSequence = {};

		for (let i = 0; i < 2; i++) {
			begEndString = begEndString.reverse();
			const stringified = JSON.stringify(begEndString);
			const word = wordEnds[stringified];

			if (word) {
				const idx = wordEnds[stringified][1];
				if (wordsFound && !wordsFound[idx]) foundWordUpdate(idx, numberOfRows);
				break;
			}
		}
	}
</script>

<svelte:window bind:innerHeight />

<div class="my-4 flex h-12 w-full flex-row justify-center border border-gray-300 p-1">
	<div class="mx-4 flex h-full items-center justify-center">
		<div class="h-6 w-6">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
				><path
					d="M18.031 16.6168L22.3137 20.8995L20.8995 22.3137L16.6168 18.031C15.0769 19.263 13.124 20 11 20C6.032 20 2 15.968 2 11C2 6.032 6.032 2 11 2C15.968 2 20 6.032 20 11C20 13.124 19.263 15.0769 18.031 16.6168ZM16.0247 15.8748C17.2475 14.6146 18 12.8956 18 11C18 7.1325 14.8675 4 11 4C7.1325 4 4 7.1325 4 11C4 14.8675 7.1325 18 11 18C12.8956 18 14.6146 17.2475 15.8748 16.0247L16.0247 15.8748Z"
				></path></svg
			>
		</div>
	</div>
	<input
		class="mx-3 w-full appearance-none border-none text-lg outline-none"
		type="number"
		placeholder="Scroll to row..."
		bind:value={scrollToIndex}
	/>
</div>

<div class="flex h-full w-full flex-row">
	<div class=" h-full w-full border border-gray-300">
		{#if grid.length == 0}
			<div class="absolute m-4 animate-bounce text-lg">Loading...</div>
		{/if}
		<VirtualList
			width="100%"
			height={Math.floor((innerHeight - 175) / 28) * 28}
			itemCount={grid.length}
			itemSize={28}
			{scrollToIndex}
			scrollToAlignment="center"
		>
			<div slot="item" let:index let:style {style}>
				<div class="flex h-7 w-fit justify-center text-center" transition:fade>
					<div class="flex h-full w-16 items-center justify-center text-xl text-gray-500">
						{index}
					</div>
					{#each grid[index] as cell, j}
						<button
							class="flex h-full w-7 items-center justify-center text-xl transition-colors
								{wordSequence[index + '|' + j]
								? 'bg-sky-300'
								: foundWords[index + '|' + j] == 1
									? 'bg-blue-100'
									: foundWords[index + '|' + j] == 2
										? 'bg-blue-200'
										: foundWords[index + '|' + j] == 3
											? 'bg-blue-300'
											: foundWords[index + '|' + j] == 4
												? 'bg-blue-400'
												: foundWords[index + '|' + j] == 5
													? 'bg-blue-500'
													: foundWords[index + '|' + j] == 6
														? 'bg-blue-600'
														: foundWords[index + '|' + j] == 7
															? 'bg-blue-700'
															: foundWords[index + '|' + j] == 8
																? 'bg-blue-800'
																: ''}"
							onmousedown={() => onMouseDown(index, j)}
							onmousemove={() => onMouseDrag(index, j)}
							onmouseup={onMouseUp}
						>
							{cell}
						</button>
					{/each}
				</div>
			</div>
		</VirtualList>
	</div>

	<div class="ml-4 flex w-72 flex-col overflow-auto border border-gray-300">
		<div class="flex h-8 items-center justify-center border-b border-gray-300 text-lg">
			Found: {numFound}/{words.length}
		</div>
		{#if wordsFound}
			<VirtualList
				width="100%"
				height={Math.floor((innerHeight - 175) / 28) * 28 - 32}
				itemCount={words.length}
				itemSize={28}
			>
				<div slot="item" let:index let:style {style}>
					<div class="flex h-8 w-full items-center justify-center px-1" transition:fade>
						<div class="flex h-full w-44 items-center justify-center text-base">
							{wordEnds[words[index]][0]}
						</div>
						<div class="flex h-full w-16 items-center justify-center text-base">
							<div class="h-6 w-6">
								{#if wordsFound[index]}
									<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="fill-green-500"
										><path
											d="M9.9997 15.1709L19.1921 5.97852L20.6063 7.39273L9.9997 17.9993L3.63574 11.6354L5.04996 10.2212L9.9997 15.1709Z"
										></path></svg
									>
								{:else}
									<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="fill-red-500"
										><path
											d="M11.9997 10.5865L16.9495 5.63672L18.3637 7.05093L13.4139 12.0007L18.3637 16.9504L16.9495 18.3646L11.9997 13.4149L7.04996 18.3646L5.63574 16.9504L10.5855 12.0007L5.63574 7.05093L7.04996 5.63672L11.9997 10.5865Z"
										></path></svg
									>
								{/if}
							</div>
						</div>
					</div>
				</div>
			</VirtualList>
		{/if}
	</div>
</div>
