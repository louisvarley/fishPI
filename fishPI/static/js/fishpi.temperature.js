fishpi.repeat('Dashboard Temperature Hook', 4000, function () {

    fishpi.api({
        class: 'temperature',
        action: 'getTemperature',
        done: function (data) {

            temperature = data["temperature"]
            label = data["label"]

            jQuery('#aquarium-temperature').removeClass("error over under normal")
            jQuery('#aquarium-temperature').addClass(label)
            jQuery('#aquarium-temperature .text').html(temperature + '&deg c');
        }
    })

})