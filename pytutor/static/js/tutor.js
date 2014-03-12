

$( document ).ready(function() {
    
    console.log($( "#test-form" ));
    
    $( "#test-form" ).submit(function( event ) 
    {
        console.log('submitting unit test');

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

