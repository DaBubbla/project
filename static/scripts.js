// Easier way to highlight important html data

$(document).ready(function() {

    // Select table data
    let signal = $('table tr#row td#signal');


    // Remove unneccessary signal data
    $(signal).each(function(){
        if( $(this).text() == 'upper' || $(this).text() == 'down' ) {
            $(this).hide();
        }
    });

    // Highlight Bear flips
    $(signal).each(function(){
        if( $(this).text() == 'BEAR' || $(this).text() == 'BULL' ) {
            $(this).parent().css('border', '2px solid orange');
        }
    });


    // Highlight buy signals
    $(signal).each(function(){
        if( $(this).text() == 'BUY_PERF' || $(this).text() == 'BUY_SIGNAL' ) {
            $(this).parent().css('background', '#28a745');
        }
    });

    // Highlight buy / sell perfs
    $(signal).each(function(){
        if( $(this).text() == 'SELL_PERF' || $(this).text() == 'SELL_SIGNAL' ) {
            $(this).parent().css('background', '#dc3545');
        }
    });

});