function load_list(id, query, val) {
	 $.ajax({
	 	url: "?" + encodeURIComponent(query) + "=" + encodeURIComponent(val),
	 	beforeSend: function () {
	 		//$('.progress').hide();
	 	},
	 	success: function (data) {
	 		$(id).html(data);
	 		//$('.progress').show();
	 	},
                progress: function(e) {
        //make sure we can compute the length
        if(e.lengthComputable) {
            //calculate the percentage loaded
            var pct = (e.loaded / e.total) * 100;

            //log percentage loaded
            console.log(pct);
        }
        //this usually happens when Content-Length isn't set
        else {
            console.warn('Content Length not reported!');
        }
    }
	 });	 
}
