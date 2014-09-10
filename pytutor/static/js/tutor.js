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
    return editor
}

function copyEditorCode(id)
{
    // data-code-field <==> ___.data("codeField")
    // notice the camelCase -- first word (denoted by dashes in html)
    // not capitalized, all subsequent words have first letter capitalized
    // $ means JQuery
    var codeField = $("#" + id).data("codeField");
    var editor = editors[id];
    var code = editor.getValue();
    $("input[name=" + codeField + "]").val(code);
    // .something means 'class called something' -- the period means 'class'
    // #something means 'id called something' -- the pound sign means 'id'
    // something means 'element called something' -- <something>
    // ex:
    // input  --> <input>
    // p      --> <p>
    // div    --> <div>
    // you can specify its attributes with []--
    // ex:
    // input[name=prompt]   ---> <input name="prompt">
    // ^Select with JQuery           ^In HTML
}

function initEditors()
{


    if($("#response-editor").length)
    {
        configureEditor("response-editor");
        $("#submit-user-code").click(function (event) 
        {
            copyEditorCode(editors["response-editor"]);
            $("#response-form").submit();
        });
    }

    if($("#prompt-editor").length)
    {
        configureEditor("prompt-editor");
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
            $( '#messages' ).css('visibility','visible');
            $( '#messages' ).css('height','auto');
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
                    $( '#messages' ).css('visibility','visible');
                    $( '#messages' ).css('height','auto');
                    if ( response.passed ){
                        $( '#message_list' ).append( "<li>Test successfully added and passed.</li>" );
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
