var CODE_MAP = {

    TASK_STATE: {
        0 : "待处理",
        1 : "处理中",
        2 : "完成",
        3 : "关闭"
    },
    TASK_TYPE: {
        1 : "标注",
        2 : "检查",
        3 : "修正"
    },
    WORK_STATE: {
        1 : "处理中",
        2 : "完成",
        3 : "关闭"
    }
};

var KEY_MAP = {

    TASK_STATE: {
        "待处理": 0,
        "处理中": 1,
        "完成": 2,
        "关闭": 3
    },
    TASK_TYPE: {
        "标注": 1,
        "检查": 2,
        "修正": 3
    },
    WORK_STATE: {
        "处理中": 1,
        "完成": 2,
        "关闭": 3
    }
};

var TASK_TEMPLATE = {
    "id": 0,
    "pcap": {"id": 0,
             "pcap_name": ""},
    "command": {
        "dataset": {
            "range": [0, 1],
            "step": 1
        }
    },
    "type": 0,
    "state": 0,
    "work": {
        "worker": {
            "id": 0,
            "name": ""
        },
        "state": 0
    },
    "description": ""
}

function newMode() {

    $("#new-btn").attr("disabled", true);
    $("#save-btn").attr("disabled", false);
    $("#delete-btn").attr("disabled", true);
    $("#submit-btn").attr("disabled", true);

    $("#state-label").text("新建");
    FormReadOnly(false);

    MODE = 1;
}

function editMode(new_task) {

    $("#new-btn").attr("disabled", true);
    $("#save-btn").attr("disabled", false);
    $("#delete-btn").attr("disabled", false);
    $("#submit-btn").attr("disabled", true);

    $("#state-label").text("编辑");
    FormReadOnly(!new_task);

    MODE = 2;
}

function unselectMode() {

    $("#new-btn").attr("disabled", false);
    $("#save-btn").attr("disabled", true);
    $("#delete-btn").attr("disabled", true);
    $("#submit-btn").attr("disabled", false);

    $("#state-label").text("待选择");

    MODE = 0;
}

function FormReadOnly(state) {

    $("#pannel-pcap-name").attr("readonly", state);
    $("#pannel-range-start").attr("readonly", state);
    $("#pannel-range-end").attr("readonly", state);
    $("#pannel-range-step").attr("readonly", state);
    $("#pannel-task-type").attr("readonly", state);
    $("#pannel-work-name").attr("readonly", state);

    $("#pannel-description").attr("readonly", state);
}

