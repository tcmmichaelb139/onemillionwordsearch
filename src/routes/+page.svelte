<script lang="ts">
	import DisplayGrid from '$lib/DisplayGrid.svelte';
</script>

<div class="m-auto my-4 w-[64rem]">
	<header class="flex flex-col">
		<h1 class="text-2xl">One Million Line Word Search</h1>
		<span
			>Inspired by the <a href="https://onemillioncheckboxes.com/" target="_blank" rel="noopener">
				One Million Checkboxes</a
			> project.</span
		>
	</header>

	<div class="flex h-fit w-full select-none flex-col text-center">
		<DisplayGrid />
	</div>
</div>
