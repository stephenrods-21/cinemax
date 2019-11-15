$(document).ready(() => {

    $(document).on('submit', '.edit-purchaserequisition-form', function (e) {
        e.preventDefault();
        console.log("HITT")

        var form = $(".edit-purchaserequisition-form");
        var model = {
            id: $("[name='id']", form).val() == '' ? 0 : $("[name='id']", form).val(),
            budgetid: $("[name='budgetid']", form).val(),
            title: $("[name='title']", form).val(),
        };

        var postUrl = $("[name='id']", form).val() == 0 ? '/editpurchaserequisition/' + model.id + '/' + model.budgetid : '/updatepurchaserequisition';

        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "POST",
            beforeSend: function () {
                $('.ajax-loader').css("visibility", "visible");
            },
            url: postUrl,
            data: { data: JSON.stringify(model) },
            context: this,
            success: function (data) {
            },
            complete: function () {
                $('.ajax-loader').css("visibility", "hidden");
                //window.location.href = '/purchaserequisition/memo';
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