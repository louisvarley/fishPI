fishpi.repeat('Dashboard Temperature Hook', 5000, function () {

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




fishpi.screenChanged('temperature', function () {
    fishpi.graphTemperature();
    jQuery('#temperature-graph').height(jQuery(window).height() - 100)
    jQuery('#temperature-graph').width(jQuery(window).width())
})


fishpi.graphTemperature = function () {


    jQuery('#temperature-graph').fadeOut("fast");

    fishpi.api({
        class: 'temperature',
        action: 'getTemperatureLog',
        done: function (data) {

            var hours = []
            var temperatures = []

            jQuery.each(data, function (hour, temperature) {
                hours.push(hour)
                temperatures.push(temperature)
            })

            fishpi.chart = new Highcharts.Chart({

                chart: {
                    renderTo: 'temperature-graph',
                    animation: true,
                    styledMode: true,
                },

                title: { text: "24 Hour Temperatures" },

                xAxis: {
                    categories: hours,
                    tickInterval: 1,
                    min: 0,
                    max: 23,
                },
                yAxis: {
                    min: 0,
                    max: 100,
                    gridLineWidth: 0,
                    title: { text: '' },
                },
                credits: { enabled: false },
                plotOptions: {
                    series: {
                        stickyTracking: false,
                        marker: {
                            enabled: true,
                            symbol: 'circle',
                            radius: 10
                        }
                    },

                    column: {
                        stacking: 'normal'
                    },
                    line: {
                        cursor: 'ns-resize'
                    }
                },

                series: [{
                    data: temperatures,
                    type: 'spline',
                    showInLegend: false,
                    name: "",
                }]

            });

            jQuery('#temperature-graph').fadeIn("fast");

        }
    });

}