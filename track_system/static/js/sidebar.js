
var pURL = window.location.pathname

if (pURL.substring(1) == "dashboard"){
    $("#dash").addClass("active")
    $("#general").removeClass("active")
    $("#profile").removeClass("active")
}
    
if(pURL.substring(1) == "general"){
    $("#general").addClass("active")
    $("#dash").removeClass("active")
    $("#profile").removeClass("active")

}

if(pURL.substring(1) == "profile"){
    $("#profile").addClass("active")
    $("#dash").removeClass("active")
    $("#general").removeClass("active")

}

