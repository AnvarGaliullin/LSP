function send_flask_form(params) {
	console.log('function <send_flask_form> called with params = ', params)
	let form_id = params.form_id
	let url = params.url
	let request_type = params.request_type
	let function_on_response = params.function_on_response || null
	let send_data = $('#' + form_id).serialize()
	let response_form_data = null

	$.ajax({
		url: url,
		data: send_data,
		type: request_type,
		success: function (response) {
			if (function_on_response != null) {
				function_on_response(response);
			}
		},
		error: function (response) {
			if (function_on_response != null) {
				function_on_response(response);
			}
		}
	});
	return false;
}