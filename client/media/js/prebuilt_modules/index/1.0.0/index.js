YUI.add('templates/index', function (Y) {
    "use strict";
    Y.TemplateStore.store("index_content", Handlebars.compile('<div id="index">Index.<ul>Hi, {{username}}</ul></div>'));
}, '0.0.1', {requires:['template-store']});

YUI.add('index', function x(Y) {
    "use strict";
    var contentTemplate = Y.TemplateStore.load("index_content");
    loadModuleData('index', function(data) {
        $("#content").html(contentTemplate(data));
    });
}, '1.0.0', {requires : ['templates/index']});