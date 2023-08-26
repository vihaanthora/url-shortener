<script lang="ts">
	let originalUrl = '';
	let customUrl = '';
	let shortenedUrl = '';
	let shortenedUrlSection: HTMLDivElement;
	let errorSection: HTMLDivElement;
	const serverUrl = 'http://127.0.0.1:8000';
	let error = '';
	async function shortenUrl() {
		error = '';
		shortenedUrl = '';
		shortenedUrlSection.classList.add('hidden');
		errorSection.classList.add('hidden');
		const response = await fetch(`${serverUrl}/api?url=${originalUrl}&custom=${customUrl}`);
		const data = await response.json();
		if (data.shortened === 'error') {
			error = 'Custom string is already mapped to another URL!';
			errorSection.classList.remove('hidden');
		} else {
			shortenedUrl = serverUrl + '/' + data.shortened;
			shortenedUrlSection.classList.remove('hidden');
		}
	}
</script>

<main class="w-full flex flex-col h-screen content-center justify-center">
	<div class="w-full max-w-md p-6 bg-white rounded-lg shadow-md self-center">
		<h1 class="text-2xl font-semibold mb-4">URL Shortener</h1>
		<form id="urlShortenerForm" class="space-y-4">
			<div>
				<label for="originalUrl" class="block text-sm font-medium text-gray-700">Original URL</label
				>
				<input
					bind:value={originalUrl}
					type="url"
                    required
					id="originalUrl"
					name="originalUrl"
					class="mt-1 p-2 w-full border rounded-lg"
				/>
				<label for="originalUrl" class="block text-sm font-medium text-gray-700 mt-2">Custom URL</label
				>
				<input
					bind:value={customUrl}
					type="text"
					id="customUrl"
					name="customUrl"
					class="mt-1 p-2 w-full border rounded-lg"
				/>
			</div>
			<div>
				<button
					on:click={shortenUrl}
					type="submit"
					class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
				>
					Shorten URL
				</button>
			</div>
		</form>
		<div id="shortenedUrlSection" bind:this={shortenedUrlSection} class="mt-4 hidden">
			<p class="font-medium">
				Shortened URL:
				<a
					id="shortenedUrl"
					href={shortenedUrl}
					class="break-all text-blue-500 underline"
					target="_blank">{shortenedUrl}</a
				>
			</p>
		</div>
		<div id="errorSection" bind:this={errorSection} class="mt-4 hidden">
			<p class="font-medium">Error: {error}</p>
		</div>
	</div>
</main>

<style>
</style>
