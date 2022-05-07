// 用户个人中心模块
const user_profile_url = api_domain + '/api/v1/user/profile/{user_id}'
const user_real_name_auth_url = api_domain + '/api/v1/user/name_auth'
const user_pwd_change_url = api_domain + '/api/v1/user/{user_id}/pwd_change'
const get_user_house_collects_url = api_domain + '/api/v1/house/user_collects/{user_id}';
const cancel_user_house_collect_url = api_domain + '/api/v1/house/user_collects';

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
        user_show: true,

        // 用户收藏的房源
        user_house_collects: [],
        user_collect_house_ids: [],
    },
    mounted() {
        this.user_info = verify_user_token()
        this.get_user_profile()
        this.get_user_house_collect()
    },
    methods: {
        update_id_card_img(img_file) {
            let upload_item = img_file.target.name
            let id_card_file = img_file.target.files[0]
            console.log(id_card_file.name)
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
        async real_name_auth() {
            // 先上传实名认证的图片
            let files = [this.user_profile.id_card_front, this.user_profile.id_card_back]
            await upload_file(files).then(data => {
                console.log(data)
                data.file_list.forEach(file_item => {
                    console.log(file_item.file_name)
                    if (this.user_profile.id_card_front.name === this.user_profile.id_card_front.name) {
                        // 上传了同一张图片
                        this.user_profile.id_card_front = file_item.file_url
                        this.user_profile.id_card_back = file_item.file_url
                    } else if (file_item.file_name === this.user_profile.id_card_front.name) {
                        this.user_profile.id_card_front = file_item.file_url
                    } else {
                        this.user_profile.id_card_back = file_item.file_url
                    }
                })
            })

            // 实名认证信息
            let user_name_auth_data = {
                user_id: this.user_info.user_id,
                real_name: this.user_profile.real_name,
                id_card: this.user_profile.id_card,
                id_card_front: this.user_profile.id_card_front,
                id_card_back: this.user_profile.id_card_back
            }
            console.log(user_name_auth_data)
            axios.post(user_real_name_auth_url, user_name_auth_data, {'headers': get_token_headers()})
                .then(response => {
                    if (response.status === 200) {
                        if (response.data.code === 0) {
                            // this.user_profile = response.data.data
                            layer.msg('实名认证已提交，待审核', {icon: 1, time: 2000})
                        }
                    } else if (response.data.status === 401) {
                        // 未认证
                    }
                })
                .catch(error => {
                    console.log(error)
                    layer.msg('实名认证提交失败', {icon: 2, time: 2000})
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
        },
        get_user_house_collect() {
            let _get_user_house_collects_url = get_user_house_collects_url.format({'user_id': this.user_info.user_id})
            axios.get(_get_user_house_collects_url, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        this.user_house_collects = resp.data.data.user_house_collects;
                        this.user_house_collects.forEach(item => {
                            this.user_collect_house_ids.push(item.house_id)
                        })
                        console.log(this.user_collect_house_ids)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        _cancel_house_collect(house_id) {
            let json_body = {
                user_id: this.user_info.user_id,
                house_id: house_id
            }
            let config = {
                data: json_body,
                headers: get_token_headers()
            }
            axios.delete(cancel_user_house_collect_url, config)
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        console.log(resp.data.data)
                        // 取消房源收藏
                        this.user_collect_house_ids = this.user_collect_house_ids.filter(item => {
                            return item !== house_id
                        })
                        this.user_house_collects = this.user_house_collects.filter(item => {
                            return item.house_id !== house_id
                        })
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        cancel_house_collect(house_id) {
            layer.open({
                icon: 0,
                title: '取消收藏',
                content: '确认取消收藏？',
                btn: ['确定', '取消'],
                yes: (index) => {
                    this._cancel_house_collect(house_id)
                    layer.close(index)
                },
                btn2: (index) => {

                }
            })
        },
    }
})
