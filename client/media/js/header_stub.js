$(function(){
    $('#header a').click(function(eventObject){
        router.navigate(eventObject.target.pathname, {trigger:true});
        return false;
    });
});