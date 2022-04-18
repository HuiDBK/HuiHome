// 注册模块

const register_url = api_domain + '/api/v1/user/register'

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
        sms_code_tip: '获取短信验证码',

        sms_code_btn_disable: true,
        error_mobile_show: false,
        error_password_show: false,
        sending_flag: false,   // 短信发送标记
    },

    methods: {
        check_password() {
            let re = /^[0-9A-Za-z]{6,20}$/;
            if (re.test(this.registerForm.password)) {
                this.error_password_show = false;
            } else {
                this.error_password_show = true;
            }
        },
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;

            if (re.test(this.registerForm.mobile)) {
                this.error_mobile_show = false;
                this.sms_code_btn_disable = false;
            } else {
                this.error_mobile_msg = '您输入的手机号格式不正确';
                this.error_mobile_show = true;
                this.sms_code_btn_disable = true;
            }

            if (this.error_mobile === false) {
                // 校验手机号是否重复注册
                // let url = '/mobiles/' + this.mobile + '/count/'
                // let options = {responseType: 'json'}
                // axios.get(url, options)
                //     .then(response => {
                //         console.log(response.data)
                //
                //         if (response.data.data.count === 1) {
                //             //    手机号重复注册
                //             this.error_mobile = true
                //             this.error_mobile_msg = '手机号码重复注册'
                //         } else {
                //             this.error_mobile = false
                //         }
                //     })
                //     .catch(error => {
                //         console.log(error.response);
                //     })
            }
        },
        check_sms_code() {
            if (this.sms_code.length !== 6) {
                this.error_sms_code_message = '请填写短信验证码';
                this.error_sms_code = true;
            } else {
                this.error_sms_code = false;
            }
        },
        send_sms_code() {
            // 避免重复点击
            alert(this.sending_flag)
            if (this.sending_flag === true) {
                return;
            }
            this.sending_flag = true;

            // 校验参数
            // this.check_mobile();
            // this.check_image_code();
            if (this.error_mobile_show === true) {
                this.sending_flag = false;
                return;
            }

            // 倒计时60秒
            let num = 60;
            let t = setInterval(() => {
                if (num === 1) {
                    clearInterval(t);
                    this.sms_code_tip = '获取短信验证码';
                    this.sending_flag = false;
                } else {
                    num -= 1;
                    // 展示倒计时信息
                    this.sms_code_tip = num + 's';
                }
            }, 1000, 60)

            // 请求短信验证码
            let url = '/sms_codes/' + this.mobile + '/?image_code=' + this.image_code + '&uuid=' + this.uuid;
            let options = {responseType: 'json'}
            axios.get(url, options)
                .then(response => {
                    if (response.data.code === 0) {
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
                        if (response.data.code === 4001) {
                            this.error_image_code_msg = response.data.errmsg;
                            this.error_image_code = true;
                        } else { // 4002
                            this.error_sms_code_message = response.data.errmsg;
                            this.error_sms_code = true;
                        }
                        this.generate_image_code();
                        this.sending_flag = false;
                    }
                })
                .catch(error => {
                    console.log(error.response);
                    this.sending_flag = false;
                })
        },
        submitRegister() {
            if(this.error_mobile_show === true || this.error_password_show === true){
                return
            }
            axios.post(register_url, this.registerForm)
                .then(response => {
                    console.log(response)
                })
                .catch(error => {
                    console.log(error)
                })
            },
    },


})