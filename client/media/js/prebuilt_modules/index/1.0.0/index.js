YUI.add('templates/index', function (Y) {
    "use strict";
    Y.TemplateStore.store("index_content", Handlebars.compile("<div>Template itself (index module)</div>"));
}, '0.0.1', {requires:['template-store']});

YUI.add('index', function x(Y) {
    "use strict";
    alert('index module loaded');
}, '1.0.0', {requires : ['templates/index']});