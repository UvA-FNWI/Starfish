/**
 * Show login dialog
 **/
function show_login(cb_success, cb_cancel){
	// Set default callbacks
	if( typeof cb_success != "function" )
		cb_success = function(){ location.reload(true); };
	if( typeof cb_cancel != "function")
		cb_cancel = function(){};

	// Set onclick event on Login button
	$('#btn_login_ok').click(function(){
		//do login
		login_api("#loginform",
			// On success
			function(data){
				// Hide lightbox
				$('#lightbox').hide()
				// Dispatch to success callback
				cb_success(data)
			},
			// On error
			function(jqXHR, textStatus, errorThrown){
				$('#login_msg').html(
					"Combination of username and password incorrect."
				)
				$('#login_msg').show();
				document.getElementById("password").value='';
			}
		);
	});

	// Set onclick event on Cancel button
	$('#btn_login_cancel').click(function(){
		$('#lightbox').hide();
		// Dispatch to cancel callback
		cb_cancel();
	})
	// Show lightbox
	$('#lightbox').show()
}