function TaskList() {


    this.newRow = function(task, row_id, bg_color) {

        var row = document.createElement("tr");
        if (bg_color) {
            row.bgColor = bg_color
        }
        row.id =  row_id;

        var task_id_text = parseInt(task.id) > 0? parseInt(task.id): "new";
        var task_id_cell = document.createElement("td");
        task_id_cell.appendChild(document.createTextNode(task_id_text));    

        var pcap_cell = document.createElement("td");
        pcap_cell.appendChild(document.createTextNode(task.pcap.pcap_name));

        var command_cell = document.createElement("td");
        command_cell.appendChild(document.createTextNode(`[${task.command.dataset.range[0]}-${task.command.dataset.range[1]}]|${task.pcap.max_of_sequence}\
                                                            step-${task.command.dataset.step}`));

        var type_cell = document.createElement("td");
        type_cell.appendChild(document.createTextNode(CODE_MAP.TASK_TYPE[task.type]));

        var state_cell = document.createElement("td");
        state_cell.appendChild(document.createTextNode(CODE_MAP.TASK_STATE[task.state]));

        var worker_cell = document.createElement("td");
        worker_cell.appendChild(document.createTextNode(task.work.worker.name));

        var work_state_cell = document.createElement("td");
        work_state_cell.appendChild(document.createTextNode(CODE_MAP.WORK_STATE[task.work.state]));

        var des_cell = document.createElement("td");
        des_cell.appendChild(document.createTextNode(task.description));

        row.appendChild(task_id_cell);
        row.appendChild(pcap_cell);
        row.appendChild(command_cell);
        row.appendChild(type_cell);
        row.appendChild(state_cell);
        row.appendChild(worker_cell);
        row.appendChild(work_state_cell);
        row.appendChild(des_cell);

        return row;
    }

    this.fresh = function() {

        document.getElementById("tasktable-body").remove();
        var table_body = document.createElement("tbody");
        table_body.id = "tasktable-body";
        document.getElementById("tasktable").appendChild(table_body);

        for (var it in TASKS) {
            var task = TASKS[it];
            
            var row = null;
            if ( task.delete ) {
                row = this.newRow(task, "task_row_" + task.id, "#FFC1C1");
            }else {
                row = this.newRow(task, "task_row_" + task.id);
            }
            row.child_task_idx = it;
            document.getElementById("tasktable-body").appendChild(row);

            $("#" + row.id).dblclick(function () {

                var task_idx = parseInt($(this).prop("child_task_idx"));
                var task = TASKS[task_idx];

                if (!confirm("是否编辑?")) {
                    return;
                }

                TASK_PANEL.fresh(task);
                CURRENT_TASK = JSON.parse(JSON.stringify(task));
                CURRENT_TASK_PTR = task;
                editMode(false);
            });
            
            if ( task.modify ) {
                var row = this.newRow(task.modify, "task_row_modify_" + task.id, "#FFEC8B");
                document.getElementById("tasktable-body").appendChild(row);
            }
        }

        for (var nit in NEW_TASKS) {
            var new_task = NEW_TASKS[nit];

            if ( new_task.delete ) {
                continue;
            }

            var row = this.newRow(new_task, "new_task_row_" + nit, "#B4EEB4");
            row.child_task_idx = nit;
            document.getElementById("tasktable-body").appendChild(row);

            $("#" + row.id).dblclick(function () {

                var task_idx = parseInt($(this).prop("child_task_idx"));
                var new_task = NEW_TASKS[task_idx];

                if (!confirm("是否编辑?")) {
                    return;
                }

                TASK_PANEL.fresh(new_task);
                CURRENT_TASK_PTR = new_task;
                CURRENT_TASK = new_task;
                editMode(true);
            });
        }
    }
}

function IfEditChange() {
    CollectCurrentInformation();
    var changed = !((CURRENT_TASK.work.state === CURRENT_TASK_PTR.work.state) &
                    (CURRENT_TASK.state === CURRENT_TASK_PTR.state));
    return changed;
}

function CollectCurrentInformation() {
    CURRENT_TASK.id = $("#pannel-task-id").val();
  
    let pcap_info = $("#pannel-pcap-name").val().split(":");
    CURRENT_TASK.pcap.id = parseInt(pcap_info[0]);
    CURRENT_TASK.pcap.pcap_name = pcap_info[1];

    CURRENT_TASK.command.dataset.range[0] = $("#pannel-range-start").val();
    CURRENT_TASK.command.dataset.range[1] = $("#pannel-range-end").val();
    CURRENT_TASK.command.dataset.step = $("#pannel-range-step").val();
    CURRENT_TASK.type = KEY_MAP.TASK_TYPE[$("#pannel-task-type").val()];
    CURRENT_TASK.state = KEY_MAP.TASK_STATE[$("#pannel-task-state").val()];

    let worker = $("#pannel-work-name").val().split(":");
    CURRENT_TASK.work.worker.id = parseInt(worker[0]);
    CURRENT_TASK.work.worker.name = worker[1];

    CURRENT_TASK.work.state = KEY_MAP.WORK_STATE[$("#pannel-work-state").val()];
    CURRENT_TASK.description = $("#pannel-description").val();
}

