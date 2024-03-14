async function query(data) {
	const response = await fetch(
		"https://api-inference.huggingface.co/models/google/gemma-7b",
		{
			headers: { Authorization: "Bearer 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" },
			method: "POST",
			body: JSON.stringify(data),
		}
	);
	const result = await response.json();
	return result;
}

console.log(query("Helllo!"));