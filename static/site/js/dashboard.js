$(document).ready(() => {

    $(document).on('click', '.approve-request', function (e) {
        e.preventDefault();
        var transactionId = $(this).attr('data-transaction-id');

        $.ajax({
            //headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "GET",
            url: '/updateTransactionStatus/' + transactionId + '/1',
            context: this,
            success: function (data) {
               // window.location.reload();
            }
        });
    })

    $(document).on('click', '.reject-request', function (e) {
        e.preventDefault();
        var transactionId = $(this).attr('data-transaction-id');

        $.ajax({
            //headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "GET",
            url: '/updateTransactionStatus/' + transactionId + '/0',
            context: this,
            success: function (data) {
                console.log(data.status)
                //window.location.reload();
            }
        });
    })

});