

fishpi.lightScheduler = function(channel){
	
	fishpi.api({
		class: 'lighting',
		action: 'getSchedule',
		get: {channel: channel},	
		done: function(data) {	
		
	
			var times = []
			var schedules = []
			
			jQuery.each(JSON.parse(data['schedule']), function(time, schedule) {
				times.push(time)
				schedules.push(schedule)
			})
			
			var chart = new Highcharts.Chart({

				chart: {
					renderTo: 'lighting-channel-editor',
					animation: true,
					styledMode: true,
				},
				
				title: {text: "Channel " + data['channel'] + " Schedule"},

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
					title:{text: 'Intensity (%)'},						
				},
				credits: {enabled: false},
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
									fishpi.saveSchedule(chart.series[0].data,data['channel']);
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
			
				
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			alert(errorThrown);
		}
	});			

}


fishpi.init(function(){
	fishpi.lightScheduler(1)
});


fishpi.init(function(){
	
	jQuery('.lighting-btn').click(function(){

			jQuery('.lighting-btn').removeClass('active');
			jQuery(this).addClass('active');
		
			channel = jQuery('.lighting-btn').filter('.active').data('channel');
			jQuery('#lighting-channel-editor').fadeOut('fast',function(){
				fishpi.lightScheduler(channel)
				jQuery('#lighting-channel-editor').fadeIn();
			});	
		
	});
	
	
});



fishpi.saveSchedule = function(data,channel){

		var schedule = new Object();
		jQuery.each(data, function(key,d) {
			schedule[d['category']] = Math.round((d['y']),2)
		})
			
		jsonSchedule = JSON.stringify(schedule);
		
		fishpi.api({
			class: 'lighting',
			action: 'setSchedule',
			get: {channel: channel},
			post: {schedule: jsonSchedule},
		});
		
		
}

