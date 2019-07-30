$(document).ready(function(){
    $('#sign-up').click(function(event){
        $("#reg-form").modal({
            showClose: false,
        })

    })
    $('#sign-ups').click(function(event){
        $("#reg-form").modal({
            showClose: false,
            closeExisting: false, 
        })
    })  
})



