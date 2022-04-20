// 字符串格式化方法
String.prototype.format = function (args) {
    let result = this;
    if (arguments.length < 1) {
        return result;
    }
    let data = arguments;		// 如果模板参数是数组
    if (arguments.length === 1 && typeof (args) == "object") {
        //如果模板参数是对象
        data = args;
    }
    for (let key in data) {
        let value = data[key];
        if (undefined !== value) {
            result = result.replace("{" + key + "}", value);
        }
    }
    return result;
}

function parser_jwt(token) {
    // 解析jwt
    let jwt_list = token.split('.')
    let payload = jwt_list[1]
    return JSON.parse(decodeURIComponent(escape(window.atob(payload.replace(/-/g, "+").replace(/_/g, "/")))))
}


function get_token_headers(){
    // 获取带token信息的http头部信息
    return {'Authorization': 'Bearer ' + localStorage.getItem('token')}
}