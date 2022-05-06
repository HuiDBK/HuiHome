// 用户中心租房需求管理
const publish_rental_demand_url = api_domain + '/api/v1/user/rental_demands/{user_id}';
const get_rental_demands_url = api_domain + '/api/v1/user/rental_demands';
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
            rent_type_list: [],
            house_type_list: [],
            traffic_info: [],
            house_facilities: [],
            min_money_budget: 500,
            max_money_budget: 5000,
        },
        rental_demand_form_copy: {},
        rental_demand_show: false,

        op_status: 1, // 发布求租表单的操作状态 1 => 发布   2 => 编辑

        // 省市区数据
        area_index: '',
        area_list: [],
        city_list: [],

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
        this.get_areas_info_of_demand().then(resp => {
            this.area_list = resp.area_list
            console.log('area_list', this.area_list)
        })
    },
    mounted() {
        this.user_info = verify_user_token()
        this.get_rental_demand_list(1)
        this.get_all_house_facility()
    },
    methods: {
        show_publish_rental_demand_dialog() {
            this.area_index = ''
            this.rental_demand_form = this.rental_demand_form_copy
            this.rental_demand_show = true
            this.op_status = 1
        },
        edit_save_demand() {
            // 编辑保存租房需求
            this._publish_or_edit_rental_demand('put')
        },
        edit_rental_demand(index) {
            this.rental_demand_form = this.rental_demand_list[index]
            console.log('rental_demand_form', this.rental_demand_form)
            this.rental_demand_form.floor_list = []
            this.rental_demand_form.floors.sort((a, b) => {
                return a - b
            })
            this.rental_demand_form.floors.forEach(item => {
                this.rental_demand_form.floor_list.push({value: item})
            })

            // 获取期望城市的省份
            let province_index = ''
            try {
                this.area_list.forEach((item, index) => {
                        item.city_list.forEach(city_item => {
                            if (city_item.name === this.rental_demand_form.city) {
                                province_index = index
                                throw new Error('interrupt')
                            }
                        })
                    }
                )
            } catch (e) {
                console.log(e)
            }
            this.area_index = province_index
            this.rental_demand_show = true
            this.op_status = 2
        },
        delete_rental_demand(rental_demand_id) {

        },
        get_rental_demand_list(page_num) {
            // 获取租房需求列表
            this.current_page_num = page_num
            let json_body = {
                limit: this.limit,
                offset: (this.current_page_num - 1) * this.limit,
                query_params: {
                    user_id: this.user_info.user_id
                }
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
        get_city_list() {
            console.log('area_index', this.area_index)
            if (this.area_index === '' || this.area_index === null) {
                return
            }
            let area_item = this.area_list[this.area_index]
            this.city_list = area_item.city_list
        },
        async get_areas_info_of_demand() {
            return await get_areas_info()
        },
        remove_floor(item) {
            let index = this.rental_demand_form.floor_list.indexOf(item)
            if (index !== -1) {
                this.rental_demand_form.floor_list.splice(index, 1)
            }
        },
        add_floor() {
            this.rental_demand_form.floor_list.push({
                value: '',
                key: Date.now()
            });
        },
        publish_rental_demand() {
            // 发布租房需求
            this._publish_or_edit_rental_demand('post')
        },
        _publish_or_edit_rental_demand(method = 'post') {
            console.log('rental_demand_form', this.rental_demand_form)
            if (this.rental_demand_form.lighting !== null) {
                this.rental_demand_form.lighting = Number(this.rental_demand_form.lighting)
            }

            if (this.rental_demand_form.elevator !== null) {
                this.rental_demand_form.elevator = Number(this.rental_demand_form.elevator)
            }

            this.rental_demand_form.floor_list.forEach(item => {
                if (item.value !== '') {
                    this.rental_demand_form.floors.push(item.value)
                }
            })
            let _publish_rental_demand_url = publish_rental_demand_url.format({'user_id': this.user_info.user_id})
            if (method === 'post') {
                axios.post(_publish_rental_demand_url, this.rental_demand_form, {'headers': get_token_headers()})
                    .then(resp => {
                        if (resp.status === 200 && resp.data.code === 0) {
                            layer.msg('发布成功', {icon: 1, time: 2000})
                            this.get_rental_demand_list(1)
                            this.rental_demand_show = false
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
            } else if (method === 'put') {
                // 更新用户租房需求
                axios.put(_publish_rental_demand_url, this.rental_demand_form, {'headers': get_token_headers()})
                    .then(resp => {
                        if (resp.status === 200 && resp.data.code === 0) {
                            layer.msg('更新成功', {icon: 1, time: 2000})
                            this.get_rental_demand_list(1)
                            this.rental_demand_show = false
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
            this.rental_demand_form.floors = []
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
        }
        ,
    }
})