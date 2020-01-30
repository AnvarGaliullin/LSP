function send_personal_cabinet_form(params) {
	let form_id = params.form_id
	let url = params.url
	let request_type = params.request_type
	let url_on_success = params.url_on_success

	let send_data = $('#'+form_id).serialize()
	console.log('form_id = ' + form_id)
	console.log('send_data.phone = ' + send_data.phone)
	console.log('url = ' + url)
	console.log('request_type = ' + request_type)
	console.log("Сохраняем данные пользователя: ")

	$.ajax({
		url: url,
		data: send_data,
		type: request_type,
		success: function (response) {
			console.log(response);
			response_form_data = response.form_data

		
			response_form_data_json = JSON.stringify(response_form_data)
			console.log('response_form_data_json. = ' + response_form_data_json);
			console.log('response_form_data = ' + response_form_data);
			for (let field in response_form_data) {
				console.log('form.' + field + ' = ' + response_form_data[field])
				// $('#'+field).html(field)
				
			   }

			// response_json = JSON.stringify(response)
			// response_form_data = response_json.name
			// console.log('response_json = ', response_json);
			// console.log('response_form_data = ', response_form_data);
			// console.log('we will redirect you on ' + url_on_success);
			// $(location).attr('href',url_on_success);
			
			if (response.code == 'SUCCESS') {
				console.log('Сервер ответил успешно, идем дальше по flow')
				notify({message:'Данные сохранены!', category:'success', icon:'fa fa-check'})
				console.log('вызвали нотификацию')

			}
			// let redirect_url = '/personal_cabinet/user_id:<user_id>'
			// if (response.code == 'SUCCESS') {
			// 	console.log('we will update form');
			// 	$("#follow").text("Remove");
			// 	$("#follow").attr("onclick", "ajax_unfollow('{{tourist_attraction_name}}')"
			//   }
			
		},
		error: function (response) {
			// console.log('response= ', response);
			// console.log('response.validation_errors = ', response.validation_errors);
			// console.log('response = ', JSON.stringify(response.responseText));
			// let response_data = JSON.parse(response.responseText);
			// console.log('response_data= ', response_data);
			// console.log('response_data.validation_errors.instagram= ', response_data.validation_errors.instagram);
			
			// console.log('error.code= ', response.code);
			// console.log(response);
		}
	});
	return false;
}


