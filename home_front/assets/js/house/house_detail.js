// 房源详情模块
const get_user_house_collects_url = api_domain + '/api/v1/house/user_collects/{user_id}';
const cancel_user_house_collect_url = api_domain + '/api/v1/house/user_collects';
const get_house_details_url = api_domain + '/api/v1/house/houses/{house_id}';
const get_house_facilities_url = api_domain + '/api/v1/house/facilities';
const get_user_orders_url = api_domain + '/api/v1/order/orders/{user_id}';
const create_order_url = get_user_orders_url


let vm = new Vue({
    el: "#app",
    data: {
        house_id: '',
        house_detail_info: {
            house_contact_info: {
                real_name: ''
            }
        },
        // 登录成功的用户信息
        user_info: {
            user_id: '',
            username: '',
            refresh: '',
            exp: ''
        },
        user_show: false,
        city_list: ['北京', '上海', '广州', '深圳'],
        district_list: ['福田区', '南山区', '宝安区', '光明区'],

        // 用户收藏信息
        user_house_collects: [],
        user_collect_house_ids: [],

        // 房屋设施信息
        all_house_facility: [],
        house_facility_ids: [],

        // 房屋定位信息
        location_info: '',

        // 用户预订数据
        start_date: '',
        end_date: '',

        // 订单数据
        user_orders: [],
        house_order_item: {
            house_id: '',
            state: '',
            start_date: '',
            end_state: ''
        },
        order_state_enum: {
            no_pay: 'no_pay',   // 未支付
            ordered: 'ordered', // 已预订
            payed: 'payed', // 已支付
            finished: 'finished', // 已完成
            canceled: 'canceled', // 已取消
        }
    },
    created() {
        this.user_info = verify_user_token()
        let now_timestamp = Date.parse(new Date()) / 1000
        if (this.user_info.exp > now_timestamp) {
            this.user_show = true
        }
        // 用户收藏
        this.get_user_house_collect()

        // 房源设施列表
        this.get_all_house_facility()

        // 获取房源详情
        // 从url的查询参数中获取房源id 格式:?house_id=1
        let query_params = getUrlQueryParams()
        console.log(query_params)
        this.house_id = query_params.house_id
        this.get_house_detail_info(this.house_id)
    },
    mounted() {
        this.set_cur_date()
        this.slideBanner()
    },
    methods: {
        go_pay() {
            // 去支付
            window.location.href = 'order.html'
        },
        async get_user_orders() {
            let _get_user_orders_url = get_user_orders_url.format({'user_id': this.user_info.user_id})
            await axios.get(_get_user_orders_url, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        this.user_orders = resp.data.data.user_orders
                    }
                })
                .catch(error => {

                })
        },
        set_cur_date() {
            let now = new Date();
            let year = now.getFullYear();
            let month = now.getMonth() + 1;
            let date = now.getDate();
            // 年/月/日
            let today = year + '-' + month + '-' + date;
            this.start_date = today
            $('#startDate').daterangepicker({
                singleDatePicker: true,
                locale: {
                    format: "YYYY-MM-DD"
                }
            });

            $('#endDate').daterangepicker({
                singleDatePicker: true,
                locale: {
                    format: "YYYY-MM-DD"
                }
            });
        },
        create_order() {
            this.start_date = $('#startDate').val()
            this.end_date = $('#endDate').val()

            let cur_date = new Date()
            let pre_date = new Date(cur_date.getTime() - 24 * 60 * 60 * 1000)
            if (new Date(this.start_date) < pre_date) {
                // 入住时间不能小于当天
                layer.msg('入住日期不能小于当天', {icon: 2, time: 2000})
                return
            }
            if (new Date(this.end_date) < cur_date) {
                // 退租时间不能小于当天
                layer.msg('退租日期不能小于当天', {icon: 2, time: 2000})
                return
            }
            if (!this.end_date || !this.start_date) {
                layer.msg('请选择入住和退租日期', {icon: 2, time: 2000})
                return
            }
            if (new Date(this.end_date) <= new Date(this.start_date)) {
                layer.msg('退租日期必须大于入住日期', {icon: 2, time: 2000})
                return
            }
            // 用户预订（创建订单）
            let order_data = {
                house_id: this.house_detail_info.house_id,
                start_date: this.start_date,
                end_date: this.end_date,
            }
            console.log('order_data', order_data)

            let _create_order_url = create_order_url.format({'user_id': this.user_info.user_id})
            axios.post(_create_order_url, order_data, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        console.log('order_resp', resp.data.data)
                        layer.msg('预定成功, 即将到跳转到订单界面', {icon: 1, time: 2000})
                        // 跳转到用户订单列表界面
                        setTimeout(() => {
                            this.go_pay()
                        }, 2000)
                    } else if (resp.data.code === 4015) {
                        // 订单已存在
                        layer.msg('订单已存在,请不要再次预定', {icon: 2, time: 2000})
                    } else if (resp.data.code === 4018) {
                        // 未实名认证
                        layer.msg('未实名认证,请实名后再预定', {icon: 2, time: 3000})
                    } else {
                        layer.msg('预定失败', {icon: 2, time: 2000})
                    }
                })
                .catch(error => {
                    layer.msg('预定失败', {icon: 2, time: 1000})
                })
        },
        toggle_map_gallery() {
            // 控制显示地图还是图片
            $('#map').toggleClass('active');
            $('#gallery').toggleClass('active');

            // 控制按钮
            $('#map-tab').toggleClass('active');
            $('#gallery-tab').toggleClass('active');
        },
        get_house_detail_info(house_id) {
            this.get_user_orders().then(r => {
                this._get_house_details_info(house_id)
            })
        },
        _get_house_details_info(house_id) {
            // 获取房源详情
            let _get_house_details_url = get_house_details_url.format({'house_id': house_id})
            axios.get(_get_house_details_url, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        this.house_detail_info = resp.data.data
                        this.location_info = this.house_detail_info.location_info
                        let house_facility_list = this.house_detail_info.house_facility_list
                        house_facility_list.forEach(item => {
                            this.house_facility_ids.push(item.facility_id)
                        })
                        console.log('house_facility_ids', this.house_facility_ids)
                        if (this.user_orders.length > 0) {
                            let house_order_list = this.user_orders.filter(item => {
                                let result = (item.house_id === this.house_detail_info.house_id)
                                // 排除已完成的订单
                                result = result && [this.order_state_enum.finished].indexOf(item.state) === -1
                                return result
                            })
                            if (house_order_list.length > 0) {
                                this.house_order_item = house_order_list[0]
                                let update_ts = get_date_str(this.house_order_item.update_ts * 1000)
                                this.house_order_item.update_ts = update_ts
                                this.start_date = this.house_order_item.start_date
                                this.end_state = this.house_order_item.end_date
                            }
                        }
                    }

                })
                .catch(error => {
                    console.log(error)
                })
        },
        user_collect_house_detail(house_id) {
            // 房源列表用户收藏房源
            // user_collect_house(house_id)
            let json_body = {
                user_id: this.user_info.user_id,
                house_id: house_id
            }
            console.log(json_body)
            axios.post(user_house_collect_url, json_body, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        layer.msg('收藏成功', {icon: 1, time: 1000})
                        this.user_collect_house_ids.push(house_id)
                    } else {
                        layer.msg('收藏房源失败', {icon: 2, time: 1000})
                    }
                })
                .catch(error => {
                    console.log(error)
                    layer.msg('收藏房源失败', {icon: 2, time: 1000})
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
        cancel_house_collect(house_id) {
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
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        get_all_house_facility() {
            axios.get(get_house_facilities_url, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        this.all_house_facility = resp.data.data.house_facility_list
                        console.log(this.all_house_facility)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        startAuto: function () {
            if (this.autoplay == false) {
                this.autoplay = true;
            }
        },
        stopAuto: function () {
            if (this.autoplay == true) {
                this.autoplay = false;
            }
        },
        slideBanner: function () {
            //选中item的盒子
            let item_box = $('.el-carousel__container')

            item_box = item_box.prevObject[0]

            //手指起点X坐标
            var startPoint = 0;
            //手指滑动重点X坐标
            var stopPoint = 0;


            //重置坐标
            var resetPoint = function () {
                startPoint = 0;
                stopPoint = 0;
            }

            //手指按下
            item_box.addEventListener("touchstart", (e) => {
                //手指按下的时候停止自动轮播
                vm.stopAuto();
                //手指点击位置的X坐标
                startPoint = e.changedTouches[0].pageX;
            });
            //手指滑动
            item_box.addEventListener("touchmove", (e) => {
                //手指滑动后终点位置X的坐标
                stopPoint = e.changedTouches[0].pageX;
            });
            //当手指抬起的时候，判断图片滚动离左右的距离
            item_box.addEventListener("touchend", (e) => {
                console.log("1：" + startPoint);
                console.log("2：" + stopPoint);
                if (stopPoint == 0 || startPoint - stopPoint == 0) {
                    resetPoint();
                    return;
                }
                if (startPoint - stopPoint > 0) {
                    resetPoint();
                    vm.$refs.carousel.next();
                    return;
                }
                if (startPoint - stopPoint < 0) {
                    resetPoint();
                    vm.$refs.carousel.prev();
                    return;
                }
            });
        },
    }
});
