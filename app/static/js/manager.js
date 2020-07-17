function PCTable() {

    this.current_page = 0;
    this.page_size = 30;
    this.datas = null;

    this.getTableInfo = function (datas) {
        this.datas = datas;
    }

    this.plotTable = function () {

        // clear origin
        document.getElementById("pctable-body").remove();
        var table_body = document.createElement("tbody");
        table_body.id = "pctable-body";
        document.getElementById("pctable").appendChild(table_body);

        for (var ri = 0; ri < this.datas.length; ri++) {
            var row = document.createElement("tr");
            var pc_info = this.datas[ri];
            
            var id_cell = document.createElement("td");
            var text_id = document.createElement("a");
            text_id.appendChild(document.createTextNode(pc_info.id));
            text_id.href = "http://" + window.location.host + "/viewer/" + pc_info.id;
            id_cell.appendChild(text_id );
            
            var seq_cell = document.createElement("td");
            seq_cell.appendChild(document.createTextNode(pc_info.sequence));

            var pcap_name_cell = document.createElement("td");
            pcap_name_cell.appendChild(document.createTextNode(pc_info.pcap_name));
   
            var annotaion_cell = document.createElement("td");
            annotaion_cell.appendChild(document.createTextNode(pc_info.boxes_annotations.length));
             
            row.appendChild(id_cell);
            row.appendChild(pcap_name_cell);
            row.appendChild(seq_cell);
            row.appendChild(annotaion_cell);
            document.getElementById("pctable-body").appendChild(row);
        }
    }
}

function initPCAPSelect(datas, pcap_id) {

    var item_o = document.createElement("option");
    item_o.appendChild(document.createTextNode("无"));
    document.getElementById("pcap-list-menu").appendChild(item_o);

    var select_pcap = null;
    for (let i = 0; i < datas.length; i++) {
        var pcap_info = datas[i];

        var item_o = document.createElement("option");
        item_o.appendChild(document.createTextNode(pcap_info.pcap_name));
        
        document.getElementById("pcap-list-menu").appendChild(item_o);

        if (pcap_info.id === pcap_id) {
            select_pcap = pcap_info;
        }
    }

    if (select_pcap) {
        var row = document.createElement("tr");

        var pcap_name_cell = document.createElement("td");
        pcap_name_cell.appendChild(document.createTextNode(select_pcap.pcap_name));

        var lidar_type_cell = document.createElement("td");
        lidar_type_cell.appendChild(document.createTextNode(select_pcap.lidar_type));

        row.appendChild(pcap_name_cell);
        row.appendChild(lidar_type_cell);

        document.getElementById("pcaptable-body").appendChild(row);

        $('#pcap-list-menu').val(select_pcap.pcap_name);
    }
}

$('#pcap-list-menu').on('change',function(e){

    var select_pcap_name = $(this).val();
    var pcap_info = null;
    for (let i = 0; i < pcaps.length; i++) {
        if (pcaps[i].pcap_name === select_pcap_name) {
            pcap_info = pcaps[i];
        }
    }

    var pcap_id = pcap_info?pcap_info.id:0;
    var url = "http://" + window.location.host + "/manager/" + pcap_id;
    window.location.href = url;
});
