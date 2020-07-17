function initPCAPList(pcaps) {

    for (var ip in pcaps) {
        var pcap = pcaps[ip];

        var row = document.createElement("tr");

        var pcap_id_cell = document.createElement("td");
        pcap_id_cell.appendChild(document.createTextNode(pcap.id));

        var pcap_name_cell = document.createElement("td");
        pcap_name_cell.appendChild(document.createTextNode(pcap.pcap_name));

        var lidar_type_cell = document.createElement("td");
        lidar_type_cell.appendChild(document.createTextNode(pcap.lidar_type));

        var use_check_cell = document.createElement("td");
        var use_check_box = document.createElement("input");
        use_check_box.id = "pcap_use_cb_" + pcap.id;
        use_check_box.type = "checkbox";
        use_check_cell.appendChild(use_check_box);

        var filter_range_cell = document.createElement("td");
        var filter_range_input_box = document.createElement("input");
        filter_range_input_box.id = "range_input_" + pcap.id;
        filter_range_input_box.value = "[]";
        filter_range_cell.appendChild(filter_range_input_box);

        row.appendChild(pcap_id_cell);
        row.appendChild(pcap_name_cell);
        row.appendChild(lidar_type_cell);
        row.appendChild(use_check_cell);
        row.appendChild(filter_range_cell);

        document.getElementById("pcaptable-body").appendChild(row);
    }
}

$("#generate-btn").click(function(){

    var scheme = {
        dataset: {},
        api: "http://" + window.location.host + "/apply"
    };
    for (var ip in pcaps) {
        var pcap = pcaps[ip];

        var use_cb_id = "pcap_use_cb_" + pcap.id;
        var is_use = $("#" + use_cb_id).prop('checked');

        if (!is_use) {
            continue;
        }

        var filter_range_input_id = "range_input_" + pcap.id;
        var filter_range_groups = JSON.parse($("#" + filter_range_input_id).val());

        var pcap_scheme = {  
            pcap_name: pcap.name,
            filter_range_groups: filter_range_groups,
            max_sequence: pcap.max_sequence
        }

        scheme.dataset[pcap.id] = pcap_scheme;
    }

    document.getElementById("api-cmd-show-panel").innerHTML = JSON.stringify(scheme);
});