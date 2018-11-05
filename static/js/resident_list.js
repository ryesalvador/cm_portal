function resident_list_page(page_num) {
    $("#resident_list").load("?ajax&page=" + encodeURIComponent(page_num));
    return false;
}