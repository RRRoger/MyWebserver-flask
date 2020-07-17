/**
  * 增删改查的逻辑
  *
  * @version v1.0.1
  * @author Roger Chen
  */


// 添加model
$("#model_add").click(function(event){
    let new_name = $("#new_model_name").val();

    if(!new_name){
        alert("请输入名称!");
    }

    $.ajax({
        url:"/model/add",
        type:"post",
        dataType:"json",
        data: {
            name: new_name
        },
        success:function(data){
            //成功后执行的动作
            console.log(data);
            if(data.code==0){
                //true
                alert("成功");
            }else{
                alert(data.msg);
            }
        },
    })
})