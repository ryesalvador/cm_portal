function load_list(id, query, val) {
    $(id).load("?ajax&" + encodeURIComponent(query) + "=" + encodeURIComponent(val));
    return false;
}