YUI.add('templates/chat', function (Y) {
    "use strict";
    Y.TemplateStore.store("chat_content", Handlebars.compile("<div>Template itself (chat module)</div>"));
}, '0.0.1', {requires:['template-store']});

YUI.add('chat', function x(Y) {
    "use strict";
    alert('chat module loaded');
}, '1.0.0', {requires : ['templates/chat']});