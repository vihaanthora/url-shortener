<script>
	import Header from './Header.svelte';
	import '../dist/output.css';
</script>

<div class="app">
	<Header />
	<main>
		<slot />
	</main>
</div>

<style>
</style>
