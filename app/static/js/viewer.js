// rgb
var COLOR_MAP = {1: [1.0, 0.0, 0.0],
                 2: [0.93, 0.46, 0.13],
                 3: [0.4, 0.0, 0.6],
                 4: [0.43, 0.37, 0.93],
                 5: [0.64, 0.18, 0.08]};


function Viewer(pc) {
 
    //创建一个场景（场景是一个容器，用于保存、跟踪所要渲染的物体和使用的光源）
    this.scene = new THREE.Scene();

    //创建一个摄像机对象（摄像机决定了能够在场景里看到什么）
    this.camera = new THREE.PerspectiveCamera(45,
      window.innerWidth / window.innerHeight, 0.1, 1000);

    //设置摄像机的位置，并让其指向场景的中心（0,0,0）
    this.camera.position.x = 0.0;
    this.camera.position.y = 0.0;
    this.camera.position.z = 30.0;
    this.camera.lookAt(this.scene.position);
    
    //设置相机控制器
    this.controls = new THREE.TrackballControls( this.camera );

    this.controls.rotateSpeed = 2.0;
    this.controls.zoomSpeed = 3;
    this.controls.panSpeed = 20;

    this.controls.noZoom = false;
    this.controls.noPan = false;

    this.controls.staticMoving = true;
    this.controls.dynamicDampingFactor = 0.3;

    this.controls.minDistance = 3;
    this.controls.maxDistance = 0.3 * 10000;

    //创建一个WebGL渲染器并设置其大小
    this.renderer = new THREE.WebGLRenderer();
    this.renderer.setClearColor(new THREE.Color(0x000000));
    this.renderer.setSize(1000, 600);

    //在场景中添加坐标轴
    this.axes = new THREE.AxisHelper(20);
    this.scene.add(this.axes);

    //将渲染的结果输出到指定页面元素中
    document.getElementById("viewer-output").appendChild(this.renderer.domElement);

    //add points
    var pc = pc;
    var points = pc.points;
    var position = [];
    var color = [];

    var xp = pc.offset.x;
    var yp = pc.offset.y;
    var zp = pc.offset.z;
    for(var i = 0; i <  points.length; i++) {

        var x = parseFloat(points[i][xp]);
        var y = parseFloat(points[i][yp]);
        var z = parseFloat(points[i][zp]);

        if (isNaN(x) || isNaN(y) || isNaN(z)) {
            continue;
        }

        position.push(x);
        position.push(y);
        position.push(z);

        color.push(1.0, 1.0, 1.0);
    }

    var geometry = new THREE.BufferGeometry();

    if ( position.length > 0 ) geometry.addAttribute( 'position', new THREE.Float32BufferAttribute( position, 3 ) );
    if ( color.length > 0 ) geometry.addAttribute( 'color', new THREE.Float32BufferAttribute( color, 3 ) );

    // build material
    var material = new THREE.PointsMaterial( { size: 0.005  } );
    if ( color.length > 0 ) {
        material.vertexColors = THREE.VertexColors;
    } else {
        material.color.setHex( Math.random() * 0xffffff );
    }

    var mesh = new THREE.Points( geometry, material );
    mesh.name = "view-points";
    this.scene.add(mesh);

    //plot boxes
    if (pc.annotation) {
        var boxes = pc.annotation.boxes;
        for (let i = 0; i < boxes.length; i++) {
            var box = boxes[i];

            var box_geometry = new THREE.BoxGeometry(box.whl[0], box.whl[2], box.whl[1]);
            var geo = new THREE.EdgesGeometry( box_geometry ); 
            
            var type = box.type;
            var color_map = COLOR_MAP[type];
            var color = new THREE.Color(color_map[0], color_map[1], color_map[2]);
            var mat = new THREE.LineBasicMaterial( { color: color, linewidth: 1 } );
            var wireframe = new THREE.LineSegments( geo, mat );

            // material.emissive.r = 1;
            // material.emissive.g = 0;
            // material.emissive.b = 0;
            // material.opacity = 0.5;
            // material.transparent = true;
            wireframe.position.set(box.xyz_center[0], box.xyz_center[1], box.xyz_center[2]);
            wireframe.rotation.z = box.yaw;
            this.scene.add(wireframe);

            var line_geo = new THREE.Geometry();
            line_geo.vertices.push(new THREE.Vector3(0, box.whl[2]/2.0, 0));
            line_geo.vertices.push(new THREE.Vector3(0, box.whl[2]/2.0 + 1.0, 0));
            
            var line_mat = new THREE.LineBasicMaterial( { color: new THREE.Color(1.0, 1.0, 0.0), linewidth: 1.5 } );
            var line = new THREE.Line(line_geo, line_mat);
            line.position.set(box.xyz_center[0], box.xyz_center[1], box.xyz_center[2]);
            line.rotation.z = box.yaw;
            this.scene.add(line);
        }
    }

    //渲染场景
    this.renderer.render(this.scene, this.camera);

    // stats = new Stats();
    // container.appendChild( stats.dom );
}

function initPCInfoTable(pc_info) {

    // clear
    document.getElementById("pctable-body").remove();
    var table_body = document.createElement("tbody");
    table_body.id = "pctable-body";
    document.getElementById("pctable").appendChild(table_body);

    var row = document.createElement("tr");

    var id_cell = document.createElement("td");
    id_cell.appendChild(document.createTextNode(pc_info.id));
    
    var seq_cell = document.createElement("td");
    seq_cell.appendChild(document.createTextNode(pc_info.sequence));

    var pcap_name_cell = document.createElement("td");
    pcap_name_cell.appendChild(document.createTextNode(pc_info.pcap_name));
    
    row.appendChild(id_cell);
    row.appendChild(pcap_name_cell);
    row.appendChild(seq_cell);
    document.getElementById("pctable-body").appendChild(row);
}

function setupViewer(points_json) {
    var viewer = new Viewer(points_json)
    
    function animate(){

        requestAnimationFrame( animate );
        viewer.controls.update();
        viewer.renderer.render( viewer.scene, viewer.camera );
        // stats.update();
    
    }

    animate()
}




