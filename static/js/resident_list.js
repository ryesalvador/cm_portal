function sort_by_bldg() {	
	$("#list-all").hide();
	$("#list-by-bldg").show()	
}



$(document).ready(function () {
		$("#list-by-bldg").hide();
		$("#link-bldg").click(sort_by_bldg);
		
		
      
		$(".container").each(function (index, element) {
			var res = {
	       loader: $('<i class="fas fa-spinner fa-pulse"></i>'),
	       image: $(element).find("img") 	
         }	
			$.ajax({				
				url: "#",
				beforeSend: function () {
					//$(element).find("img").hide();		
					//$(element).prepend(res.loader);					
				},
				success: function (data) {
					//$(element).find("img").show();
					//$(element).find(res.loader).remove();
				}
			});
			
		});
	});