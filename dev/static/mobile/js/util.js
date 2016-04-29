jQuery(document).ready(function($) {
	
   $.ajax({
   	url: '/path/to/file',
   	type: 'GET',
   	dataType: 'JSON',
   	data: {param1: 'value1'},
   })
   success: function() {
   	console.log("success");
   }
   error:function() {
   	console.log("error");
   }
   .always(function() {
   	console.log("complete");
   });
   


});