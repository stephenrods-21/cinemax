$(document).ready(() => {
    var j = 0;
    var lastIndx = 0;
    var levelIndx = 0;
    var reload = false;

    $(document).on('click', '.remove-level', function (e) {
        if (confirm("Are you sure you want to delete this level?")) {
            reload = true;
            var levelCounter = 0;
            var levelIndx = $(this).attr('data-level-indx');
            $('#LevelBlock' + levelIndx).remove();
            levelCounter += 1;

            var deletedLevel = $(this).attr('data-level-indx');
            var newIndex = parseInt(deletedLevel);
            var prevLevel = newIndex;
            $('.approver-line-item').each((idx, elm) => {
                var currentLevel = $(elm).find('[name="level"]').val();
                if (currentLevel >= deletedLevel) {
                    $(elm).find('[name="level"]').val(currentLevel - 1);
                }
                prevLevel = currentLevel;
            });
            $('.loa-form').submit();
        }
    });

    $('#AddLevel').click(function (e) {
        j += 1;
        levelIndx = $(this).attr('data-level-indx');
        console.log(levelIndx)
        if (levelIndx == NaN || levelIndx == "None")
            levelIndx = 0;
        else {
            levelIndx = parseInt($(this).attr('data-level-indx'));
        }

        lastIndx += 1;
        levelIndx += 1;
        $(this).attr('data-last-indx', lastIndx);
        $(this).attr('data-level-indx', levelIndx);

        var htm = $('#LoaTemplate').html();
        htm = htm.replace(/\approval-rule/g, 'approval-rule-list')
        htm = htm.replace(/\{idx}/g, levelIndx)
        htm = htm.replace(/\{j}/g, j)
        htm = htm.replace(/\{level}/g, 'Level #' + levelIndx)
        htm = htm.replace(/\{levelindx}/g, levelIndx)
        htm = htm.replace(/\{lastindx}/g, 1)
        htm = htm.replace(/\{lblApprover}/g, 'Approver #' + 1)
        htm = htm.replace(/\"display: none;"/g, '')

        $('#LoaDetails').append(htm);
    });

    $(document).on('click', '.delete-loa', function (e) {
        if (confirm("Are you sure you want to delete this line of approval?")) {
            e.preventDefault();
            var loaId = $(this).attr('data-loa-id');
            $.ajax({
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                type: "POST",
                url: "/deletelineofapproval/" + loaId,
                data: {},
                context: this,
                success: function (data) {
                    console.log(data);
                    window.location.href = '/lineofapprovals';
                }
            });
        }
    });

    $(document).on('click', '.add-approver', function (e) {
        debugger
        var lineIndx = $(this).attr('data-indx');
        var lastIndx = parseInt($(this).attr('data-last-indx'));
        lastIndx += 1;
        j += 1;
        $(this).attr('data-last-indx', lastIndx);

        var htm = $('#LevelSchema').html();
        htm = htm.replace(/\{j}/g, j);
        htm = htm.replace(/\{idx}/g, lastIndx);
        htm = htm.replace(/\approver-line/g, 'approver-line-item');
        htm = htm.replace(/\{level}/g, parseInt($(this).attr('data-level-indx')));
        htm = htm.replace(/\{lblApprover}/g, 'Approver #' + lastIndx);
        htm = htm.replace(/\"display: none;"/g, '');

        $('#ApprovalRule' + lineIndx).find('[name="requiredapproval"]').attr('max', lastIndx);
        $('#ApprovalRule' + lineIndx).find('[name="totalapproval"]').val(lastIndx);

        $('#ApproverList' + lineIndx).append(htm);

    });

    $(document).on('submit', '.loa-form', (e) => {
        $(this).attr('disabled', true);
        e.preventDefault();

        var approverList = [];
        var j = 0;
        $('.approver-line-item').each((idx, elm) => {
            j += 1;
            approverList.push({
                approver_id: $(elm).find('[name="approver"]').val(),
                //must_approve: $(elm).find(':checkbox:checked').length > 0 ? true : false,
                level: $(elm).find('[name="level"]').val(),
                // level: j,
                line_of_approval_id: $(elm).find('[name="lineOfApprovalId"]').val(),
                line_of_approval_detail_id: $(elm).find('[name="lineOfApprovalDetailId"]').val()
            })
        });

        var filteredApproverList = [];
        for (var i = 0; i < approverList.length; i++) {
            if (approverList[i].approver_id != "")
                filteredApproverList.push(approverList[i])
        }

        var approvalRuleList = [];
        var i = 1;
        $('.approval-rule-list').each((idx, elm) => {
            approvalRuleList.push({
                level: i,
                required_approval: $(elm).find('[name="requiredapproval"]').val()
            })
            i++;
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

        console.log({ data: JSON.stringify(model), approverList: JSON.stringify(filteredApproverList), approvalRuleList: JSON.stringify(approvalRuleList) })
        $.ajax({
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: "POST",
            beforeSend: function () {
                $('.ajax-loader').css("visibility", "visible");
            },
            url: postUrl,
            data: { data: JSON.stringify(model), approverList: JSON.stringify(filteredApproverList), approvalRuleList: JSON.stringify(approvalRuleList) },
            context: this,
            success: function (data) {
                if (reload) {
                    window.location.reload();
                    reload = false;
                }
                else
                    window.location.href = '/lineofapprovals';

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

})