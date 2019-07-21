/* Initialise FishPI */
var fishpi = {}

fishpi.init = function(func){
	
	jQuery( document ).ready(function() {
		func();
	})
	
}

fishpi.refreshScreen = function(){
		
	screen = jQuery('.screen-btn').filter('.active').data('screen');
	jQuery('.screen').hide();	
	jQuery('#' + screen).fadeIn();

}

fishpi.init(function(){
	
	fishpi.refreshScreen();
	
    jQuery('.screen-btn').click(function(){
		jQuery('.screen-btn').removeClass('active');
		jQuery(this).addClass('active');
		fishpi.refreshScreen();
	});
	
	jQuery('#main').height(jQuery(window).height());	
	jQuery('#notice-bar').height(jQuery(window).height() - jQuery('#footer-bar').height());
	
})




