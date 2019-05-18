$(function(){
  // hide image 
  $("#loader").hide();
  $('#first').hide();
  $('#last').hide();
    

  $('#submit').click(function(){
    if($("#first_name").val() === ""){
      alert("give your fisrt name please !")
      return false;
    }
    if($("#last_name").val() === ""){
      alert("give your last name please !")
      return false;
    }
    if($("#email").val() === ""){
      alert("give your email please !")
      return false;
    }
    if($('#password').val() === ""){
      alert("password vide ")
      return false;
    }
    if($('#password').val() != $("#re_password").val() ){
      alert("don't match !")
      return false;
    }
    return true;
  })




  $('#add_article').click(function(){
    if($('#titre').val() === ""){
      alert('titre empty !')
      return false;
    }
    if($('#slug').val() === ""){
      alert("slug empty !")
      return false;
    }
    if($('#categorie').val() === ""){
      alert("categorie empty !")
      return false;
    }
    if($('#contenu').val() === ""){
      alert("contenu empty")
      return false;
    }
  })

  $('#add_comment').click(function(e){

    e.preventDefault();
    if($('#comment').val() === ''){
      $('#error_comment').show()
    }
    else{
      const url = $('#send-comment').attr('data-url')
      const csrfmiddlewaretoken = $("#send-comment input").val();

      $(document).ajaxStart(function(){
        // Show image container
        $("#loader").show();
        });
        $(document).ajaxComplete(function(){
        // Hide image container
        $("#loader").hide();
        });
        
         $.ajax({
           type: "POST",
           url: url,
           data: {
             'comment': $('#comment').val(),
             'csrfmiddlewaretoken': csrfmiddlewaretoken
           },
           success: function (data) {
             $("#ajax-comment").html(data);
             $('#comment').val("")
           },
           echec : function(){
            alert("error 500 !!!")
           }
         });
    }
  })
})