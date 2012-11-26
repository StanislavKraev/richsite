if (typeof(YUI_config) === "undefined") {
    var YUI_config = {};
}
$.extend(YUI_config, {
    "root":"",
    "base":"",
    "combine":true,
    "groups":{
        "rek":{
            "comboBase":"/combo/?",
            "root":"",
            "combine":true,
            "modules":{
                //"main_portal_css/1.10.1":{"path":"main_portal_css/1.10.1/main_portal.css", "type":"css", "name":"main_portal_css/1.10.1"},
                "template-store":{"path":"template-store/1.0.0/template-store.js", "name":"template-store"},
                "news":{"path":"news/1.0.0/news.js", "requires":["template-store"]},
                "chat":{"path":"chat/1.0.0/chat.js", "requires":["template-store"]},
                "utils":{"path":"utils/1.0.0/utils.js"},
                "index":{"path":"index/1.0.0/index.js", "requires":["template-store"]}
            }},
        "dynamic":{"comboBase":"", "combine":false, "base":"", "root":"", "modules":{}}}});

$(function(){
});