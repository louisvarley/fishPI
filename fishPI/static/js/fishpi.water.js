
fishpi.repeat("Show Water Changed", 1000, function () {

    fishpi.api({
        class: 'water',
        action: 'getDayLitres',
        done: function (data) {
            jQuery('#aquarium-water-changed .text').html(fishpi.round(data.litres,1) + "L")
        }
    })

})

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

fishpi.screenChanged('water', function () {
    fishpi.waterScheduler();
    jQuery('#water-schedule-editor').fadeIn();
    jQuery('#water-schedule-editor').height(jQuery(window).height() - 100)
    jQuery('#water-schedule-editor').width(jQuery(window).width())
})

fishpi.waterScheduler = function () {

    fishpi.api({
        class: 'water',
        action: 'getSchedule',
        done: function (data) {

            var times = []
            var schedules = []

            jQuery.each(JSON.parse(data['schedule']), function (time, schedule) {
                times.push(time)
                schedules.push(schedule)
            })

            fishpi.chart = new Highcharts.Chart({

                chart: {
                    renderTo: 'water-schedule-editor',
                    animation: true,
                    styledMode: true,
                },

                title: { text: "Water Change Scheduler " },

                xAxis: {
                    categories: times,
                    tickInterval: 1,
                    min: 0,
                    max: 23,
                },
                yAxis: {
                    min: 0,
                    max: 5,
                    tickInterval: 1,
                    gridLineWidth: 0,
                    title: { text: '' },
                },
                credits: { enabled: false },
                plotOptions: {
                    series: {
                        point: {
                            events: {
                                drag: function (e) {
                                    if (e.newY > 100) {
                                        this.y = 100;
                                        return false;
                                    }
                                    if (e.newY < 0) {
                                        this.y = 0;
                                        return false;
                                    }

                                    $('#drag').html(
                                        'Dragging <b>' + this.series.name + '</b>, <b>' + this.category + '</b> to <b>' + Highcharts.numberFormat(e.y, 2) + '</b>');
                                },
                                drop: function () {
                                    fishpi.saveWaterSchedule(fishpi.chart.series[0].data, data['channel']);
                                }
                            }
                        },
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

                tooltip: {
                    pointFormat: "Intensity: {point.y:.0f} %",
                    animation: true,
                    crosshairs: true,
                    enabled: false,
                    followTouchMove: true,
                },

                series: [{
                    data: schedules,
                    type: 'spline',
                    showInLegend: false,
                    name: "",
                    draggableY: true,
                    dragMinY: 0,
                    dragMaxY: 100,
                }]

            });


        }
    });

}


fishpi.saveWaterSchedule = function (data) {

    var schedule = new Object();
    jQuery.each(data, function (key, d) {
        schedule[d['category']] = Math.round((d['y']), 2)
    })

    jsonSchedule = JSON.stringify(schedule);

    fishpi.api({
        class: 'water',
        action: 'setSchedule',
        post: { schedule: jsonSchedule },
    });

}

