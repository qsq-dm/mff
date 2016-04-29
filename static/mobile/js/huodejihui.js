jQuery(document).ready(function($) {
	
    $('.foot2').click(function(event) {
    	  
    	  $('.footer1').hide();
    	  $('.footer2').show();
          $(this).addClass('current').siblings().removeClass('current');
    });
    $('.foot1').click(function(event) {
    	  
    	  $('.footer1').show();
    	  $('.footer2').hide();
          $(this).addClass('current').siblings().removeClass('current');
    });

     $('.bg1').click(function(event) {
             $('.share').hide();
             
     });
   
});