
fishpi.repeat("Ticks Counter", 1000, function () {

    fishpi.api({
        class: 'water',
        action: 'getWaterTotalTicks',
        done: function (data) {
            jQuery('#aquarium-water-ticks .text').html(data.ticks)
        }
    })

}, true)

fishpi.repeat("Show Water Changed", 30000, function () {

    fishpi.api({
        class: 'water',
        action: 'getWaterTotalDayLitres',
        done: function (data) {
            jQuery('#aquarium-water-changed .text .a').html(fishpi.round(data.litres,1) + "L")
        }
    })

    fishpi.api({
        class: 'water',
        action: 'getWaterLitresPerDay',
        done: function (data) {
            jQuery('#aquarium-water-changed .text .o').html(fishpi.round(data.litres, 1) + "L")
        }
    })

}, true)

fishpi.repeat('Dashboard Water Solenoid', 10000, function () {

    fishpi.api({
        class: 'water',
        action: 'getSolenoidStatus',
        done: function (data) {

            if (data.response == "off") {
                jQuery('#solenoid-status').removeClass("active")
                jQuery('#solenoid-status i').removeClass("fa-spin")
            }

            if (data.response == "on") {
                jQuery('#solenoid-status').addClass("active")
                jQuery('#solenoid-status i').addClass("fa-spin")
            }
        }
    })

}, true)

fishpi.screenChanged('water', function () {
    fishpi.waterScheduler();
    jQuery('#water-schedule-editor').fadeIn();
    jQuery('#water-schedule-editor').height(jQuery(window).height() - 100)
    jQuery('#water-schedule-editor').width(jQuery(window).width())
})

fishpi.waterScheduler = function () {

    fishpi.api({
        class: 'water',
        action: 'getWaterSchedule',
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
                        stickyTracking: true,
                        cursor: 'move',
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
                    pointFormat: "{point.y:.0f} Litres",
                    animation: true,
                    crosshairs: true,
                    enabled: true,
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
        action: 'setWaterScheduleLitres',
        post: { schedule: jsonSchedule },
    });

}

fishpi.repeat('Dashboard Notifications Water Changes', 10000, function () {

    

})

