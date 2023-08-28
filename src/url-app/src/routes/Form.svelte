<script lang="ts">
	import { onMount } from 'svelte';
	let originalUrl = '';
	let customUrl = '';
	let shortenedUrl = '';
	let totalUrls = 'Loading...';
	let copied = false;
	let shortenedUrlSection: HTMLDivElement;
	let errorSection: HTMLDivElement;
	const serverUrl = 'https://url-shortener-r1o1.onrender.com';
	let error = '';
	async function copyToClipboard() {
		try {
			await navigator.clipboard.writeText(shortenedUrl);
			copied = true;
		} catch (error) {
			console.error('Error copying to clipboard:', error);
			copied = false;
		}
	}
	async function shortenUrl(e: any) {
		error = '';
		shortenedUrl = '';
		copied = false;
		shortenedUrlSection.classList.add('hidden');
		errorSection.classList.add('hidden');
		if (originalUrl == '') {
			error = 'Original URL cannot be empty!';
			errorSection.classList.remove('hidden');
			return;
		}
		const response = await fetch(`${serverUrl}/api/url/shorten`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ original: originalUrl, custom: customUrl })
		});
		const data = await response.json();
		if (data.shortened === 'error') {
			error = 'Custom string is already mapped to another URL!';
			errorSection.classList.remove('hidden');
		} else if (data.shortened === undefined) {
			error = 'Invalid URL!';
			errorSection.classList.remove('hidden');
		} else {
			shortenedUrl = serverUrl + '/' + data.shortened;
			shortenedUrlSection.classList.remove('hidden');
		}
		fetchTotalUrls();
	}
	async function fetchTotalUrls() {
		const response = await fetch(`${serverUrl}/api/url/total`);
		const data = await response.json();
		totalUrls = data.total;
	}

	onMount(fetchTotalUrls);
</script>

<main class="h-screen flex flex-col items-center justify-center">
	<div class="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
		<h1 class="text-2xl font-semibold mb-4">URL Shortener</h1>
		<form id="urlShortenerForm" class="space-y-4">
			<div>
				<label for="originalUrl" class="block text-sm font-medium text-gray-700">Original URL</label
				>
				<input
					bind:value={originalUrl}
					type="url"
					required
					placeholder="Enter a valid URL"
					autocomplete="off"
					id="originalUrl"
					name="originalUrl"
					class="mt-1 p-2 w-full border rounded-lg"
				/>
				<label for="originalUrl" class="block text-sm font-medium text-gray-700 mt-2"
					>Custom String (if any)</label
				>
				<input
					bind:value={customUrl}
					type="text"
					placeholder="Enter a custom string, eg. 'my-url'"
					autocomplete="off"
					id="customUrl"
					name="customUrl"
					class="mt-1 p-2 w-full border rounded-lg"
				/>
			</div>
			<div>
				<button
					on:click={shortenUrl}
					type="button"
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
			<button
				class="bg-blue-500 text-white px-2 py-1 rounded-lg hover:bg-blue-600 mt-2"
				on:click={copyToClipboard}
			>
				{copied ? 'Copied!' : 'Copy'}
			</button>
		</div>
		<div id="errorSection" bind:this={errorSection} class="mt-4 hidden">
			<p class="font-medium">Error: {error}</p>
		</div>
		<div class="mt-4 text-center">
			<p class="text-gray-500">
				Total URLs converted till date: <span id="totalUrls" class="font-semibold">{totalUrls}</span
				>
			</p>
		</div>
	</div>
</main>
