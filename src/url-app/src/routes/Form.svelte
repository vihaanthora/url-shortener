<script>
	let originalUrl = '';
	let customUrl = '';
	let shortenedUrl = '';
	const serverUrl = 'http://127.0.0.1:8000';
	async function shortenUrl() {
		const response = await fetch(`${serverUrl}/api?url=${originalUrl}&custom=${customUrl}`);
		const data = await response.json();
		if (data.shortened === 'error') {
			shortenedUrl = 'Error: Custom string already exists in the db, please enter another!';
		} else {
			shortenedUrl = serverUrl + '/' + data.shortened;
		}
	}
</script>

<main>
	<h3>URL Shortener</h3>
	<input bind:value={originalUrl} placeholder="Enter URL to shorten" id="original-url" />
	<input bind:value={customUrl} placeholder="Enter custom string" id="custom-url" />

	<button on:click={shortenUrl}>Shorten</button>
	{#if shortenedUrl}
		<p>Shortened URL: <a href={shortenedUrl} target="_blank">{shortenedUrl}</a></p>
	{/if}
</main>

<style>
	/* Add your styles here */
</style>
