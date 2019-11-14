$(document).ready(() => {

    $(document).on('change', '#MemoBU', (e) => {
        if ($('#MemoBU').val() != '') {
            $.ajax({
                //headers: { "X-CSRFToken": getCookie("csrftoken") },
                type: "GET",
                url: '/getDocumentNumber/' + $('#MemoBU').val(),
                context: this,
                success: function (data) {
                    console.log(data)
                    $('#DocumentNumber').val(data.documentno);
                }
            });
        }
    })

    $(document).on('submit', '.edit-memo-form', function (e) {
        $(this).attr('disabled', true);
        e.preventDefault();

        var form = $(".edit-memo-form");
        var model = {
            id: $("[name='id']", form).val() == '' ? 0 : $("[name='id']", form).val(),
            businessunit: $("[name='businessunit']", form).val(),
            documentno: $("[name='documentno']", form).val(),
            topic: $("[name='topic']", form).val(),
            description: $("[name='description']", form).val(),
            amount: $("[name='amount']", form).val()
        };

        var postUrl = $("[name='id']", form).val() == '' ? '/editmemo/' + model.id : '/updatememo';

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
                window.location.href = '/memo';
            },
            complete: function () {
                $('.ajax-loader').css("visibility", "hidden");
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