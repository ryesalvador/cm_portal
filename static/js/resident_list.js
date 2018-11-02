function sort_by_bldg() {	
	$("#list-all").hide();
	$("#list-by-bldg").show()	
}

$(document).ready(function () {
		$("#list-by-bldg").hide();
		$("#link-bldg").click(sort_by_bldg)
		$(".loadlater").each(function(index, element){
        $(element).attr("src", $(element).attr("data-src"));
    });
	});