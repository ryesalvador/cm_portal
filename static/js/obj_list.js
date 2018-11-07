function load_list(id, page_num) {
    $(id).load("?ajax&page=" + encodeURIComponent(page_num));
    return false;
}