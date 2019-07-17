
jQuery( document ).ready(function() {
	
	/* On Load */
	refreshScreen();
	
	/* Screen Change */
    jQuery('.screen-btn').click(function(){
		jQuery('.screen-btn').removeClass('active');
		jQuery(this).addClass('active');
		refreshScreen();
	});
});

var refreshScreen = function(){
	
	screen = jQuery('.screen-btn').filter('.active').data('screen');
	
	jQuery('.screen').hide();
		
		jQuery('#' + screen).fadeIn();

}