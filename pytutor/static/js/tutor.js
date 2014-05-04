
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
    //Trying to add either of these doesn't work. :(
    //var promptEditor = configureEditor("prompt-editor");
    //var solutionEditor = ace.edit("solution-editor");

    /*$("#question-form").submit(function ( event) 
    {
        // Stop form from submitting normally
        event.preventDefault();
        var $form = $( this );
        
        //var promptCode = promptEditor.getValue();
        var solutionCode = solutionEditor.getValue();
        //$("#id_prompt").val(promptCode);
        $("#id_solution").val(solutionCode);
        var data = $form.serialize();
        var url = $form.attr( "action" );
        $('form').unbind().submit();     
    });*/


    //response form stuff
    var responseEditor = configureEditor("response-editor");

    $("#response-form").submit(function ( event) 
    {
        // Stop form from submitting normally
        event.preventDefault();
        var $form = $( this );
        
        var code = responseEditor.getValue();
        $("#user_code").val(code);
        var data = $form.serialize();
        var url = $form.attr( "action" );
        $('form').unbind().submit();     
    });
});

