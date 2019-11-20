$(document).ready(() => {

    // $(document).on('click', '#upload', function(e) {
    //     console.log("UPLOAD")
    //     $('#zmr').click();
    // });


    // $(document).on('submit', '#id_ajax_upload_form', function (e) {
    //     e.preventDefault();
    //     $form = $(this)
    //     var formData = new FormData(this);
    //     $.ajax({
    //         url: '/upload',
    //         type: 'POST',
    //         data: formData,
    //         success: function (response) {
    //             $('.error').remove();
    //             console.log(response)
    //             if (response.error) {
    //                 $.each(response.errors, function (name, error) {
    //                     error = '<small class="text-muted error">' + error + '</small>'
    //                     $form.find('[name=' + name + ']').after(error);
    //                 })
    //             } else {
    //                 alert(response.message)
    //                 //window.location = ""
    //             }
    //         },
    //         cache: false,
    //         contentType: false,
    //         processData: false
    //     });
    // });

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

    $(document).on('submit', '#id_ajax_upload_form', function (e) {
        $(this).attr('disabled', true);
        e.preventDefault();
        console.log("sfdsfsdfdsf")

        // var form = $(".edit-memo-form");
        // var model = {
        //     id: $("[name='id']", form).val() == '' ? 0 : $("[name='id']", form).val(),
        //     businessunit: $("[name='businessunit']", form).val(),
        //     documentno: $("[name='documentno']", form).val(),
        //     topic: $("[name='topic']", form).val(),
        //     description: $("[name='description']", form).val(),
        //     amount: $("[name='amount']", form).val()
        // };

        var form = $(".edit-memo-form");
        var id = $("[name='id']", form).val() == '' ? 0 : $("[name='id']", form).val()
        var formData = new FormData(this);
        formData.append('documentno', $("[name='documentno']", form).val())
        formData.append('amount', $("[name='amount']", form).val())
        
        var postUrl = $("[name='id']", form).val() == '' ? '/editmemo/' + id : '/updatememo';

        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "POST",
            beforeSend: function () {
                $('.ajax-loader').css("visibility", "visible");
            },
            url: postUrl,
            data: formData,
            success: function (data) {
                window.location.href = '/memo';
            },
            complete: function () {
                $('.ajax-loader').css("visibility", "hidden");
            },
            cache: false,
            contentType: false,
            processData: false
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