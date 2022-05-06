// 租房需求详情
const get_rental_demand_url = api_domain + '/api/v1/user/rental_demands/{demand_id}';
const get_house_facilities_url = api_domain + '/api/v1/house/facilities';

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

        activeNames: ['1'],

        // 房屋设施
        all_house_facility: [],

        demand_id: null,

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
        let {demand_id} = getUrlQueryParams()
        this.demand_id = demand_id
    },
    mounted() {
        this.user_info = verify_user_token()
        this.get_all_house_facility()
        this.get_rental_demand_detail(this.demand_id)
    },
    methods: {
        get_rental_demand_detail(demand_id) {
            // 获取租房需求详情
            let _get_rental_demand_url = get_rental_demand_url.format({'demand_id': demand_id})
            axios.get(_get_rental_demand_url, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        this.rental_demand_form = resp.data.data
                        this.rental_demand_form.floors.sort((a, b) => {
                            return a - b
                        })
                        this.rental_demand_form.house_facilities = this.all_house_facility.filter(item => {
                            return this.rental_demand_form.house_facilities.indexOf(item.facility_id) !== -1
                        })
                        this.rental_demand_form.create_ts = get_date_str(this.rental_demand_form.create_ts * 1000, true)
                        console.log('rental_demand_form', this.rental_demand_form)
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
    }
})