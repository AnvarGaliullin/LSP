// Flash Messages notification position and css
$.notifyDefaults({
	offset: {
		x: 20,
		y: 70
	},
	onShow: function () {
		this.css({ 'width': 'auto', 'height': 'auto' });
	}
});
// Flash Messages notification
function notify(parametrs) {
	message = parametrs.message
	category = parametrs.category
	icon = parametrs.icon || ''
	$.notify({
		icon: icon,
		message: message
	}, {
		type: category
	});
}
// Actually import popper.js functionality
$(function () {
	$('[data-toggle="tooltip"]').tooltip()
})