function load_list(id, query, val) {
    $(id).load("?" + encodeURIComponent(query) + "=" + encodeURIComponent(val));
    return false;
}