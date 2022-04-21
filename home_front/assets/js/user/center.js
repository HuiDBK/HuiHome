// 用户个人中心模块
const user_profile_url = api_domain + '/api/v1/user/profile/{user_id}'
const user_real_name_auth_url = api_domain + '/api/v1/user/name_auth/{user_id}'

let vm = new Vue({
    el: "#app",
    data: {
        // 登录成功的用户信息
        user_info: {
            user_id: '',
            username: '',
            refresh: '',
            exp: ''
        },

        // 用户详情信息
        user_profile: {
            auth_status: '',
            avatar: '',
            career: '',
            create_ts: null,
            gender: '',
            hobby: '',
            id_card: '',
            id_card_back: '',
            id_card_front: '',
            mail: '',
            mobile: '',
            real_name: '',
            role: '',
            state: '',
            user_id: '',
            username: ''
        },

        // 用户真实密码
        real_password: '',

        error_mobile_msg: '',
        error_mobile_show: false,
    },

    mounted() {
        let token = localStorage.getItem('token')
        if (token != null) {
            this.user_info = parser_jwt(token)
            // 判断token有没有过期
            let now_timestamp = Date.parse(new Date()) / 1000
            console.log(now_timestamp)
            console.log(this.user_info.exp)
            if (this.user_info.exp < now_timestamp) {
                // token已过期
                alert('登录状态已失效，请重新登录')
                window.location.href = '/house_rental/home_front/index.html'
            }
        } else {
            window.location.href = '/house_rental/home_front/index.html'
        }
        this.get_user_profile()
    },
    methods: {
        update_id_card_img(img_file) {
            let upload_item = img_file.target.name
            let id_card_file = img_file.target.files[0]
            if (upload_item === 'id_card_front') {
                this.user_profile.id_card_front = id_card_file
            } else if (upload_item === 'id_card_back') {
                this.user_profile.id_card_back = id_card_file
            }
            let reader = new FileReader();
            reader.readAsDataURL(id_card_file);
            reader.onload = (e) => {
                let id_card_element = document.getElementById(upload_item)
                id_card_element.setAttribute('src', e.target.result)
            }
        },
        get_user_profile() {
            // 获取用户详情信息
            let _user_profile_url = user_profile_url.format({'user_id': this.user_info.user_id})
            let token_headers = get_token_headers()
            console.log(token_headers)
            axios.get(_user_profile_url, {'headers': token_headers})
                .then(response => {
                    console.log(response.data.data)
                    this.user_profile = response.data.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
        real_name_auth(){
            // 实名认证
            let _user_real_name_auth_url = user_real_name_auth_url.format({'user_id': this.user_info.user_id})
            let user_name_auth_data = {
                user_id: this.user_info.user_id,
                real_name: this.user_profile.real_name,
                id_card: this.user_profile.id_card,
                id_card_front: this.user_profile.id_card_front,
                id_card_back: this.user_profile.id_card_back
            }

            // 需要上传实名认证图片,因此改用form表单格式
            let user_name_auth_form_data = paramsToFormData(user_name_auth_data)
            let config = {
                'headers': get_token_headers(),
                'Content-Type': 'multipart/form-data'
            }
            axios.post(_user_real_name_auth_url, user_name_auth_form_data, config)
                .then(response => {
                    if (response.data.status === 200) {
                        if (response.data.data.code === 0) {
                            // this.user_profile = response.data.data
                        }
                    } else if (response.data.status === 401) {
                        // 未认证
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        submitProfile() {
            // 更新用户信息
            console.log(this.user_profile)
            let _user_profile_url = user_profile_url.format({'user_id': this.user_info.user_id})
            let config = {
                'headers': get_token_headers(),
            }
            axios.put(_user_profile_url, this.user_profile, config)
                .then(response => {
                    if (response.data.status === 200) {
                        if (response.data.data.code === 0) {
                            this.user_profile = response.data.data
                        }
                    } else if (response.data.status === 401) {
                        // 未认证
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
})