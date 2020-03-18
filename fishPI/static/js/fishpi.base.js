/* Initialise FishPI */
var fishpi = {}

fishpi.online = true;

fishpi.repeaters = {};

fishpi.init = function(name, func) {
    jQuery(document).ready(function () {
        func();
    })
}

fishpi.init("stop refresh", function () {

    $(document).keyup(function (e) {
        if (e.key === "Escape") { // escape key maps to keycode `27`
            alert('escaped');
            clearInterval(reload);
        }
    });

})

fishpi.init("auto refresh", function () {

    var beginInterval = function () {
        return setTimeout(function () {
            if (fishpi.online) {
                location.reload(true);
            }
        }, 30000);
    }

    var reload = beginInterval();

    jQuery(document).on('keypress click', function () {
        clearInterval(reload);
        reload = beginInterval();
    });

})

fishpi.repeat = function(name, interval, func, initial) {

    if (initial) {func()}

    fishpi.repeaters[name] = (setTimeout(function () {

        func();
        fishpi.repeat(name,interval,func,false)

    }, interval));

    return name;

}

fishpi.round = function (n, p) {

    var multiplier = Math.pow(10, p || 0);
    return Math.round(n * multiplier) / multiplier;
}

fishpi.repeatRemove = function (name) {

    if (fishpi.repeaters[name] != null) {
        clearTimeout(fishpi.repeaters[name]);
        fishpi.repeaters[name] = null;
        return true;
    }

    return false;
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

fishpi.screenChanged = function (screen, func) {

    fishpi.init('screenChanged Hook for ' + screen, function () {
        jQuery('.screen-btn').click(function () {
            if (jQuery(this).data("screen") == screen) {
                func()
            }
        })
    })
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

    var toastHTML = '<div class="toast" role="alert" aria-live="assertive" aria-atomic="true"><div class="toast-header"><i class="fas fa-exclamation-circle"></i> <strong class="mr-auto">' + title + '</strong><button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close"><span aria-hidden="true">&times;</span></div><div class="toast-body">' + text + '</div></div>';
    var toast = jQuery(toastHTML)
    jQuery(toast).hide();
    jQuery('#main').append(toast)
    jQuery(toast).fadeIn();

    window.setTimeout(function () {
        jQuery('.toast').fadeOut(function () {
           jQuery(this).remove();
        });
    },5000)


}

fishpi.repeat("Time and Date", 1000, function () {

    monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    var today = new Date();
    var time = ("0" + today.getHours()).slice(-2) + ":" + ("0" + today.getMinutes()).slice(-2)
    var date = monthNames[today.getMonth()] + ' ' + today.getDate();

    jQuery('#time').html(time);
    jQuery('#date').html(date)

}, true)
