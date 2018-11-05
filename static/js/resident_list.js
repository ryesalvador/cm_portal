function resident_list_page(page_num) {
    $("#resident_list").load("?page=" + encodeURIComponent(page_num));
    return false;
}

$(document).ready(function () {
		$(".page-link").click(resident_list_page);	     
	}
);