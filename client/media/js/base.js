function loadModuleData(moduleName, successCallback) {
    $.ajax('/' + moduleName + '/', {
        type : 'GET',
        success : successCallback,
        dataType:'json',
        data:{json:1},
        error:function() {
            alert('failed to get module data');
        }
    });
}
