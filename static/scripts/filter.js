//filter result by profession
let full_description = function(data) {
	let val = null
	let job_id = $(this).attr("id")
	for (let i = 0; i < data.length; i++) {
		let item = data[i]
		if (item['id'] + `${i}` == job_id) {
			$(".full_descrp").empty().append(
				$('<h3>',
					 {
						"class": "title",
						text: `${item["title"]}`
					}
				),
				$(
					"<p>",
					{"class": "description",
						text: `${item["description"]}`
					}
				),
				$(
					"<p>",
					{
						"class": "hourly_rate",
						text: `Hourly rate: ${item["hourly_rate"]}`
					}
				),
				$("<p>",
					{
						"class": "State",
						text: `State: ${item["State"]}`
					}
				),
				$("<p>",
					{
						"class": "Contact",
						text: `Contact: ${item["Contact"]}`
					}
				),
				$(
					"<p>",
					{
						"class": "Name_of_premise",
						text: `Name of premise: ${item["Name_of_premise"]}`
					}
				),
				$(
					"<p>",
					{
						"class": "Address",
						text: `Address: ${item["Address"]}`
					}
				),
				$(
					"<p>",
					{
						"class": "Shift",
						text: `Shift: ${item["Shift"]}`
					}
				),
				$(
					"<p>",
					{
						"class": "Status",
						text: `Status: ${item["Status"]}`
					}
				),
				$(
					"<p>",
					{
						"class": "Start_date",
						text: `Start date: ${item["Start_date"]}`
					}
				),
				$(
					"<p>",{
						"class": "End_date",
						text: `End date: ${item["End_date"]}`
					}
				),
				$(
					"<p>",
					{
						"class": "Number_of_hours_Per_shift",
						text: `Number of hours per shift: ${item["Number_of_hours_Per_shift"]}`
					}
				),
			)
		}
	}
}
let success = function(data) {
	$(".jb_sum_wrapper").html("")
	let first_card = data[0]["id"] + "0"
	console.log(first_card)
	for (let i = 0; i < data.length; i++) {
		let item = data[i]
		let d_id = item["id"] + `${i}`
		let $val = $(
				"<div>",
				{
					"class": "card sum_card",
					id: d_id,
					click: function (event) {
					full_description.call(this, data)
					}
				}
			)

		$(".jb_sum_wrapper").append($val)

		$(`div#${d_id}`).append(
			$(
				"<h3>",
				{
					"class": "title",
					text: `${item["title"]}`,
					}
				),
			$(
				"<p>",
				 {
					"class": "Status",
					text: `Status: ${item["Status"]}`,
				}
			),
			$(
				"<p>",
				{
					"class": "Start_date",
					text: `Start Date: ${item["Start_date"]}`
				}
			),
			$(
				"<p>",
				{
					"class": "End_date_date",
					text: `End Date: ${item["End_date"]}`
				}
			),
			$(
				"<p>",
				{
					"class": "Number_hours_per_shift",
					text: `Number of hours per shift: ${item["Number_of_hours_Per_shift"]}`
				}
			),
			$(
				"<p>",
				{
					"class": "hourly_rate",
					text: `Hourly rate: ${item["hourly_rate"]}`
				}
			)
		)
	}
	$(`#${first_card}`).trigger('click')
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
				console.log(data);
				success(data)
			},
			error: function(xhr, status, error) {
					console.log(error, xhr.responseText, status)
			}
		}
)
})
