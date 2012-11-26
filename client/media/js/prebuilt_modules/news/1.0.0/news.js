YUI.add('templates/news', function (Y) {
    "use strict";
    Y.TemplateStore.store("news_content", Handlebars.compile("<div>Template itself (news module)</div>"));
}, '0.0.1', {requires:['template-store']});

YUI.add('news', function x(Y) {
    "use strict";
    alert('news module loaded');
}, '1.0.0', {requires : ['templates/news']});