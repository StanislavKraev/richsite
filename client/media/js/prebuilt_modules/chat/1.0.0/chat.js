YUI.add('templates/chat', function (Y) {
    "use strict";
    Y.TemplateStore.store("chat_content", Handlebars.compile('<div id="chat">Chat page.        <ul>    {{#each chat_module_init.messages }}{{>chat_message }} {{/each}}    </ul>    </div>'));    Y.TemplateStore.store("chat_message", Handlebars.compile('<li><a href="">{{message_body}}</a></li>'));
}, '0.0.1', {requires:['template-store']});

YUI.add('chat', function x(Y) {
    "use strict";
    var contentTemplate = Y.TemplateStore.load("chat_content");
    Handlebars.registerPartial('chat_message', Y.TemplateStore.load("chat_message"));

    loadModuleData('chat', function(data) {
        $("#content").html(contentTemplate(data, {}));
    });
}, '1.0.0', {requires : ['templates/chat']});