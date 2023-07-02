// 房源列表模块
const house_list_url = api_domain + '/api/v1/house/houses';
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

        // 房屋查询参数
        house_query_params: {
            city: null,
            district: null,
            rent_type: null,
            address: null,
            rent_money_range: null,
            area_range: null,
        },
        user_show: false,

        area_list: [],
        city_list: [],
        district_list: [],

        // 房源列表数据
        house_list: [],
        house_total: 0,
        has_more: true,
        offset: 0,
        limit: 6,
        page_sizes: [3, 6],
        current_page_num: 1,
        total_page_num: Math.floor(this.house_total / this.limit),

        min_price: 0,
        max_price: 10000,
        min_area: 0,
        max_area: 150,

        rent_money_range: [this.min_price, this.max_price],
        area_range: [this.min_area, this.max_area],

        user_house_collects: [],
        user_collect_house_ids: []
    },
    created() {
        this.get_areas_info_of_house_list().then(resp => {
            this.area_list = resp.area_list
            this.area_list.forEach(item => {
                this.city_list = this.city_list.concat(item.city_list)
            })
            console.log('area_list', this.area_list)
            console.log('city_list', this.city_list)
        })
    },
    mounted() {
        this.user_info = verify_user_token(false)
        let {rent_type, city, rent_money_range} = getUrlQueryParams()
        console.log("rent_type", rent_type, "city", city, "rent_money_range", rent_money_range)
        if(rent_type && rent_type !== ''){
            this.house_query_params.rent_type = rent_type
        }
        if(city && city !== ''){
            city = decodeURIComponent(city)
            this.house_query_params.city = city
        }
        if (rent_money_range && rent_money_range !== '') {
            this.house_query_params.rent_money_range = rent_money_range.split(';')
        }
        let now_timestamp = Date.parse(new Date()) / 1000
        if (this.user_info.exp > now_timestamp) {
            this.user_show = true
        }
        this.set_price_area_range()
        this.get_house_list(this.current_page_num, this.house_query_params)
        this.get_user_house_collect()
    },
    methods: {
        async get_areas_info_of_house_list() {
            return await get_areas_info()
        },
        set_price_area_range() {
            // Range Slider Script
            $(".js-range-slider-price").ionRangeSlider({
                type: "double",
                min: 0,
                max: 10000,
                from: this.min_price,
                to: this.max_price,
                grid: true
            });


            // Range Slider Script
            $(".js-range-slider-area").ionRangeSlider({
                type: "double",
                min: 0,
                max: 300,
                from: this.min_area,
                to: this.max_area,
                grid: true
            });
        },
        handleSizeChange(page_size) {
            console.log(`每页 ${page_size} 条`);
            this.limit = page_size
            this.get_house_list(this.current_page_num, this.house_query_params)
        },
        handleCurrentChange(page_num) {
            console.log(`当前页: ${page_num}`);
            this.current_page_num = page_num
            this.get_house_list(page_num, this.house_query_params)
        },
        search_houses() {
            // 范围分号分割;
            let price_range_str = $(".js-range-slider-price").val()
            let area_range_str = $(".js-range-slider-area").val()
            this.house_query_params.city = $("#city").val()
            this.house_query_params.district = $("#district").val()
            let rent_type = $("#rent_type").val();
            if (rent_type === 'all') {
                rent_type = null;
            }
            this.house_query_params.rent_type = rent_type
            this.house_query_params.rent_money_range = price_range_str.split(';');
            this.house_query_params.area_range = area_range_str.split(';');
            console.log('house_query_params', this.house_query_params)
            this.get_house_list(1, this.house_query_params)

        },
        city_change(){
            try {
                this.city_list.forEach(item => {
                    if(item.name === this.house_query_params.city){
                        this.district_list = item.district_list
                        throw new Error('exit for loop')
                    }
                })
            }  catch (e){
                console.log('exit for loop')
            }
        },
        get_house_list(page_num, query_params = {}) {
            console.log(page_num)
            this.page_num = page_num
            // 获取房源列表
            let json_body = {
                offset: (this.page_num - 1) * this.limit,
                limit: this.limit,
                query_params: query_params
            }
            axios.post(house_list_url, json_body, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        this.house_list = resp.data.data.data_list;
                        this.house_total = resp.data.data.total;
                        this.has_more = resp.data.data.has_more;
                        if (this.house_total % this.limit === 0) {
                            this.total_page_num = this.house_total / this.limit
                        } else {
                            this.total_page_num = Math.floor(this.house_total / this.limit) + 1
                        }
                        console.log(this.total_page_num)
                        console.log(this.house_list)
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
    }
});
