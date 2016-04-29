jQuery(document).ready(function($) {
	function show_one () {
		$('.tcc').addClass('hidden');
    	$('.tcc1').removeClass('hidden')
    	$('.bg').removeClass('hidden');
	}
	function show_two() {
		$('.tcc').addClass('hidden');
		$('.tcc2').removeClass('hidden');
		$('.bg').removeClass('hidden');
	}
	function show_three() {
		$('.tcc').addClass('hidden');
    	$('.tcc3').removeClass('hidden');
    	$('.bg').removeClass('hidden');
	}
	function hide_all (argument) {
		 $('.tcc').addClass('hidden');
		 $('.bg').addClass('hidden');
	}
	window.show_one = show_one;
	window.show_two = show_two;
	window.show_three = show_three;
	
});