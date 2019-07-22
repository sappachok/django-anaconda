(function(){
    var $ = django.jQuery;
    $(document).ready(function(){
        $('textarea.html-editor').each(function(idx, el){
            CodeMirror.fromTextArea(el, {
                mode: {name: "python",
					   version: 3,
					   singleLineStringErrors: false},
				lineNumbers: true,
				indentUnit: 4,
				matchBrackets: true
            });
        });
    });
})();