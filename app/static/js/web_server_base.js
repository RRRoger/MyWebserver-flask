/*
一些通用的函数写在这里, 这个已经放在了base.html里面, 无须再次引用
 *@author Roger
*/


/*
这个函数先验证一下接口返回是否是成功的;
如果code不是0; 则表示接口失败;
通过报错信息可以查看具体错误信息

 *@param  {Object} result 参数说明
 *@param  {Boolean} showTip 是否提示"成功"
 *@return {Boolean} 接口成功失败标志
*/
function validate_api_result(result, showTip){
    console.log(result);
    if(result.code !== 0){
        let msg = result.msg;
        if(!msg){location.href='/';return;};
        layer.confirm(msg, {
            btn: ['确认'], //,'否'],
            time: 200000, //20s后自动关闭
        },function(index){
            console.log("这是点击确定按钮走的回调");
            layer.close(index);
        },function(){
            console.log("这是点击取消按钮走的回调");
        });
        return false
    }else if(result.code === 0){
        // 提示一下
        if(showTip){layui.layer.msg('成功',{time: 1000});};
    };
    return true
}




/**
 *  将form序列化Json对象
 * {key1:"value1",key2:"value2"}
 * @example
 * <script>
 * var formParams = $("#formId").serializeObject();
 * </script>
 * ref https://blog.csdn.net/elonspace/article/details/51831066
 */
$.prototype.serializeObject = function() {
	var a, o, h, i, e;
	a = this.serializeArray();
	o = {};
	h = o.hasOwnProperty;
	for (i = 0; i < a.length; i++) {
		e = a[i];
		if (!h.call(o, e.name)) {
			o[e.name] = e.value;
		}
	}
	return o;
};


/*
删除动作
 *@param  {Object} obj layui table 某个行的对象, 需要删除
 *@param  {string} record_id 需要删除的id
 *@param  {string} url 调用的url
*/
function delete_record(obj, record_id, url){

    layer.confirm("确认要删除吗?", {
        btn: ['确认' ,'否'],
        time: 200000, //20s后自动关闭
    },function(index){
        // 删除动作
        $.ajax({
            url: url,
            type: "post",
            data: {record_id:record_id},
            success: result => {
                if(!validate_api_result(result)){return}; // 此处先预处理一下返回值, 需要报错的要报错
                obj.del();
                layui.layer.msg('删除成功',{time: 1000});
            },
            fail: err => {
                layui.layer.msg('删除失败',{time: 1000});
            }
        });
        layer.close(index);
    },function(){
        console.log("这是点击取消按钮走的回调");
    });

};


// layui table 显示 行号
function table_index(d){return (d.LAY_INDEX)}
