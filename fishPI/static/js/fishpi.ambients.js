fishpi.repeat('Dashboard Ambientse Hook', 60000, function () {

    fishpi.api({
        class: 'ambients',
        action: 'getAmbients',
        done: function (data) {
            type = data["type"]

            switch (type) {


                case "cloudy":
                    jQuery('#ambients i').removeClass().addClass("fas fa-cloud")
                    jQuery('#ambients h5').html("Cloudy")
                    break;

                case "stormy":
                    jQuery('#ambients i').removeClass().addClass("fas fa-bolt")
                    jQuery('#ambients h5').html("Storm")
                    break;

                case "rainy":
                    jQuery('#ambients i').removeClass().addClass("fas fa-cloud-rain")
                    jQuery('#ambients h5').html("Raining")
                    break;

                case "nature":
                    jQuery('#ambients i').removeClass().addClass("fas fa-crow")
                    jQuery('#ambients h5').html("Nature")
                    break;

                case "none":
                    jQuery('#ambients i').removeClass().addClass("fas fa-fish")
                    jQuery('#ambients h5').html("Clear")
                    break;


            }


        }
    })

}, true)
