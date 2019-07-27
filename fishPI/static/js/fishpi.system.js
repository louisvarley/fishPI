fishpi.repeat('Dashboard System System Temperature Hook', 4000, function () {

    fishpi.api({
        class: 'system',
        action: 'getSystemTemperature',
        done: function (data) {
            temperature = data["temperature"]
            label = data["label"]

            jQuery('#system-temperature').removeClass("error over under normal")
            jQuery('#system-temperature').addClass(label)
            jQuery('#system-temperature .text').html(temperature + '&deg c');

        }
    })

})