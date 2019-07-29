
fishpi.api = function (c) {

    var d = {
        class: null,
        action: null,
        get: null,
        post: null,
        dataType: "json",
        done: function () { },
        fail: function () { fishpi.toast("API Error", c['class'] + '/' + c['action']) }
    };

    jQuery.extend(d, c);

    jQuery.ajax({
        type: d["post"] == null ? "GET" : "POST",
        url: "/api/" + d['class'] + "/" + d['action'] + "/?" + jQuery.param(d['get']),
        dataType: d['dataType'],
        traditional: true,
        data: d['post'],
    }).done(function (data) {
        d['done'](data);
    }).fail(function (data) {
        d['fail'](data);
    })


}

