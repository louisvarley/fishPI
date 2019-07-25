/* Initialise FishPI */
var fishpi = {}

fishpi.init = function (name, func) {

    jQuery(document).ready(function () {
        func();
    })
}

fishpi.refreshScreen = function () {

    screen = jQuery('.screen-btn').filter('.active').data('screen');
    jQuery('.screen').hide();

    if (jQuery('#' + screen).hasClass('hide-notifications')) {
        jQuery('#left').hide();
        jQuery('#right').addClass('col-md-12').removeClass('col-md-8');
    } else {
        jQuery('#right').addClass('col-md-8').removeClass('col-md-12');
        jQuery('#left').show();
    }

    jQuery('#' + screen).fadeIn();

}

fishpi.init('Screen Loader Hook',function () {

    fishpi.refreshScreen();

    jQuery('.screen-btn').click(function () {
        jQuery('.screen-btn').removeClass('active');
        jQuery(this).addClass('active');
        fishpi.refreshScreen();
    });

    jQuery('#main').height(jQuery(window).height());
    jQuery('#notice-bar').height(jQuery(window).height() - jQuery('#footer-bar').height());

})

fishpi.toast = function (title, text) {

    var toast = jQuery(`
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
          <div class="toast-header">
            <strong class="mr-auto">` + title + `</strong>
            <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="toast-body">
           ` + text + `
          </div>
        </div>

    `)

    jQuery(toast).hide();
    jQuery('#main').append(toast)
    jQuery(toast).fadeIn();

    window.setTimeout(function () {
        jQuery('.toast').fadeOut(function () {
            jQuery(this).remove();
        });
    },5000)


}