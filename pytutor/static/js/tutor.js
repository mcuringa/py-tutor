

// Attach a submit handler to the form
$( "#test-form" ).submit(function( event ) 
{
    // Stop form from submitting normally
    event.preventDefault();
    var $form = $( this );
    var data = $form.serialize();   
    var url = $form.attr( "action" );

    var posting = $.post( url, data );
    // Put the results in a div
    posting.done(function( data ) {
        var content = $( data ).find( "#content" );
        $( "#result" ).empty().append( content );
    });
});


