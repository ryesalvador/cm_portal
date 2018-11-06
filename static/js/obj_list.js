function obj_list_page(page_num) {
    $("#obj_list").load("?ajax&page=" + encodeURIComponent(page_num));
    return false;
}