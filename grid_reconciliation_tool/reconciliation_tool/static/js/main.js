
/* Formatting function for row details - modify as you need */
function format ( d, f ) {

    var s = d['Row #'] - 1;
    var s2 = '/report_matches/' + s;
    $.ajax({
      type: 'GET',
      url: s2,
      dataType: 'json',
      success: function(jsonData) {
        // alert(JSON.stringify(jsonData));

        var s = '<table cellpadding="5" class="table table-hover table-condensed table-bordered" cellspacing="0" border="0" style="margin-bottom: 0px; padding-left:50px;">';
        s += '<thead> \
                <tr> \
                    <th>Matching Row #</th> \
                    <th>Username</th> \
                    <th>Amount</th> \
                    <th>Match Rate (%)</th> \
                </tr> \
            </thead> \ '
        $.each(jsonData, function(idx, obj) {
            s += '<tr>'+'<td>' + obj['Matching Row #'] +'</td>' +
                 '<td>'+ obj.Username+'</td>' +
                 '<td>'+ obj.Amount+'</td>' + 
                 '<td>'+ obj['Match Rate (%)']+'</td></tr>';
        });

        s += '</table>';

        // Call back function
        f(s);
      },
      error: function() {
        console.log('Error loading');
      }
    });
}

function getConfidence() {
    $.ajax({
      type: 'GET',
      url: '/confidence',
      dataType: 'json',
      success: function(jsonData) {
        $('#confidence').html('<h2>Algorithm Accuracy vs Manual: ' + jsonData.confidence + '% </h2>');
      },
      error: function() {
        console.log('Error loading');
      }
    });
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
                    <th>Status</th> \
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
                { "data": "Status" },
                { "data": "Manual Status" }
            ],
            "lengthMenu": [[25, 50, 75, -1], [25, 50, 75, "All"]],
            "fnDrawCallback" : function() {
                getConfidence();
            }
        } );

        // Add event listener for opening and closing details
        $('#report_table tbody').on('click', 'td.details-control', function () {
            var tr = $(this).closest('tr');
            var row = table.row( tr );
     
            if ( row.child.isShown() ) {
                // This row is already open - close it
                row.child.hide();
                tr.removeClass('shown');
            }
            else {
                // Open this row
                var res = format( row.data(), function(reponse) {
                    row.child( reponse ).show();
                    tr.addClass('shown');
                    $('div.slider', row.child()).slideDown();
                });
                
            }
        } );


        $('#calculate').hide();

    }); // end calculate

    $('#fund-file').on('click', function () {
        $('#result').html(' <table id="report_table" class="table table-striped" cellspacing="0" width="100%"> \
            <thead> \
                <tr> \
                    <th>Email</th> \
                    <th>Username</th> \
                    <th>Transaction Type</th> \
                    <th>Amount</th> \
                    <th>Status</th> \
                    <th>Date</th> \
                </tr> \
            </thead> \
        </table>');
        
        var table = $('#report_table').DataTable( {
            "ajax": {
                "url": "/file_fund",
                "dataSrc": ""
            },
            stateSave: true,
            "columns": [
                { "data": "email" },
                { "data": "username" },
                { "data": "transaction type" },
                { "data": "ammount" },
                { "data": "status" },
                { "data": "date" }
            ],
            "lengthMenu": [[25, 50, 75, -1], [25, 50, 75, "All"]]
        } );
    });

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

