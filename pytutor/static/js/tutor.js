
function configureEditor(editorId)
{
    // configure ace editor
    var editor = ace.edit(editorId);
    editor.setTheme("ace/theme/GitHub");
    editor.getSession().setMode("ace/mode/python");
    editor.getSession().setUseSoftTabs(true);
    return editor
}


$( document ).ready(function() {

    
    //question form stuff
    $( "#test-form" ).submit(function( event ) 
    {
        //
        if ($( '#version' ).html() == '0') {
            event.preventDefault();
            $( '#message_list' ).append( "<li>You must create a function name and prompt before adding unit tests.</li>" );
        } else if ($( '#id_args' ).val() == '' || $( '#id_result' ).val() == '') {
            event.preventDefault();
            $( '#message_list' ).append( "<li>Unit tests require arguments and a result.</li>" );
        } else {
            // Stop form from submitting normally
            event.preventDefault();
            var $form = $( this );
            var data = $form.serialize();   
            var url = $form.attr( "action" );

            var posting = $.post( url, data );
            
            posting.done(function( data ) {
                $( "#unit-tests ul" ).append( "<li>" + data + "</li>" );
            });
        }
    });

    $( "#id_comment").val("");


    //response form stuff
    var responseEditor = configureEditor("response-editor");

    $("#response-form").submit(function ( event) 
    {
        console.log("response form submitted");
        // Stop form from submitting normally
        event.preventDefault();
        var $form = $( this );
        
        var code = responseEditor.getValue();
        console.log(code);
        $("#user_code").val(code);
        var data = $form.serialize();
        var url = $form.attr( "action" );
        $('form').unbind().submit();     });
});

