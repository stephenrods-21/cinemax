$(document).ready(() => {
    calculatetotal();

    var i = 0;
    $("#add_row_po_line").click(function () {
        lastIdx = parseInt($(this).attr('data-last-indx'));
        newIndx = lastIdx + 1;
        $(this).attr('data-last-indx', newIndx);
        //b = i - 1;
        $('#addrpoline' + (newIndx)).html($('#addrpoline' + lastIdx).html()).find('input').val('').find('td:first-child').html(newIndx);
        $('#tab_logic').append('<tr id="addrpoline' + (newIndx + 1) + '" data-indx="' + (newIndx + 1) + '" class="po-pr-line-item"></tr>');
        //i++;
    });
    $("#delete_row").click(function () {
        if (i > 1) {
            $("#addr" + (i - 1)).html('');
            i--;
        }
        //calc();
    });

    $('#tab_logic tbody').on('keyup change', function () {
        //calc();
    });
    $('#tax').on('keyup change', function () {
        //calc_total();
    });

    $(document).on('change', '#PRNumber', (e) => {
        if ($('#PRNumber').val() != '') {
            $.ajax({
                //headers: { "X-CSRFToken": getCookie("csrftoken") },
                type: "GET",
                url: '/purchaseorder/getprdetail/' + $('#PRNumber').val(),
                context: this,
                success: function (data) {
                }
            });
        }
    });

    $(document).on('submit', '.edit-purchaseorder-form', function (e) {
        e.preventDefault();

        var form = $(".edit-purchaseorder-form");
        var id = $("[name='id']", form).val() == '' ? 0 : $("[name='id']", form).val()
        var formData = new FormData(this);
        formData.append('prid', $("[name='prid']", form).val())

        var lineItems = []
        $('.po-pr-line-item').each((idx, elm) => {
            lineItems.push({
                prlineid: $(elm).find('[name="prlineitems"]').val(),
                linequantity: $(elm).find('[name="linequantity"]').val(),
                lineunitprice: $(elm).find('[name="lineunitprice"]').val(),
                lineamount: $(elm).find('[name="lineamount"]').val(),
            })
        });

        lineItems.pop();
        formData.append('lineitems', JSON.stringify(lineItems))

        var postUrl = $("[name='id']", form).val() == '' ? '/purchaseorder/editpurchaseorder/' + id + '/0' : '/purchaseorder/updatepurchaseorder';

        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "POST",
            beforeSend: function () {
                $('.ajax-loader').css("visibility", "visible");
            },
            url: postUrl,
            data: formData,
            success: function (data) {
            },
            complete: function () {
                $('.ajax-loader').css("visibility", "hidden");
                window.location.href = '/purchaseorder/list'
            },
            cache: false,
            contentType: false,
            processData: false
        });
        return false;
    });

    $(document).on('change', '.po-pr-line-items', function (e) {
        var prLineId = $(this).val();
        var indx = $(this).attr('data-indx');

        var trid = $(this).closest('tr').attr('data-indx');
        var amount = $(this).closest('tr').find('.amount').val();

        if (prLineId != '') {
            $.ajax({
                //headers: { "X-CSRFToken": getCookie("csrftoken") },
                type: "GET",
                url: '/purchaseorder/getprlinedetail/' + prLineId,
                context: this,
                success: function (data) {
                    //console.log(data)
                    $(this).closest('tr').find('.amount').val(data.amount);
                    $(this).closest('tr').find('.quantity').val(1);
                    $(this).closest('tr').find('.price').val(data.amount);
                    calculatetotal();
                }
            });
        }
    })

    function calculatetotal() {
        var grandTotal = 0;
        $('.po-pr-line-item').each((idx, elm) => {
            var lineamount = $(elm).find('[name="lineamount"]').val();
            if (lineamount != undefined) {
                grandTotal += parseFloat(lineamount);
            }
        });
        $('#GrandTotal').text(grandTotal);
    }

    $(document).on('click', '.approve-po-request', function (e) {
        $(this).attr('disabled', true);
        e.preventDefault();
        var transactionId = $(this).attr('data-transaction-id');

        $.ajax({
            //headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "GET",
            beforeSend: function () {
                $('.ajax-loader').css("visibility", "visible");
            },
            url: '/purchaseorder/updatePOTransactionStatus/' + transactionId + '/1',
            context: this,
            success: function (data) {

            },
            complete: function () {
                $('.ajax-loader').css("visibility", "hidden");
                window.location.reload();
            }
        });
    });

    $(document).on('click', '.reject-po-request', function (e) {
        $(this).attr('disabled', true);
        e.preventDefault();
        var transactionId = $(this).attr('data-transaction-id');

        $.ajax({
            //headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "GET",
            beforeSend: function () {
                $('.ajax-loader').css("visibility", "visible");
            },
            url: '/purchaseorder/updatePOTransactionStatus/' + transactionId + '/0',
            context: this,
            success: function (data) {

            },
            complete: function () {
                $('.ajax-loader').css("visibility", "hidden");
                window.location.reload();
            }
        });
    });

    function getCookie(c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
        return "";
    }
})