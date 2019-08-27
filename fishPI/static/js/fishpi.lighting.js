
fishpi.chart = null;

fishpi.lightScheduler = function (channel) {

    fishpi.api({
        class: 'lighting',
        action: 'getSchedule',
        get: { channel: channel },
        done: function (data) {

            var times = []
            var schedules = []

            jQuery.each(JSON.parse(data['schedule']), function (time, schedule) {
                times.push(time)
                schedules.push(schedule)
            })

            fishpi.chart = new Highcharts.Chart({

                chart: {
                    renderTo: 'lighting-channel-editor',
                    animation: true,
                    styledMode: true,
                },

                title: { text: "Channel " + data['channel'] + " Schedule" },

                xAxis: {
                    categories: times,
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
                                    fishpi.saveSchedule(fishpi.chart.series[0].data, data['channel']);
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

fishpi.init('Responsive Light Screen', function () {

    var i = jQuery('.lighting-btn').length
    var windowWidth = jQuery(window).width()
    var windowHeight = jQuery(window).height()
    var width = Math.round(windowWidth / i) * 0.98

    jQuery('.lighting-btn').each(function () {
        jQuery(this).width(width);
        jQuery(this).css("max-width", width);
    })


    jQuery('.lighting-dashboard-channel').each(function () {
        jQuery(this).width(windowWidth / 3)
        jQuery(this).css("max-width", windowWidth / 3);
        jQuery(this).height((windowHeight / 3) - 88)
    })

})

fishpi.currentChannel = function () {
    return jQuery('.lighting-btn-channel').filter('.active').data('channel');
}

fishpi.init('Flash Light channel hook', function () {

    jQuery('#btn-lighting-flash').click(function () {
        
        fishpi.api({
            class: 'lighting',
            action: 'flash',
            get: { channel: fishpi.currentChannel },
            done: function (data) {
                fishpi.toast('Flashing', 'Flashing Channel ' + fishpi.currentChannel());
            }
        });

    });
})

fishpi.init('Copy Light Schedule Hook', function () {

    jQuery('#lighting-channels-copy button').click(function () {

        copyTo = jQuery(this).data('channel');
        fishpi.saveSchedule(fishpi.chart.series[0].data, copyTo);
        jQuery('#btn-lighting-actions').hide();
        fishpi.toast('Schedule has been saved...',"Schedule has been cloned and saved to channel " + copyTo)

    })


})

fishpi.init('Lighting action buttons hook', function () {

    jQuery('#btn-lighting-options').mouseover(function () {
        jQuery(this).fadeOut('fast', function () {
            jQuery('#btn-lighting-actions').fadeIn('fast');
        })
    })

    jQuery('#btn-lighting-actions').mouseleave(function () {
        jQuery(this).fadeOut('fast',function () {
            jQuery('#lighting-channels-copy').hide();
            jQuery('#btn-lighting-options').fadeIn('fast');
        });  
    })
})

fishpi.init('Copy Schedule Drop down hook', function () {

    jQuery('#btn-lighting-copy').click(function () {
        jQuery('#lighting-channels-copy').show();
        jQuery('#lighting-channels-copy button').show();
        jQuery('#lighting-channels-copy button [data-channel="' + fishpi.currentChannel() + '"]').hide();
    })

})

fishpi.init('Light Channel Button Hook', function () {

    jQuery('.lighting-btn').click(function () {

        jQuery('.lighting-btn').removeClass('active');
        jQuery(this).addClass('active');

        channel = fishpi.currentChannel();

        if (channel == 'all') {
            jQuery('#lighting-options').hide();
            jQuery('#lighting-channel-editor').fadeOut('fast', function () {
                jQuery('#lighting-channel-dashboard').fadeIn();
            });	

        } else {
            jQuery('#lighting-channel-dashboard').fadeOut('fast', function () {
                jQuery('#lighting-channel-editor').fadeOut('fast', function () {
                    fishpi.lightScheduler(channel)
                    jQuery('#lighting-channel-editor').fadeIn();
                    jQuery('#lighting-options').fadeIn();
                });	
            })
        }

    });


});

fishpi.init('Light Channel Loader Hook', function () {

    jQuery('#lighting-btn-dashboard').click();
})

fishpi.saveSchedule = function (data, channel) {

    var schedule = new Object();
    jQuery.each(data, function (key, d) {
        schedule[d['category']] = Math.round((d['y']), 2)
    })

    jsonSchedule = JSON.stringify(schedule);

    fishpi.api({
        class: 'lighting',
        action: 'setSchedule',
        get: { channel: channel },
        post: { schedule: jsonSchedule },
    });

}

fishpi.repeat('Lighting Dashboard Show Percentages', 60000, function () {

    fishpi.api({
        class: 'lighting',
        action: 'getBrightnessAll',
        done: function (data) {

            jQuery.each(data, function (i, item) {

                jQuery('.lighting-dashboard-channel[data-channel="' + i + '"] .progress-bar').width(item + '%')

                if (item > 10) {
                    jQuery('.lighting-dashboard-channel[data-channel="' + i + '"] .progress-bar').html(item + '%')
                } else {
                    jQuery('.lighting-dashboard-channel[data-channel="' + i + '"] .progress-bar').html('')

                }

                if (item < 1) {
                    jQuery('.lighting-dashboard-channel[data-channel="' + i + '"] .progress-bar').hide()
                } else {
                    jQuery('.lighting-dashboard-channel[data-channel="' + i + '"] .progress-bar').show()
                }

            })

        }

    })
}, true)

fishpi.repeat('Dashboard Lighting Average', 60000, function () {

    fishpi.api({
        class: 'lighting',
        action: 'getBrightnessAverage',
        done: function (data) {

            if (data.response >= 70) {
                jQuery('#lighting-status .card-title').html('Sunny');
                jQuery('#lighting-status .icon').html('<i class="fas fa-sun"></i>')
            }

            if (data.response <= 50) {
                jQuery('#lighting-status .card-title').html('Cloudy');
                jQuery('#lighting-status .icon').html('<i class="fas fa-cloud-sun"></i>')
            }

            if (data.response <= 20) {
                jQuery('#lighting-status .card-title').html('Evening');
                jQuery('#lighting-status .icon').html('<i class="fas fa-cloud-moon"></i>')
            }

            if (data.response <= 10) {
                jQuery('#lighting-status .card-title').html('Night');
                jQuery('#lighting-status .icon').html('<i class="fas fa-moon"></i>')
            }


        }
    })

}, true)