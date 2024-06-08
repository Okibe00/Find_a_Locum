//filter result by profession
let success = function(data) {
	$(".jb_sum_wrapper").html("")
	for (let i = 0; i < data.length; i++) {
		let item = data[i]
		let d_id = item["id"] + `${i}`
		let $val = $("<div>", {"class": "card sum_card", id: d_id})
		$(".jb_sum_wrapper").append($val)

		$(`div#${d_id}`).append(
			`<h3 class="title">${item["title"]}</h3>`,
			`<p class="Status">Status: ${item["Status"]}</p>`,
			`<p class="Start_date">Start Date: ${item["Start_date"]}</p>`,
			`<p class="End_date">End Date: ${item["End_date"]}</p>`,
			`<p class="Number_hours_per_shift">Number of hours per shift: ${item["Number_of_hours_Per_shift"]}</p>`,
			`<p class="hourly_rate">Hourly rate: ${item["hourly_rate"]}</p>`
		)
			$(`div#${d_id}`).click(function() {
				console.log($(this).attr("id"))
				let val = null
				let job_id = $(this).attr("id")
				for (let i = 0; i < data.length; i++) {
					let item = data[i]
					if (item['id'] + `${i}` == job_id) {
						console.log("found")
						console.log(item)
						val = `<h3 class="title">${item["title"]}</h3>
						<p class="description">${item["description"]}</p>
						<p class="hourly_rate">Hourly rate: ${item["hourly_rate"]}</p>
						<p class="state">State: ${item["State"]}</p>
						<p class="Contact">Contact: ${item["Contact"]}</p>
						<p class="Name_of_premise">Name of Premise: ${item["Name_of_premise"]}</p>
						<p class="Address">Address: ${item["Address"]}</p>
						<p class="Shift">Shift: ${item["Shift"]}</p>
						<p class="Status">Status: ${item["Status"]}</p>
						<p class="Start_date">Start date: ${item["Start_date"]}</p>
						<p class="End_date">End date: ${item["End_date"]}</p>
						<p class="Number_of_hours_Per_shift">Number of hours per shift: ${item["Number_of_hours_Per_shift"]}</p>`
						$(".full_descrp").html(val)
					}
				}
			})
	}
}

$(document).ready(function() {
  let name_arr = []
	let id_arr = []
	let all_jobs = []
  $("input:checkbox").change(function() {
    if ($(this).is(":checked")) {
      name_arr.push($(this).parent().attr("prof_name"))
      id_arr.push($(this).parent().attr("prof_id"))
    } else {
      let prof = $(this).parent().attr("prof_name")
      let prof_id = $(this).parent().attr("prof_id")
      name_arr = name_arr.filter((x) => x != prof)
      id_arr = id_arr.filter((x) => x != prof_id)
    }
    $(".field h4").text(name_arr.join() || "Pharmacist, Nurses, Doctors")

		json_obj = JSON.stringify({'prof_id': id_arr})
		$(".btn").click(function() {
			$.ajax(
					{
						url: "http://127.0.0.1:5001/api/v1/job_search/",
						type: 'POST',
						contentType: 'application/json',
						data: json_obj,
						success: function(data) {
									success(data)
						},
						error: function(xhr, status, error) {
								console.log(error, xhr.responseText, status)
						}
					}
			)
		})
  })

	//populate the ui
	$.ajax(
		{
			url: "http://127.0.0.1:5001/api/v1/jobs/",
			type: 'GET',
			datatype: 'json',
			success: function(data) {
				success(data)
			},
			error: function(xhr, status, error) {
					console.log(error, xhr.responseText, status)
			}
		}
)
})
