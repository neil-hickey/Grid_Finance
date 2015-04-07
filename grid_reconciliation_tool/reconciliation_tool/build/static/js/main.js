
/* Formatting function for row details - modify as you need */
function format ( d ) {
    // `d` is the original data object for the row
    return '<div class="slider">' +
        '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
            '<tr>' +
                '<td>Full name:</td>' +
                '<td>'+d.Username+'</td>' +
            '</tr>' +
        '</table>' +
    '</div>';
}


jQuery(function ($) { // $(document).ready()
    $('#calculate').hide();

    // calcuate ajax call
    $('#calculate').on('click', function () {
        $('#result').html(' <table id="report_table" class="table table-striped" cellspacing="0" width="100%"> \
            <thead> \
                <tr> \
                    <th></th> \
                    <th>Row #</th> \
                    <th>Username</th> \
                    <th>Amount</th> \
                    <th>Match Rate (%)</th> \
                    <th>Manual Status</th> \
                </tr> \
            </thead> \
        </table>');
        
        var table = $('#report_table').DataTable( {
            "ajax": {
                "url": "/report",
                "dataSrc": ""
            },
            stateSave: true,
            "columns": [
                {
                    "class":          "details-control",
                    "orderable":      false,
                    "data":           null,
                    "defaultContent": ""
                },
                { "data": "Row #" },
                { "data": "Username" },
                { "data": "Amount" },
                { "data": "Match Rate (%)" },
                { "data": "Manual Status" }
            ],
            "lengthMenu": [[25, 50, 75, -1], [25, 50, 75, "All"]]
        } );

        // Add event listener for opening and closing details
        $('#report_table tbody').on('click', 'td.details-control', function () {
            var tr = $(this).closest('tr');
            var row = table.row( tr );
     
            if ( row.child.isShown() ) {
                // This row is already open - close it
                $('div.slider', row.child()).slideUp( function () {
                    row.child.hide();
                    tr.removeClass('shown');
                } );
            }
            else {
                // Open this row
                row.child( format(row.data()), 'no-padding' ).show();
                tr.addClass('shown');
                $('div.slider', row.child()).slideDown();
            }
        } );


        $('#calculate').hide();

        // $.get( "/report", function( data ) {
        //     $( "#result" ).html( data );
        //     $('.dataframe').dataTable(  {
        //         "lengthMenu": [[25, 50, 75, -1], [25, 50, 75, "All"]]
        //     } );
        //     // var dynatable = $('.dataframe').data('dynatable');
        //     // alert(JSON.stringify(dynatable.records.getFromTable()));

        //     $('#calculate').hide();
        //     // Table is converted with a border which must be removed
        //     $(".dataframe").removeAttr("border");
        //     // $(".dataframe").attr("border","0");
        // }).fail(function() {
        //     $( "#result").html( '<div class="alert alert-danger" role="alert" style="margin-top:10px">' + 
        //                         '<span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>' +
        //                         '<span class="sr-only">Error:</span>' +
        //                         ' Unable to generate report!<br>' +
        //                         ' <ul>Files must be uploaded before calculating!</ul> ' +
        //                         '</div>'
        //     );
        // });
    }); // end calculate



    // spinner on ajax calls
    $body = $("body");
    $(document).on({
        ajaxStart: function() { $body.addClass("loading");    },
        ajaxStop: function() { $body.removeClass("loading"); }    
    });

    // drag and drop setup
    Dropzone.options.myDropzone = {

        // Prevents Dropzone from uploading dropped files immediately
        autoProcessQueue: false,
        uploadMultiple: true,
        acceptedFiles: '.csv',
        maxFiles: 2,
        addRemoveLinks: true,
        paramName: 'file',

        init: function() {
            var submitButton = document.querySelector("#submit-all")
            myDropzone = this; // closure

            submitButton.addEventListener("click", function() {
                myDropzone.processQueue(); // Tell Dropzone to process all queued files.
            });

            // You might want to show the submit button only when 
            // files are dropped here:
            this.on("queuecomplete", function() {
                $('#calculate').show();
            });

        }
    }; // end dropzone

}); // end jquery

