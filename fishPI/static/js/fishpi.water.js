fishpi.repeat('Dashboard Water Solenoid', 4000, function () {

    fishpi.api({
        class: 'water',
        action: 'getSolenoidStatus',
        done: function (data) {

            jQuery('#solenoid-status .card-title').html(data.response)

            if (data.response == "off") {
                jQuery('#solenoid-status').removeClass("active")
            }

            if (data.response == "on") {
                jQuery('#solenoid-status').addClass("active")
            }
        }
    })

})