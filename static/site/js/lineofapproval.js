$(document).ready(() => {
    var j = 0;
    var lastIndx = 0;
    var levelIndx = 0;

    $(document).on('click', '#AddLevel', function () {
        // if ($(this).attr('data-last-indx') != undefined) {
        //     lastIndx = parseInt($(this).attr('data-last-indx'));
        // }
        // if ($(this).attr('data-level-indx') != undefined) {
        //     levelIndx = parseInt($(this).attr('data-level-indx'));
        // }
        j += 1;
        if (levelIndx == NaN)
            levelIndx = 0;

        lastIndx += 1;
        levelIndx += 1;
        $(this).attr('data-last-indx', lastIndx);
        $(this).attr('data-level-indx', levelIndx);

        var htm = $('#LoaTemplate').html();
        htm = htm.replace(/\{idx}/g, levelIndx)
        htm = htm.replace(/\{j}/g, j)
        htm = htm.replace(/\{level}/g, 'Level #' + levelIndx)
        htm = htm.replace(/\{levelindx}/g, levelIndx)
        htm = htm.replace(/\{lastindx}/g, 1)
        htm = htm.replace(/\{lblApprover}/g, 'Approver #' + 1)
        htm = htm.replace(/\"display: none;"/g, '')

        $('#LoaDetails').append(htm);
    });

    $(document).on('click', '.add-approver', function (e) {
        var lineIndx = $(this).attr('data-indx');
        var lastIndx = parseInt($(this).attr('data-last-indx'));
        lastIndx += 1;
        j += 1;
        $(this).attr('data-last-indx', lastIndx);

        var htm = $('#zmr').html();
        htm = htm.replace(/\{j}/g, j)
        htm = htm.replace(/\{idx}/g, lastIndx)
        htm = htm.replace(/\{level}/g, parseInt($(this).attr('data-level-indx')))
        htm = htm.replace(/\{lblApprover}/g, 'Approver #' + lastIndx)
        htm = htm.replace(/\"display: none;"/g, '')

        $('#ApproverList' + lineIndx).append(htm);
    });

    $(document).on('submit', '.loa-form', (e) => {
        e.preventDefault();

        var approverList = [];
        $('.approver-line-item').each((idx, elm) => {
            approverList.push({
                approver_id: $(elm).find('[name="approver"]').val(),
                must_approve: $(elm).find(':checkbox:checked').length > 0 ? true : false,
                level: $(elm).find('[name="level"]').val(),
                line_of_approval_id: $(elm).find('[name="lineOfApprovalId"]').val(),
                line_of_approval_detail_id: $(elm).find('[name="lineOfApprovalDetailId"]').val()
            })
        });

        var filteredApproverList = [];
        for (var i = 0; i < approverList.length; i++) {
            if (approverList[i].approver_id != "")
                filteredApproverList.push(approverList[i])
        }

        var form = $(".loa-form");
        var lineOfApprovalId = $("[name='id']", form).val() == '' ? 0 : $("[name='id']", form).val();
        var model = {
            id: lineOfApprovalId,
            name: $("[name='name']", form).val(),
            businessunit: $("[name='businessunit']", form).val(),
            approvers: $("[name='approverneeded']", form).val()
        };

        var postUrl = $("[name='id']", form).val() == '' ? '/editlineofapprovals/' + lineOfApprovalId : '/updatelineofapprovals';
        console.log({ data: JSON.stringify(model), approverList: JSON.stringify(filteredApproverList) });

        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "POST",
            url: postUrl,
            data: { data: JSON.stringify(model), approverList: JSON.stringify(filteredApproverList) },
            context: this,
            success: function (data) {
                console.log(data);
                window.location.href = '/lineofapprovals';
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