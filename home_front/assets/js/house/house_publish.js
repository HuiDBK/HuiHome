// 房源发布模块
const publish_house_url = api_domain + '/api/v1/house/publish';

let vm = new Vue({
    el: "#app",
    data: {
        // 登录成功的用户信息
        user_info: {
            user_id: '',
            username: '',
            role: '',
            refresh: '',
            exp: ''
        },

        // 发布房源表单
        publish_house_form: {
            city: null,
            district: null,
            rent_type: null,
            address: null,
            rent_money: null,
            area_range: null,
            title: null,
            index_img: null,
            house_desc: null,
            bargain_money: null,
            water_rent: null,
            electricity_rent: null,
            strata_fee: null,
            deposit_ratio: null,
            pay_ratio: null,
            bedroom_num: null,
            living_room_num: null,
            kitchen_num: null,
            toilet_num: null,
            area: null,
            contact_info: {
                real_name: null,
                mobile: null
            },
            room_num: null,
            floor: null,
            max_floor: null,
            has_elevator: null,
            build_year: null,
            direction: null,
            lighting: null,
            certificate_no: null,
            location_info: null,
        },
        user_show: true,
        login_register_btn_show: false,  // 登录注册按钮显示

        area_list: [],
        city_list: [],
        district_list: [],

        house_img_url: '',
    },
    mounted() {
        this.user_info = verify_user_token()
    },
    methods: {
        // 房源展示图上传成功后调用此方法
        handleHouseImgSuccess(res, file) {
            this.house_img_url = res.data.file_url;
            this.publish_house_form.index_img = res.data.file_key;
        },
        publish_house() {
            // 发布房源
            console.log('publish_house_form', this.publish_house_form)
            if(!this.publish_house_form.location_info && this.publish_house_form.location_info !== ''){
                let [nl, sl] = this.publish_house_form.location_info.split(',')
                this.publish_house_form.location_info.nl = nl
                this.publish_house_form.location_info.sl = sl
            }
            axios.post(publish_house_url, this.publish_house_form, {'headers': get_token_headers()})
                .then(resp => {
                    if(resp.status === 200 && resp.data.code === 0){
                        layer.msg('发布成功', {icon: 1, time: 2000})
                    }else{
                        layer.msg('发布房源失败', {icon: 2, time: 2000})
                    }
                })
                .catch(error => {
                    console.log(error)
                    layer.msg('发布房源失败', {icon: 2, time: 2000})
                })
        },
    }
});
