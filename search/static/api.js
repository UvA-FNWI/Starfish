/**
 * General API call function
 *  1). Forwards the asynchronous request to the API
 *  2). Checks the response:
 *    a): [Case 200] Call callback for success
 *    b): [Case 401] Issue login procedure and try again
 *    c): [Otherwise] Call callback for error
 *
 * Arguments:
 *  endpoint - The API url to connect to
 *  data - The data to be send, default: null
 *  method - "get" or "post", default: based on data
 *  cb_success - Callback in case of success, default: empty
 *  cb_error - Callback in case an unexpected error occurs, default: empty
 *  cb_cancel - Callback in case login was required but canceled, default: empty
 */
function api_call(endpoint, data, method, cb_success, cb_error, cb_cancel)
{
	// Set default callbacks
	if( typeof cb_success != "function") cb_success = function(){};
	if( typeof cb_error != "function") cb_error = function(){};
	if( typeof cb_cancel != "function") cb_cancel = function(){};
	// Set default data
	if( data == undefined ) data = null
	// Set default method
  if( method == undefined && (data == null)  method = "get"
  else if( method == undefined) method = "post"
  // Setup attempt to execute post call to api
	if(method == "post"){
		jqxhr = $.post(endpoint, data);
  }else{
		jqxhr = $.get(endpoint);
  }
	// Add handler for the success case
	jqxhr.done(function(response, textStatus, jqHXHR){
		  cb_succes(response, jqXHR)
  });
	// Add handler for the fail case
	jqxhr.fail(function(jqXHR, textStatus, errorThrown){
		// error code is 401 (Unauthorized)
		if(jqXHR.statusCode() == 401){
		  // Show login dialog
			show_login(
				function(){
				  // Login success: try api call again
				  api_call(endpoint, data);
				},
				function(){
					// Login cancel
					cb_cancel();
					// Assist garbage collect
					data = null
				}
		  );
		}else{
			// Unexpected error, not related to login
		  cb_error(jqXHR, textStatus, errorThrown)
		  // Assist garbage collect
		  data = null
		}
	});
}

function comment_api(inputdata)
{
  return api_call('/comment', inputdata);
}

function vote_api(inputdata)
{
  return api_call('/vote', inputdata);
}

function askquestion_api(inputdata)
{
  return api_call('/askquestion', inputdata);
}
