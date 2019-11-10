$(document).ready(() => {
    var i = 0;
    $(document).on('click', '#AddApprover', (e) => {
        i++;
        console.log("ONCHAGE")
        //console.log("Chnage")
        var htm = $('#LoaTemplate').html();
        htm = htm.replace(/\{idx}/g, i)
        htm = htm.replace(/\{lblApprover}/g, 'Approver #' + i)
        htm = htm.replace(/\"display: none;"/g, '')
        console.log(htm)
        $('#LoaDetails').append(htm);

    })

    $(document).on('submit', '.loa-form', (e) => {
        e.preventDefault();

        var approverList = [];
        $('#LoaDetails .approver-line-item').each((idx, elm) => {
            approverList.push({
                approver_id: $(elm).find('[name="approver"]').val(),
                must_approve: $(elm).find(':checkbox:checked').length > 0 ? true : false,
                line_of_approval_id: $(elm).find('[name="lineOfApprovalId"]').val(),
                line_of_approval_detail_id: $(elm).find('[name="lineOfApprovalDetailId"]').val()
            })
        });

        var form = $(".loa-form");
        var lineOfApprovalId = $("[name='id']", form).val() == '' ? 0 : $("[name='id']", form).val();
        var model = {
            id: lineOfApprovalId,
            name: $("[name='name']", form).val(),
            businessunit: $("[name='businessunit']", form).val(),
            approvers: $("[name='approverneeded']", form).val()
        };

        var postUrl = $("[name='id']", form).val() == '' ? '/editlineofapprovals/' + lineOfApprovalId : '/updatelineofapprovals';
        console.log({ data: JSON.stringify(model), approverList: JSON.stringify(approverList) });

        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "POST",
            url: postUrl,
            data: { data: JSON.stringify(model), approverList: JSON.stringify(approverList) },
            context: this,
            success: function (data) {
                console.log(data);
                window.location.href = '/lineofapprovals';
                //$('#LoginModal').html(data);
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

})