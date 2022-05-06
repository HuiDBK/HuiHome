// 用户中心我的家
const get_user_orders_url = api_domain + '/api/v1/order/orders/{user_id}';

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

        user_orders: [],

        // 订单状态枚举信息
        order_state_enum: {
            no_pay: 'no_pay',   // 未支付
            ordered: 'ordered', // 已预订
            payed: 'payed', // 已支付
            finished: 'finished', // 已完成
            canceled: 'canceled', // 已取消
        },
        order_state_list: [
            {key: 'all', label: '全部'},
            {key: 'no_pay', label: '未支付'},
            {key: 'ordered', label: '已预订'},
            {key: 'payed', label: '已支付'},
            {key: 'finished', label: '已完成'},
            {key: 'canceled', label: '已取消'}],

        order_search_state: '',

        // 分页数据
        user_order_list: [],
        order_total: 0,
        current_page_num: 1,
        offset: 0,
        limit: 6,
        page_sizes: [3, 6],
    },
    mounted() {
        this.user_info = verify_user_token()
        this.get_my_home()
    },
    methods: {
        get_order_list(page_num, order_list) {
            let temp_orders = [...order_list]   // 复制数组避免splice删除已有的数据
            let offset = (page_num - 1) * this.limit
            console.log(this.user_order_list)
            this.user_orders = (offset + this.limit >= temp_orders.length) ? temp_orders.splice(offset, temp_orders.length) : temp_orders.splice(offset, this.limit)
            this.current_page_num = page_num
            console.log(this.user_order_list)
        },
        handleSizeChange(page_size) {
            console.log(`每页 ${page_size} 条`);
            this.limit = page_size
            this.get_order_list(this.current_page_num, this.user_order_list)
        },
        handleCurrentChange(page_num) {
            console.log(`当前页: ${page_num}`);
            this.current_page_num = page_num
            this.get_order_list(page_num, this.user_order_list)
        },
        get_my_home() {
            let _get_user_orders_url = get_user_orders_url.format({'user_id': this.user_info.user_id})
            axios.get(_get_user_orders_url, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        this.user_orders = resp.data.data.user_orders
                        // 格式化时间
                        this.user_orders.forEach(item => {
                            item.update_ts = get_date_str(item.update_ts * 1000)
                        })
                        this.user_order_list = this.user_orders

                        // 过滤出我的家
                        this.user_order_list = this.user_order_list.filter(item => {
                            return item.state === this.order_state_enum.payed || item.state === this.order_state_enum.finished
                        })
                        console.log('my_home_list', this.user_order_list)
                        this.order_total = this.user_order_list.length
                        this.get_order_list(1, this.user_order_list)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
    }
})