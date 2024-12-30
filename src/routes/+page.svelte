<script lang="ts">
	import DisplayGrid from '$lib/DisplayGrid.svelte';
	import { fade } from 'svelte/transition';

	let numberOfRows = $state(100000);

	let showDropdown = $state(false);
</script>

<svelte:head>
	<title>One Million Line Word Search</title>
	<meta name="description" content="A word search with one million lines." />
</svelte:head>

<div class="m-auto my-4 w-[64rem]">
	<header class="flex flex-row items-end">
		<div class="flex flex-col">
			<h1 class="text-2xl">One Million Line Word Search</h1>
			<span
				>Inspired by the <a
					class="text-blue-500 transition-colors hover:text-blue-700"
					href="https://onemillioncheckboxes.com/"
					target="_blank"
					rel="noopener"
				>
					One Million Checkboxes</a
				> project.</span
			>
		</div>

		<div class="ml-auto mt-auto">
			<div class="flex flex-col items-end">
				<div class="border border-gray-300 pl-4">
					<span>Lines:</span>
					<button class="py-2 pr-4" onclick={() => (showDropdown = !showDropdown)}>
						{numberOfRows}
					</button>
				</div>
				{#if showDropdown}
					<div
						class="absolute z-10 mt-12 border border-gray-300 bg-white"
						transition:fade={{ duration: 100 }}
					>
						{#each [25, 100, 100000] as option}
							<button
								class="flex w-full justify-end px-4 py-2 hover:bg-gray-200"
								onclick={() => {
									numberOfRows = option;
									showDropdown = false;
								}}
							>
								{option}
							</button>
						{/each}
					</div>
				{/if}
			</div>
		</div>
		<div class="ml-4 flex border border-gray-300">
			<a
				class="px-4 py-2 text-blue-500 transition-colors hover:text-blue-700"
				href="https://github.com/tcmmichaelb139/onemillionwordsearch"
				target="_blank"
				rel="noopener">GitHub</a
			>
		</div>
	</header>

	<div class="flex h-fit w-full select-none flex-col text-center">
		<DisplayGrid {numberOfRows} />
	</div>
</div>
