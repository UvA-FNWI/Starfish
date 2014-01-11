function api_call(view_func, formdata)
{
  $.post(view_func, formdata, function(response){
    if(response.success)
    {
      return response;
    } else {
      // if not logged in, show log in modal box
      $.post('/login', formdata, function(loginresponse) {
          if(loginresponse.success) {
            // if user logs in, continue
            api_call(view_func, formdata);
          } else {
            // else abort
            // TODO what if user cancels
            document.getElementById("password").value='';
            alert("Combination of username and password incorrect");
          };
      });
    };
  );
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
