YUI.add('templates/chat', function (Y) {
    "use strict";
    Y.TemplateStore.store("chat_content", Handlebars.compile('<div id="chat">Chat page.<ul>{{#each chat_module_init.messages }}<li>{{message_body}}</li>{{/each}}</ul></div>'));
}, '0.0.1', {requires:['template-store']});

YUI.add('chat', function x(Y) {
    "use strict";
    var contentTemplate = Y.TemplateStore.load("chat_content");
    loadModuleData('chat', function(data) {
        $("#content").html(contentTemplate(data));
    });
}, '1.0.0', {requires : ['templates/chat']});