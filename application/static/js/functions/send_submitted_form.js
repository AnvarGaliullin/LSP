function send_submitted_form(params) {
	let form_id = params.form_id
	let url = params.url
	let request_type = params.request_type
	let send_data = $('#'+form_id).serialize()

	$.ajax({
		url: url,
		data: send_data,
		type: request_type,

		success: function (response) {
			response_form_data = response.form_data
			if (response.code == 'SUCCESS') {
				// notify({message:'Данные сохранены!', category:'success', icon:'fa fa-check'})

				for (let field in response_form_data) {
					let icon_href = '#' + field + '-href > a' // Search for icon in {{render_field}} and change it href
					$(icon_href).$(a).attr( "href", response_form_data[field]);
				   }
			}
		
			
		},
		error: function (response) {
		
		}
	});
	return false;
}


