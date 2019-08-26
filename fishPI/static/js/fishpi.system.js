fishpi.repeat('Dashboard System System Temperature Hook', 60000, function () {

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

}, true)

fishpi.repeat("Online Check", 30000, function () {

    fishpi.api({
        class: 'system',
        action: 'online',
        done: function () {

            fishpi.online = true;
            jQuery('#status i').removeClass('fa-times-circle').addClass('fa-check-circle');

        },
        fail: function () {

            fishpi.online = false;
            jQuery('#status i').removeClass('fa-check-circle').addClass('fa-times-circle');
        }
    })
}, true)