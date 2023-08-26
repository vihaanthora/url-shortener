<script>
	import Form from './Form.svelte';
</script>

<svelte:head>
	<title>Shorten URLs</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<Form />
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}
</style>
