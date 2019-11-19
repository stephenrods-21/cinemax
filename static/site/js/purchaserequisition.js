$(document).ready(() => {

    var i = 0;
    $("#add_row").click(function () {
        debugger
        lastIdx = parseInt($(this).attr('data-last-indx'));
        newIndx = lastIdx + 1;
        $(this).attr('data-last-indx', newIndx);
        //b = i - 1;
        $('#addr' + (newIndx)).html($('#addr' + lastIdx).html()).find('input').val('').find('td:first-child').html(newIndx);
        $('#tab_logic').append('<tr id="addr' + (newIndx+1) + '" class="pr-line-item"></tr>');
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


    $(document).on('submit', '.edit-purchaserequisition-form', function (e) {
        e.preventDefault();
        console.log("HITT")

        var form = $(".edit-purchaserequisition-form");
        var model = {
            id: $("[name='id']", form).val() == '' ? 0 : $("[name='id']", form).val(),
            budgetid: $("[name='budgetid']", form).val(),
            title: $("[name='title']", form).val(),
            vendorname: $("[name='vendorname']", form).val(),
            vendoraccount: $("[name='vendoraccount']", form).val(),
            amount: $("[name='amount']", form).val(),
        };

        var lineItems = []
        $('.pr-line-item').each((idx, elm) => {
            lineItems.push({
                lineid: $(elm).find('[name="lineid"]').val(),
                linedescription: $(elm).find('[name="linedescription"]').val(),
                lineamount: $(elm).find('[name="lineamount"]').val(),
                lineremark: $(elm).find('[name="lineremark"]').val(),
            })
        });

        lineItems.pop();

        console.log({ data: JSON.stringify(model), lineitems: JSON.stringify(lineItems) })

        var postUrl = $("[name='id']", form).val() == 0 ? '/editpurchaserequisition/' + model.id + '/' + (model.budgetid == "" ? 0 : model.budgetid) : '/updatepurchaserequisition';

        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "POST",
            beforeSend: function () {
                $('.ajax-loader').css("visibility", "visible");
            },
            url: postUrl,
            data: { data: JSON.stringify(model), lineitems: JSON.stringify(lineItems) },
            context: this,
            success: function (data) {
            },
            complete: function () {
                $('.ajax-loader').css("visibility", "hidden");
                window.location.href = '/purchaserequisition';
            }
        });
        return false;
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

});