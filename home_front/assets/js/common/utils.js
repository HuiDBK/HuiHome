// 工具类模块
let refresh_token_url = api_domain + '/api/v1/auth/refresh'
let upload_file_url = api_domain + '/api/v1/common/upload/'
let batch_upload_file_url = api_domain + '/api/v1/common/upload/batch'
let user_house_collect_url = api_domain + '/api/v1/house/user_collects'
let get_areas_info_url = api_domain + '/api/v1/common/areas'

// 响应拦截器
axios.interceptors.response.use(
  (response) => {
    // 对响应数据做一些处理
    return response;
  },
  (error) => {
    // 在响应错误时做一些处理
    if (error.response && error.response.status === 401) {
      // 捕获到 401 未登录状态码
      // 执行你想要的操作，比如跳转到登录页面
      window.location.href = 'index.html';
    }
    return Promise.reject(error);
  }
);

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
            if (response.data.status === 200) {
                localStorage.setItem('token', response.data.data.token)
            } else if (response.data.status === 401) {
                // refresh_token 已失效重定向到首页
            }
        })
        .catch(error => {
            console.log(error)
        })
}

function paramsToFormData(obj) {
    // js对象转FormData
    const formData = new FormData();
    Object.keys(obj).forEach((key) => {
        if (obj[key] instanceof Array) {
            obj[key].forEach((item) => {
                formData.append(key, item);
            });
            return;
        }
        formData.append(key, obj[key]);
    });
    return formData;
}


function user_logout() {
    // 用户退出登录
    localStorage.clear()
    window.location.href = './index.html'

}

async function upload_file(file) {
    // 文件上传
    let upload_form_data, upload_url;
    if (file instanceof Array) {
        // 批量上传
        upload_form_data = paramsToFormData({'files': file});
        upload_url = batch_upload_file_url
    } else {
        // 单文件上传
        upload_form_data = paramsToFormData({'file': file});
        upload_url = upload_file_url
    }
    let config = {
        'headers': get_token_headers(),
        'Content-Type': 'multipart/form-data'
    }
    return new Promise((resolve, reject) => {
        axios.post(upload_url, upload_form_data, config)
            .then(response => {
                if (response.status === 200 && response.data.code === 0) {
                    resolve(response.data.data);
                    return response.data.data;
                }
            })
            .catch(error => {
                reject(error.data)
                console.log(error)
            })
    });
}

function verify_user_token(is_redirect = true) {
    // 校验token, is_redirect: 没有token和token是否重定向
    let token = localStorage.getItem('token')
    let user_info = {}
    if (token != null) {
        user_info = parser_jwt(token)
        // 判断token有没有过期
        let now_timestamp = Date.parse(new Date()) / 1000
        console.log(now_timestamp)
        console.log(user_info.exp)
        if (user_info.exp < now_timestamp && is_redirect) {
            // token已过期
            layer.msg('登录状态已失效，请重新登录', {icon: 0, time: 2000})
            setTimeout((e) => {
                window.location.href = 'index.html'
            }, 2000)

        }
    } else if (is_redirect) {
        window.location.href = 'index.html'
    }
    return user_info
}

function user_collect_house(house_id) {
    // 用户收藏房源
    let user_info = verify_user_token()
    let json_body = {
        user_id: user_info.user_id,
        house_id: house_id
    }
    console.log(json_body)
    axios.post(user_house_collect_url, json_body, {'headers': get_token_headers()})
        .then(resp => {
            if (resp.status === 200 && resp.data.code === 0) {
                layer.msg('收藏成功', {icon: 1, time: 1000})
            } else {
                layer.msg('收藏房源失败', {icon: 2, time: 1000})
            }
        })
        .catch(error => {
            console.log(error)
            layer.msg('收藏房源失败', {icon: 2, time: 1000})
        })
}

/**
 * 获取当前 URL 所有 GET 查询参数
 * 入参：要解析的 URL，不传则默认为当前 URL
 * 返回：一个<key, value>参数对象
 */
function getUrlQueryParams(url = location.search) {
    const params = {};
    const keys = url.match(/([^?&]+)(?==)/g);
    const values = url.match(/(?<==)([^&]*)/g);
    for (const index in keys) {
        params[keys[index]] = values[index];
    }
    return params;
}

function formatDate(time,format='YY-MM-DD hh:mm:ss'){
	let date = new Date(time);

	let year = date.getFullYear(),
		month = date.getMonth()+1,//月份是从0开始的
		day = date.getDate(),
		hour = date.getHours(),
		min = date.getMinutes(),
		sec = date.getSeconds();
	let preArr = Array.apply(null,Array(10)).map(function(elem, index) {
		return '0'+index;
	});

	let newTime = format.replace(/YY/g,year)
						.replace(/MM/g,preArr[month]||month)
						.replace(/DD/g,preArr[day]||day)
						.replace(/hh/g,preArr[hour]||hour)
						.replace(/mm/g,preArr[min]||min)
						.replace(/ss/g,preArr[sec]||sec);

	return newTime;
}


function get_date_str(ts, need_time = false) {
    // 根据时间戳获取时间str 参数时间戳单位是毫秒
    let parse_date = new Date(ts)
    let year = parse_date.getFullYear();
    let month = parse_date.getMonth() + 1;
    let date = parse_date.getDate();
    let hour = parse_date.getHours();
    let min = parse_date.getMinutes();
    let sec = parse_date.getSeconds();

    // 年-月-日
    let date_str = year + '-' + month + '-' + date;
    if(need_time){
        date_str = formatDate(ts)
    }
    return date_str
}


async function get_areas_info() {
    // 获取省市区数据
    return new Promise((resolve, reject) => {
        axios.get(get_areas_info_url, {'headers': get_token_headers()})
            .then(response => {
                if (response.status === 200 && response.data.code === 0) {
                    resolve(response.data.data);
                    return response.data.data;
                }
            })
            .catch(error => {
                reject(error.data)
                console.log(error)
            })
    });
}
