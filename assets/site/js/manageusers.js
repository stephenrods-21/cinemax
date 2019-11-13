$(document).ready(() => {

    $(document).on('submit', '.edit-user-form', (e) => {
        $(this).attr('disabled', true);
        e.preventDefault();

        var form = $(".edit-user-form");
        var userId = $("[name='id']", form).val() == '' ? 0 : $("[name='id']", form).val();
        var model = {
            id: userId,
            username: $("[name='username']", form).val(),
            password: $("[name='password']", form).val(),
            email: $("[name='email']", form).val(),
            businessunit: $("[name='businessunit']", form).val(),
            role: $("[name='role']", form).val()
        };

        var postUrl = $("[name='id']", form).val() == '' ? '/edituser/' + userId : '/updateuser';

        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "POST",
            url: postUrl,
            data: { data: JSON.stringify(model) },
            context: this,
            success: function (data) {
                console.log(data);
                window.location.href = '/manageusers';
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