//foo


var editors = Array();

function configureEditor(id) 
{
    // configure ace editor
    var editor = ace.edit(id);
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
    editor.getSession().setUseWrapMode(true);
    editor.getSession().setUseSoftTabs(true);
    editors[id] = editor;
    return editor;
}

/**
 * Copy the from ace editor into a hidden filed to 
 * submit user-generated code
 */
function copyEditorCode(id)
{
    var codeField = $("#" + id).data("codeField");
    var editor = editors[id];
    var code = editor.getValue();
    $("input[name=" + codeField + "]").val(code);
}

function initEditors()
{

    $('.code-editor.lang-bash').each(function(i, editor) {
        var ace = configureEditor(editor);
        ace.renderer.setShowGutter(false); 
        ace.getSession().setMode("ace/mode/sh");
        ace.setTheme("ace/theme/chrome");

        ace.setOptions({
            readOnly: true,
            highlightActiveLine: false,
            highlightGutterLine: false
        });

        var code = $(editor).html()
        var linesOfCode = code.split("\n");
        $(editor).height((linesOfCode.length * 1.5 + 2) + "em");

    });

    if($("#user-code").length)
    {
        var userCodeEditor = configureEditor("user-code");
    }

    if($("#response-editor").length)
    {
        configureEditor("response-editor");
        $("#submit-user-code").click(function (event) 
        {
            copyEditorCode("response-editor");
            $("#response-form").submit();
        });
    }

    if($("#prompt-editor").length)
    {
        var prompt = configureEditor("prompt-editor");
        prompt.getSession().setMode("ace/mode/markdown");        
        
        configureEditor("solution-editor");

        $("#save-question").click(function (event) 
        {
            copyEditorCode("prompt-editor");
            copyEditorCode("solution-editor");
            $("#question-form").submit();
        });
    }
}




$( document ).ready(function() {
    
    //question form stuff
    $( "#test-form" ).submit(function( event ) 
    {
        //
        if ($( '#version' ).html() == '0') {
            event.preventDefault();
            // $( '#messages' ).css('visibility','visible');
            // $( '#messages' ).css('height','auto');
            $( '#messages' ).show();
            $( '#message_list' ).append( "<li>You must create a function name and prompt before adding unit tests.</li>" );
        } else {
            // Stop form from submitting normally
            event.preventDefault();

            var $form = $( this );
            var data = $form.serialize();   
            var url = $form.attr( "action" );

            $.post( url, data ).success(function( response ) {
                if ( response.success ){
                    $( "#unit-tests ul" ).append( response.list_append );
                    $( '#messages' ).show();
                    if ( response.passed ){
                        $( '#message_list' ).append( "<li>" + response.assert_code + "</li>" );
                    } else {
                        $( '#message_list' ).append( "<li>Test successfully added.</li>" );
                        $( '#message_list' ).append( "<li>New test failed on Solution code. "
                            + "Check this test case and your solution code to fix the issue.</li>" );
                    }
                } else {
                    //data not valid
                    $( '#messages' ).css('visibility','visible');
                    $( '#messages' ).css('height','auto');
                    $( '#message_list' ).append( "<li>" + response.message + "</li>" );
                }
            });
        }
    });

    initEditors();


    $("#question-form :text").each(function(){
        $( this ).addClass("form-control");
    });
    $("#question-form select").each(function(){
        $( this ).addClass("form-control");
    });
    $("#question-form textarea ").each(function(){
        $( this ).addClass("form-control");
    });
    $("#test-form :text").each(function(){
        $( this ).addClass("form-control");
    });
    $( "#id_comment").val("");




});
