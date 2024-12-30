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
		<!-- drop down menu with 3 options: 25, 100, 100000-->
		<!-- I want to create a custom drop down menu with three options 25, 100, and 100000. Also I don't want to use html select. I want the style to align with what I have currently which are sharp corners and prety minimal style

		The options will update "numberOfRows" whenever it changes. The default value is 100000. Also I want it to show up when I click the dropdown menu. I can have a variable for this just make the code, I will add it after. -->
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
