function load_list(id, query, val) {
	 $.ajax({
	 	url: "?" + encodeURIComponent(query) + "=" + encodeURIComponent(val),
	 	beforeSend: function () {
	 		//$(id).hide();
			$(id).prepend('<div class="fa-3x"><i class="fas fa-spinner fa-pulse"></i></div>')
	 	},
	 	success: function (data) {
	 		$(id).html(data);
	 	},
	 });	 
}
