// 工具类模块
refresh_token_url = api_domain + '/api/v1/auth/refresh'

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


function get_token_headers(is_refresh_token = false) {
    // 获取带token信息的http头部信息
    if (is_refresh_token === true) {
        return {'Authorization': 'Bearer ' + localStorage.getItem('refresh_token')}
    } else {
        return {'Authorization': 'Bearer ' + localStorage.getItem('token')}
    }

}

function refresh_token() {
    // 刷新token
    let token_headers = get_token_headers(true)
    axios.put(refresh_token_url, {headers: token_headers})
        .then(response => {
            if (response.data.status === 200){
                localStorage.setItem('token', response.data.data.token)
            }else if (response.data.status === 401){
                // refresh_token 已失效重定向到首页
            }
        })
        .catch(error => {
            console.log(error)
        })
}