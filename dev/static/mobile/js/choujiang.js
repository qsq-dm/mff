jQuery(document).ready(function($) {
	
     $('.box li:nth-child(5)').click(function(event) {
     	  $(this).addClass('current').siblings().removeClass('current')

     });

});