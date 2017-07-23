  

//-- No use time. It is a javaScript effect.
function insertChat(who, text,time){
	
    var control = "";
   
    if (who == "user"){
        
      	control= '<div class="chatbox__body__message chatbox__body__message--left">'+
            '<img src="img/user-image.png" alt="Picture">'+
            '<p>'+text+'</p>'+
        '</div>';
    }else{
       	control='<div class="chatbox__body__message chatbox__body__message--right">'+
            '<img src="img/dhl round.jpg" alt="Picture">'+
            '<p>'+text+'</p>'+
        '</div>';
    }
    setTimeout(
        function(){                        
            $(".chatbox__body").append(control);
			$(".chatbox__body").scrollTop($(".chatbox__body")[0].scrollHeight);
        }, time);
    
}

function resetChat(){
    $(".chatbox__body").empty();
}

$(".chatbox__message").on("keyup", function(e){
    if (e.which == 13){
        var text = $(this).val().trim();
        if (text !== ""){
        	insertChat("user", text,0);              
            $(this).val('');
			
			console.log("-"+text+"-");
        	$.ajax({
				xhrFields: { withCredentials: true },
				method: "POST",
				url: "http://127.0.0.1:2015/",
				data: {user: text}
				
				})
        	  .done(function( data ) {
				  console.log(data);
        	    insertChat("dhl",JSON.parse(data).HelpDesk,0);
        	  });
            
        }
    }
});

//-- Clear Chat
resetChat();

//-- Print Messages

insertChat("dhl", "Welcome to DHL. How can I help you today", 0);
//-- NOTE: No use time on insertChat.

(function($) {
    $(document).ready(function() {
        var $chatbox = $('.chatbox'),
            $chatboxTitle = $('.chatbox__title'),
            $chatboxTitleClose = $('.chatbox__title__close'),
            $chatboxCredentials = $('.chatbox__credentials');
        $chatboxTitle.on('click', function() {
            $chatbox.toggleClass('chatbox--tray');
        });
        $chatboxTitleClose.on('click', function(e) {
            e.stopPropagation();
            $chatbox.addClass('chatbox--closed');
        });
        $chatbox.on('transitionend', function() {
            if ($chatbox.hasClass('chatbox--closed')) $chatbox.remove();
        });
    });
})(jQuery);


