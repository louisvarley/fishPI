fishpi.repeat('Dashboard Co2', 10000, function () {

    fishpi.api({
        class: 'CO2',
        action: 'getCo2Status',
        done: function (data) {

            if (data.response == "off") {
                jQuery('#co2-status').removeClass("active")
            }

            if (data.response == "on") {
                jQuery('#co2-status').addClass("active")
            }
        }
    })

}, true)