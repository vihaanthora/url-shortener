<script>
	import Header from './Header.svelte';
	import '../dist/output.css';
</script>

<div class="bg-vintage-bg h-screen">
	<Header />
	<main>
		<slot />
	</main>
</div>

<style>
	.bg-vintage-bg {
		background-color: #f7f3e9;
	}
</style>
