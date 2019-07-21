
fishpi.apiURL = function(c,a,p=[]){
	p = jQuery.param(p);
	return "/api/<class>/<action>".replace("<class>",c).replace("<action>",a) + '/?' + p;
}

fishpi.api = function(c){
	

	var d = { 
		class: null, 
		action: null, 
		get: null, 
		post: null, 
		dataType: "json",
		done: function(){},
		fail: function(){alert('API Call Failure on ' + c['class'] + '/' + c['action'])}
	};
		
	jQuery.extend(d,c);
	
	jQuery.ajax({
		type: d["post"] == null ? "GET" : "POST",
		url: fishpi.apiURL(d['class'],d['action'],d['get']),
		dataType: d['dataType'],
		traditional: true,
		data: d['post'],
	}).done(function(data){	
		d['done'](data);		
	}).fail(function(data){	
		d['fail'](data);
	})
	
}