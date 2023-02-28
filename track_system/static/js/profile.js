$(document).ready(function(){

    $("#btn-update").click(function(){
        $("#settingtab").addClass("active")
        $("#profiletab").removeClass("active")

    })

    $("body").on("click", "#btn-save", function() { 

        let username = $("#update_username").val()
        let email = $("#update_email").val()
        let password = $("#update_password").val()

        let dict_data = {
          username : username,
          email : email,
          password : password
        }

        let format_data = JSON.stringify(dict_data) // Convert data into string
        $.post("/profile", {action: "update_data", data: format_data},).done(function(data){
           convert_data = JSON.parse(data)
           if(convert_data.status = "save"){
              location.reload()
           }


        });

    });

    
    $("body").on("submit", "#form-pass-validate", function() { 

        let password = $("#validate-pass").val()
        $.post("/profile",{ action: "get_user_detail", password: password},)
          .done(function(data) {
           
            convert_data = JSON.parse(data) // convert json string to javascript object notation
            if(convert_data.data == "error"){
              $("#validate-pass").val('')

            }else{
              let user = convert_data.data
              $("#form-pass-validate").replaceWith('<div class="card card-primary card-outline">'
                + '<div class="card-body box-profile"><div class="text-center"></div>'
                + '<h3 class="profile-username text-center">Update Detail</h3>'
                + '<ul class="list-group list-group-unbordered mb-3">'
                + '<li class="list-group-item"><b>Username</b> <a class="float-right"><div class="col-sm-12 my-1">'
                + '<input id="update_username" type="text" class="form-control" value=' + user.username + '></div></a></li>'
                + '<li class="list-group-item"><b>Email</b> <a class="float-right"><div class="col-sm-12 my-1">'
                + '<input id="update_email" type="text" class="form-control" value=' + user.email + '></div></a></li>'
                + '<li class="list-group-item"><b>Update Password</b> <a class="float-right"><div class="col-sm-12 my-1">'
                + '<input id="update_password" type="text" class="form-control" placeholder="Optional change password"></div></a></li></ul>'
                + '<button id="btn-save" type="button" class="btn btn-primary col-md-12"><b>Save</b></button></div></div>'

              )
            }

          },"json");

          return false;
    });

  

});