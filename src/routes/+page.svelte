<script lang="ts">
	import DisplayGrid from '$lib/DisplayGrid.svelte';
	import { fade } from 'svelte/transition';

	let numberOfRows = $state(100000);

	let showDropdown = $state(false);
</script>

<div class="m-auto my-4 w-[64rem]">
	<header class="flex flex-row">
		<div class="flex flex-col">
			<h1 class="text-2xl">One Million Line Word Search</h1>
			<span
				>Inspired by the <a href="https://onemillioncheckboxes.com/" target="_blank" rel="noopener">
					One Million Checkboxes</a
				> project.</span
			>
		</div>

		<div class="ml-auto mt-auto">
			<button
				class="border border-gray-300 px-4 py-2"
				onclick={() => (showDropdown = !showDropdown)}
			>
				{numberOfRows}
			</button>
			{#if showDropdown}
				<div
					class="absolute z-10 mt-2 border border-gray-300 bg-white"
					transition:fade={{ duration: 100 }}
				>
					{#each [25, 100, 100000] as option}
						<button
							class="flex w-full justify-start px-4 py-2 hover:bg-gray-200"
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
	</header>

	<div class="flex h-fit w-full select-none flex-col text-center">
		<DisplayGrid {numberOfRows} />
	</div>
</div>
