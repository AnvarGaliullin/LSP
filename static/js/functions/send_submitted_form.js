function send_flask_form(params) {
	console.log('i was called send form')
	console.log('inside_params = ',params)
	let form_id = params.form_id
	let url = params.url
	let request_type = params.request_type
	let send_data = $('#'+form_id).serialize()
	console.log('!!!i was called send form')
	$.ajax({
		url: url,
		data: send_data,
		type: request_type,

		success: function (response) {
			response_form_data = response.form_data
			console.log('response_form_data = ',response_form_data)
			if (response.code == 'SUCCESS') {
				notify({message:'Данные сохранены!', category:'success', icon:'fa fa-check'})

				for (let field in response_form_data) {
					let icon_href = '#' + field + '-href > a' // Search for icon in {{render_field}} and change it href
					console.log('response_form_data[' + field + '] = '+response_form_data[field])
					if (response_form_data[field] == '') {
						console.log('is null should remove attr!!');
						$(icon_href).removeAttr("href");
					} else {
						console.log('NOT null should add attr!!');
						$(icon_href).attr("href", response_form_data[field]);
					}

				   }
			}
		
			
		},
		error: function (response) {
		
		}
	});
	console.log('!!akdkafsmfs!i was called send form')
	return false;
}

console.log('i ended')