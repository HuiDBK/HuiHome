// 用户个人中心模块
const user_profile_url = api_domain + '/api/v1/user/profile/{user_id}'
const user_real_name_auth_url = api_domain + '/api/v1/user/name_auth/{user_id}'
const user_pwd_change_url = api_domain + '/api/v1/user/{user_id}/pwd_change'

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
        user_pwd_change_info: {
            src_password: '',
            new_password: '',
            confirm_password: ''
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

        error_password_msg: '',
        error_password_show: false,
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
                    if (response.status === 200) {
                        this.user_profile = response.data.data
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        real_name_auth() {
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
                    if (response.status === 200) {
                        if (response.data.code === 0) {
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
        check_change_password() {
            // 修改密码校验
            if (this.user_pwd_change_info.new_password !== this.user_pwd_change_info.confirm_password) {
                this.error_password_msg = '两次密码不一致';
                this.error_password_show = true;
            } else if (this.user_pwd_change_info.new_password.length < 6 || this.user_pwd_change_info.new_password.length > 20) {
                this.error_password_msg = '请输入6-20字符的密码';
                this.error_password_show = true;
            } else {
                this.error_password_msg = ''
                this.error_password_show = false;
            }
        },
        user_change_pwd() {
            this.check_change_password()
            if (this.error_password_show === true) {
                return
            }
            let _user_pwd_change_url = user_pwd_change_url.format({'user_id': this.user_info.user_id})
            this.user_pwd_change_info.src_password = md5(this.user_pwd_change_info.src_password)
            this.user_pwd_change_info.new_password = md5(this.user_pwd_change_info.new_password)
            this.user_pwd_change_info.confirm_password = md5(this.user_pwd_change_info.confirm_password)
            axios.put(_user_pwd_change_url, this.user_pwd_change_info, {'headers': get_token_headers()})
                .then(response => {
                    if (response.status === 200) {
                        if (response.data.code === 0) {
                            const {token} = response.data.data
                            localStorage.setItem('token', token)
                            this.user_info = parser_jwt(token)
                            layer.msg('更新成功!', {icon: 1, time: 1000});
                            this.user_pwd_change_info = {}
                        } else {
                            this.error_password_msg = response.data.message;
                            this.error_password_show = true;
                        }
                    } else if (response.data.status === 401) {
                        // 未认证
                        layer.msg('401 更新失败!', {icon: 1, time: 1000});
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