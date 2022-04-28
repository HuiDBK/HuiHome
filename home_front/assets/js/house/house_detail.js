// 房源详情模块
const get_user_house_collects_url = api_domain + '/api/v1/house/user_collects/{user_id}';
const cancel_user_house_collect_url = api_domain + '/api/v1/house/user_collects';
const get_house_details_url = api_domain + '/api/v1/house/houses/{house_id}';
const get_house_facilities_url = api_domain + '/api/v1/house/facilities';

let vm = new Vue({
    el: "#app",
    data: {
        house_id: '',
        house_detail_info: '',
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

        user_house_collects: [],
        user_collect_house_ids: [],
        all_house_facility: [],
        house_facility_ids: [],
        location_info: '',
    },
    mounted() {
        this.user_info = verify_user_token()
        let now_timestamp = Date.parse(new Date()) / 1000
        if (this.user_info.exp > now_timestamp) {
            this.user_show = true
        }
        // this.get_user_house_collect()
        // 从url的查询参数中获取房源id 格式:?house_id=1
        let query_params = getUrlQueryParams()
        console.log(query_params)
        this.house_id = query_params.house_id
        this.get_house_detail_info(this.house_id)
        this.get_all_house_facility()
        this.slideBanner()
    },
    methods: {
        toggle_map_gallery() {
            // 控制显示地图还是图片
            $('#map').toggleClass('active');
            $('#gallery').toggleClass('active');

            // 控制按钮
            $('#map-tab').toggleClass('active');
            $('#gallery-tab').toggleClass('active');
        },
        get_house_detail_info(house_id) {
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
                        console.log(this.house_facility_ids)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        user_collect_house_list(house_id) {
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
        }
    }
});