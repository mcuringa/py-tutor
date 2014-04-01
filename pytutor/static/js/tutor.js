

$( document ).ready(function() {
    
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
});

