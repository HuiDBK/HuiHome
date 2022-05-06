// 所有租房需求详情
const get_rental_demands_url = api_domain + '/api/v1/user/rental_demands';
const get_house_facilities_url = api_domain + '/api/v1/house/facilities';

let vm = new Vue({
    el: "#app",
    data: {
        // 登录成功的用户信息
        user_info: {
            user_id: '',
            role: '',
            username: '',
            refresh: '',
            exp: ''
        },
        user_show: true,

        // 租房需求表单信息
        rental_demand_form: {
            demand_title: '',
            extend_content: null,
            lighting: null,
            elevator: null,
            floor_list: [
                {value: ''},
            ],
            floors: [],
            city: null,
            desired_residence_area: null,
            rent_type_list: [],
            house_type_list: [],
            traffic_info: [],
            company_address: null,
            commuting_time: null,
            house_facilities: [],
            min_money_budget: 500,
            max_money_budget: 5000,
            user_info: {},
        },
        rental_demand_form_copy: {},
        rental_demand_show: false,

        op_status: 1, // 发布求租表单的操作状态 1 => 发布   2 => 编辑

        // 房屋设施
        all_house_facility: [],

        // 分页数据
        rental_demand_list: [],
        rental_demand_total: 0,
        current_page_num: 1,
        offset: 0,
        limit: 6,
        page_sizes: [3, 6],
    },
    created() {
        this.rental_demand_form_copy = this.rental_demand_form
    },
    mounted() {
        this.user_info = verify_user_token()
        this.get_rental_demand_list(1)
    },
    methods: {
        get_rental_demand_list(page_num) {
            // 获取租房需求列表
            this.current_page_num = page_num
            let json_body = {
                limit: this.limit,
                offset: (this.current_page_num - 1) * this.limit
            }
            axios.post(get_rental_demands_url, json_body, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        this.rental_demand_list = resp.data.data.data_list
                        this.rental_demand_list.forEach(item => {
                            item.create_ts = get_date_str(item.create_ts * 1000, true)
                        })
                        this.rental_demand_total = resp.data.data.total
                        console.log('rental_demands', this.rental_demand_list)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
    }
})