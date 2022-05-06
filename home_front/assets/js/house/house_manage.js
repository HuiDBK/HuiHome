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
            role: '',
            refresh: '',
            exp: ''
        },

        // 房屋查询参数
        house_query_params: {
            house_owner: null,
            city: null,
            district: null,
            state: null,
            rent_type: null,
            address: null,
            rent_money_range: null,
            area_range: null,
        },
        user_show: true,
        login_register_btn_show: false,  // 登录注册按钮显示

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

        user_house_collects: [],
        user_collect_house_ids: []
    },
    mounted() {
        this.user_info = verify_user_token()
        this.house_query_params.house_owner = this.user_info.user_id
        this.get_house_list(this.current_page_num, this.house_query_params)
    },
    methods: {
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
            console.log('house_query_params', this.house_query_params)
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
