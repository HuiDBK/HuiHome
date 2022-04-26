// 用户个人中心模块
const house_list_url = api_domain + '/api/v1/house/houses';

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
        city_list: ['北京', '上海', '广州', '深圳'],
        district_list: ['福田区', '南山区', '宝安区', '光明区'],

        // 房源列表数据
        house_list: null,
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
    },
    mounted() {
        this.user_info = verify_user_token()
        let now_timestamp = Date.parse(new Date()) / 1000
        if (this.user_info.exp > now_timestamp) {
            this.user_show = true
        }
        this.set_price_area_range()
        this.get_house_list(this.current_page_num)
    },
    methods: {
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
            this.get_house_list(this.current_page_num)
        },
        handleCurrentChange(page_num) {
            console.log(`当前页: ${page_num}`);
            this.current_page_num = page_num
            this.get_house_list(page_num)
        },
        search_houses() {
            // 范围分号分割;
            let price_range_str = $(".js-range-slider-price").val()
            let area_range_str = $(".js-range-slider-area").val()
            this.house_query_params.city = $("#city").val()
            this.house_query_params.district = $("#district").val()
            let rent_type = $("#rent_type").val();
            if(rent_type === 'all'){
               rent_type = null;
            }else {
                rent_type = [rent_type]
            }
            this.house_query_params.rent_type = rent_type
            this.house_query_params.rent_money_range = price_range_str.split(';');
            this.house_query_params.area_range = area_range_str.split(';');
            console.log(this.house_query_params)
            this.get_house_list(1, this.house_query_params)

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
        }
    }
});