function TaskPanel() {

    this.fresh = function(task) {
        $("#pannel-task-id").val(task.id);
        $("#pannel-pcap-name").val(task.pcap.id + ":" + task.pcap.pcap_name);
        $("#pannel-range-start").val(task.command.dataset.range[0]);
        $("#pannel-range-end").val(task.command.dataset.range[1]);
        $("#pannel-range-step").val(task.command.dataset.step);

        $("#pannel-task-type").val(CODE_MAP.TASK_TYPE[task.type]);
        $("#pannel-task-state").val(CODE_MAP.TASK_STATE[task.state]);

        $("#pannel-work-name").val(task.work.worker.id + ":" + task.work.worker.name);
        $("#pannel-work-state").val(CODE_MAP.WORK_STATE[task.work.state]);

        $("#pannel-description").val(task.description);
    }

    this.init = function() {

        unselectMode();

        $("#pannel-task-id").val("");
        $("#pannel-pcap-name").val("");
        $("#pannel-range-start").val("");
        $("#pannel-range-end").val("");
        $("#pannel-range-step").val("");

        $("#pannel-task-type").val("");
        $("#pannel-task-state").val("");

        $("#pannel-work-name").val("");
        $("#pannel-work-state").val("");

        $("#pannel-description").val("");
    }
}

$("#save-btn").click(function(){

    if (!confirm("是否保存?")) {
        TASK_LIST.fresh();
        return;
    }

    if (MODE === 2) {
        if (IfEditChange()) {
            CollectCurrentInformation();
            if (parseInt(CURRENT_TASK_PTR.id) > 0) {
                CURRENT_TASK_PTR.modify = JSON.parse(JSON.stringify(CURRENT_TASK));
            }
        }
    } else if (MODE === 1) {
        CollectCurrentInformation();
        var new_task = JSON.parse(JSON.stringify(CURRENT_TASK));
        CURRENT_TASK_PTR = new_task;
        new_task.id = 0;
        NEW_TASKS.push(new_task);
    }

    TASK_LIST.fresh();
    TASK_PANEL.init();
});

$("#new-btn").click(function(){

    if (!confirm("是否新建?")) {
        TASK_LIST.fresh();
        return;
    }

    TASK_PANEL.init();
    newMode();
    CURRENT_TASK = JSON.parse(JSON.stringify(TASK_TEMPLATE));
    CURRENT_TASK.delete = false;
});

$("#delete-btn").click(function(){

    if ( MODE !== 2 ) {
        return;
    }

    if (!confirm("是否删除?")) {
        TASK_LIST.fresh();
        return;
    }

    CURRENT_TASK_PTR.delete = true;

    TASK_LIST.fresh();
    TASK_PANEL.init();
});

$("#submit-btn").click(function(){

    var delete_task_list = [];
    var modify_task_list = [];
    for (var it in TASKS) {
        var task = TASKS[it];

        if ( !task.delete ) {
            if ( task.modify ) {
                modify_task_list.push(task);
            }
        }else {
            delete_task_list.push(task);
        }
    }

    var new_task_lsit = [];
    for (var it in NEW_TASKS) {
        var task = NEW_TASKS[it];

        if ( !task.delete ) {
            new_task_lsit.push(task);
        }
    }

    var message = "new:\n"
    for (it in new_task_lsit) {
        var task = new_task_lsit[it];
        message += "    - id: " + (task.id + "\n")

    }

    message += "delete:\n"
    for (it in delete_task_list) {
        var task = delete_task_list[it];
        message += "    -id: " + (task.id + "\n")

    }

    message += "modify:\n"
    for (it in modify_task_list) {
        var task = modify_task_list[it];
        message += "    -id: " + (task.id + "\n")

    }

    message = "是否提交?\n" + message;
    if (!confirm(message)) {
        return;
    }

    var form = {
        "delete": delete_task_list,
        "modify": modify_task_list,
        "new": new_task_lsit
    }
    $.ajax({
        url: "/update_task",   
        type: "POST", //请求方法
        data: JSON.stringify(form),   //传送的数据
        dataType: "json", //传送的数据类型
        success: function (data) {
            
            var reply = data;
            var reply_message = "Success:\n";

            reply_message += "new:\n";
            for (let i in reply.new) {
                reply_message += "    -id: " + reply.new[i] + "\n";
            }

            reply_message += "delete:\n";
            for (let i in reply.delete) {
                reply_message += "    -id: " + reply.delete[i] + "\n";
            }

            reply_message += "modify:\n";
            for (let i in reply.modify) {
                reply_message += "    -id: " + reply.modify[i] + "\n";
            }

            alert(reply_message);
            location.reload();
            
        }
    })
});