<script>
	import Header from './Header.svelte';
	import '../dist/output.css';
</script>

<div class="flex bg-vintage-bg">
	<Header />
	<main class="flex-grow">
		<slot />
	</main>
</div>

<style>
	.bg-vintage-bg {
		background-color: #f7f3e9;
	}
</style>
