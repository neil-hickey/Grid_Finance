jQuery(function ($) { // $(document).ready()

	$("#wrapper").toggleClass("toggled");

	$('#result1').html(' <table id="report_table" class="table table-striped" cellspacing="0" width="70%"> \
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

 	$('#result2').html(' <table id="report_table2" class="table table-striped" cellspacing="0" width="70%"> \
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
        
        var table = $('#report_table2').DataTable( {
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