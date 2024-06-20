document.addEventListener("DOMContentLoaded", () => {
	let form = document.querySelector("#job_post");
	form.addEventListener("submit", function(event) {
		event.preventDefault();//prevent default form submission behavior
		submit_job(form);
	});
});

// send form data
async function submit_job(form) {
	let payload = new FormData(form);
	try {
		let response = await fetch (
				"http://localhost:5001/api/v1/post_job",
				{
						method: "POST",
						body: payload,
				}
			);
			response = await response.json();
			console.log(response);
	} catch (e) {
		console.error(e);
	}
}
