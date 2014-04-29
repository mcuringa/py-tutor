

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
    
    //Get all response editor divs and ace-ify them
    var count = 1;
    var responseEditor;

    $( ".aceify" ).each( function(i, obj) {
        str = "aceify" + count;
        $(this).attr("id", str);
        responseEditor = configureEditor(str);
        count++;
    });
    
    
    $( "#test-form" ).submit(function( event ) 
    {

        // Stop form from submitting normally
        event.preventDefault();
        var $form = $( this );
        var data = $form.serialize();   
        var url = $form.attr( "action" );

        var posting = $.post( url, data );
        
        posting.done(function( data ) {
            $( "#unit-tests ul" ).append( "<li>" + data + "</li>" );
        });
    });

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

