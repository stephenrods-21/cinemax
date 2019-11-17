$(document).ready(() => {

    $(document).on('click', '.approve-request', function (e) {
        $(this).attr('disabled', true);
        e.preventDefault();
        var transactionId = $(this).attr('data-transaction-id');

        $.ajax({
            //headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "GET",
            beforeSend: function () {
                $('.ajax-loader').css("visibility", "visible");
            },
            url: '/updateTransactionStatus/' + transactionId + '/1',
            context: this,
            success: function (data) {
                window.location.reload();
            },
            complete: function () {
                $('.ajax-loader').css("visibility", "hidden");
            }
        });
    });

    $(document).on('click', '.reject-request', function (e) {
        $(this).attr('disabled', true);
        e.preventDefault();
        var transactionId = $(this).attr('data-transaction-id');

        $.ajax({
            //headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "GET",
            beforeSend: function () {
                $('.ajax-loader').css("visibility", "visible");
            },
            url: '/updateTransactionStatus/' + transactionId + '/0',
            context: this,
            success: function (data) {
                window.location.reload();
            },
            complete: function () {
                $('.ajax-loader').css("visibility", "hidden");
            }
        });
    });

    $(document).on('click', '.approve-pr-request', function (e) {
        $(this).attr('disabled', true);
        e.preventDefault();
        var transactionId = $(this).attr('data-transaction-id');

        $.ajax({
            //headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "GET",
            beforeSend: function () {
                $('.ajax-loader').css("visibility", "visible");
            },
            url: '/updatePRTransactionStatus/' + transactionId + '/1',
            context: this,
            success: function (data) {
                window.location.reload();
            },
            complete: function () {
                $('.ajax-loader').css("visibility", "hidden");
            }
        });
    });

    $(document).on('click', '.reject-pr-request', function (e) {
        $(this).attr('disabled', true);
        e.preventDefault();
        var transactionId = $(this).attr('data-transaction-id');

        $.ajax({
            //headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "GET",
            beforeSend: function () {
                $('.ajax-loader').css("visibility", "visible");
            },
            url: '/updatePRTransactionStatus/' + transactionId + '/0',
            context: this,
            success: function (data) {
                window.location.reload();
            },
            complete: function () {
                $('.ajax-loader').css("visibility", "hidden");
            }
        });
    });

});