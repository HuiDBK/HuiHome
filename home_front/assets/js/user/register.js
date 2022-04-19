// 登录注册模块
const register_url = api_domain + '/api/v1/user/register'
const username_verify_url = api_domain + '/api/v1/user/username/{username}/verify'
const mobile_verify_url = api_domain + '/api/v1/user/mobile/{mobile}/verify'
const sms_code_url = api_domain + '/api/v1/user/sms_code/{mobile}'
const login_url = api_domain + '/api/v1/user/login'

let vm = new Vue({
    el: "#app",
    data: {
        // v-models
        registerForm: {
            username: '',
            mobile: '',
            sms_code: '',
            password: '',
            role: 'tenant',
        },
        loginForm: {
            account: '',
            password: '',
        },

        // 登录成功的用户信息
        user_info: {
            user_id: '',
            username: '',
            refresh: '',
            exp: ''
        },
        sms_code_tip: '获取短信验证码',

        error_mobile_msg: '',
        error_mobile_show: false,

        error_username_msg: '',
        error_username_show: false,

        error_sms_code_msg: '',
        error_sms_code_show: false,

        sms_code_btn_disable: true,
        error_password_show: false,
        sending_flag: false,   // 短信发送标记

        login_register_btn_show: true,  // 登录注册按钮显示
        user_show: false,    // 用户头像显示

        // 登录错误的信息
        error_login_msg: '',
        error_login_show: false
    },

    mounted() {
        let token = localStorage.getItem('token')
        console.log(token)
        if (token != null) {
            this.user_info = parser_jwt(token)
            // 判断token有没有过期
            let now_timestamp = Date.parse(new Date()) / 1000
            console.log(now_timestamp)
            console.log(this.user_info.exp)
            if (this.user_info.exp > now_timestamp) {
                this.login_register_btn_show = false
                this.user_show = true
            } else {
                // 已过期
                this.login_register_btn_show = true
                this.user_show = false
            }
        }
    },
    methods: {
        check_username() {
            if (this.registerForm.username.length < 3 || this.registerForm.username.length > 20) {
                // 用户名长度必须在 3-20 之间
                this.error_username_msg = '用户名长度必须在 3-20 之间'
                this.error_username_show = true
            } else {
                this.error_username_show = false
            }

            if (this.error_username_show === false) {
                // 校验用户名是否重复注册
                let _username_verify_url = username_verify_url.format({'username': this.registerForm.username})
                console.log(_username_verify_url)
                axios.get(_username_verify_url)
                    .then(response => {
                        if (response.data.data.verify_result === true) {
                            this.error_username_msg = '该用户名已注册'
                            this.error_username_show = true
                        } else {
                            this.error_username_show = false
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        },
        check_password() {
            let re = /^[0-9A-Za-z]{6,20}$/;
            if (re.test(this.registerForm.password)) {
                this.error_password_show = false;
            } else {
                this.error_password_show = true;
            }
        },
        verify_mobile() {
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.registerForm.mobile)) {
                this.error_mobile_show = false;
                this.sms_code_btn_disable = false;
                return true
            } else {
                this.error_mobile_show = true;
                this.sms_code_btn_disable = true;
                return false
            }
        },
        check_mobile() {
            let result = this.verify_mobile()
            if (result === false) {
                this.error_mobile_msg = '您输入的手机号格式不正确';
            }
            if (this.error_mobile_show === false) {
                // 校验手机号是否重复注册
                let _mobile_verify_url = mobile_verify_url.format({'mobile': this.registerForm.mobile})
                axios.get(_mobile_verify_url)
                    .then(response => {
                        console.log(response.data)
                        if (response.data.data.verify_result === true) {
                            this.error_mobile_msg = '该手机号已注册'
                            this.error_mobile_show = true
                            this.sms_code_btn_disable = true
                        } else {
                            this.error_mobile_show = false
                            this.sms_code_btn_disable = false
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        },
        check_sms_code() {
            if (this.registerForm.sms_code.length !== 6) {
                this.error_sms_code_msg = '请填写6位的短信验证码';
                this.error_sms_code_show = true;
            } else {
                this.error_sms_code_show = false;
            }
        },
        send_sms_code() {
            // 避免重复点击
            if (this.sending_flag === true) {
                return;
            }
            this.sending_flag = true;

            // 校验参数
            this.check_mobile();
            if (this.error_mobile_show === true) {
                this.sending_flag = false;
                return;
            }

            // 请求短信验证码
            let _sms_code_url = sms_code_url.format({'mobile': this.registerForm.mobile});
            axios.get(_sms_code_url)
                .then(response => {
                    if (response.data.code === 0) {
                        this.error_sms_code_show = false;
                        // 倒计时60秒
                        var num = 60;
                        var t = setInterval(() => {
                            if (num === 1) {
                                clearInterval(t);
                                this.sms_code_tip = '获取短信验证码';
                                this.sending_flag = false;
                            } else {
                                num -= 1;
                                // 展示倒计时信息
                                this.sms_code_tip = num + '秒';
                            }
                        }, 1000, 60)
                    } else {
                        if (response.data.code === 4002) {
                            // 短信验证码错误
                            this.error_sms_code_msg = response.data.message;
                            this.error_sms_code_show = true;
                        }
                        this.sending_flag = false;
                    }
                })
                .catch(error => {
                    console.log(error.response);
                    this.sending_flag = false;
                })
        },
        submitRegister() {
            this.check_username();
            this.check_mobile();
            this.check_sms_code();
            this.check_password();

            if (this.error_mobile_show === true || this.error_password_show === true || this.error_sms_code_show === true) {
                window.event.returnValue = false;
                console.log('args error')
            }
            axios.post(register_url, this.registerForm)
                .then(response => {
                    if (response.data.code === 0) {
                        // 注册成功
                        const {token, refresh_token} = response.data.data
                        localStorage.setItem('token', token)
                        localStorage.setItem('refresh_token', refresh_token)
                        this.user_info = parser_jwt(token)
                        this.login_register_btn_show = false
                        this.user_show = true
                        window.location.reload()
                    } else {
                        // 注册失败
                        console.log(response.data)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        submitLogin() {
            axios.post(login_url, this.loginForm)
                .then(response => {
                    if (response.data.code === 0) {
                        // 登录成功
                        const {token, refresh_token} = response.data.data
                        localStorage.setItem('token', token)
                        localStorage.setItem('refresh_token', refresh_token)
                        this.user_info = parser_jwt(token)
                        window.location.reload()
                    } else {
                        // 登录失败
                        console.log(response.data)
                        this.error_login_msg = response.data.message
                        this.error_login_show = true
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
    },


})