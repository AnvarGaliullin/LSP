function submit_personal_cabinet_form(response) {
	console.log('<submit_personal_cabinet_form> with response = ',response);
	try {
		// Validation errors
		status_code = response.responseJSON.code;
	} catch (err) {
		// OK
		try {
			status_code = response.code;
		} catch (err2) {
			// ERRORS
		}
	}
	  console.log('status_code= ',status_code)


	// error_code = response.responseJSON['code'] || ''
	// validation_errors = response.responseJSON['validation_errors']
	// // ah = response_validation_errors.home_region
	// console.log('responseJSON = ',response.responseJSON)
	// console.log('response_validation_errors = ',response_validation_errors)
	// console.log('ah = ',ah)
	if (status_code == 'SUCCESS') {
		response_form_data = response.form_data
		notify({ message: 'Данные сохранены!', category: 'success', icon: 'fa fa-check' })
		for (let field in response_form_data) {
			let icon_href = '#' + field + '-href > a' // Search for icon in {{render_field}} and change it href
			let field_errors = '#' + field + '-errors ul' // Search for icon in {{render_field}} and change it href
			// console.log('response_form_data[' + field + '] = '+response_form_data[field])
			$(field_errors).html('');
			if (response_form_data[field] == '') {
				$(icon_href).removeAttr("href");
			} else {
				$(icon_href).attr("href", response_form_data[field]);
			}
		}
	}

	if (status_code == 'ERROR') {
		response_form_errors = response.responseJSON.form_errors
		console.log('response_form_errors = ',response_form_errors)
		notify({ message: 'Возникли ошибки!', category: 'danger', icon: 'fa fa-times' })
		console.log('STOOOP')
		for (let field in response_form_errors) {
			
			let field_errors = '#' + field + '-errors ul' // Search for icon in {{render_field}} and change it href
			console.log('field = ',field, ' with errors = ',response_form_errors[field])

			
			// console.log('response_form_data[' + field + '] = '+response_form_data[field])
			if (response_form_errors[field] == '') {
				// $(icon_href).removeAttr("href");
				console.log('NO ERRORS ON FIELD ', field, '!!!')
			} else {
				console.log('ERRORS ON FIELD ', field, '!!!')
				let icon_href = '#' + field + '-href > a' // Search for icon in {{render_field}} and change it href
				$(icon_href).removeAttr("href");
				// $("#header ul").append('<li><a href="/user/messages"><span class="tab">Message Center</span></a></li>');
				// $('#mt-news ul').html('<li><a class="red" href="#" target="_self">Context x</a></li>');
				// alert($('#mt-news').html());

				$(field_errors).html('<li style="color:red;">' + response_form_errors[field] + '</li>');
				// $(field_errors).attr("href", response_form_data[field]);
			}
		}
	}

};
