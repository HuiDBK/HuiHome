// 订单模块
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

        user_orders: [],
        order_state_enum: {
            no_pay: 'no_pay',   // 未支付
            ordered: 'ordered', // 已预订
            payed: 'payed', // 已支付
            finished: 'finished', // 已完成
            canceled: 'canceled', // 已取消
        },

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
        this.get_user_orders()
    },
    methods: {
        get_user_orders() {
            let _get_user_orders_url = get_user_orders_url.format({'user_id': this.user_info.user_id})
            axios.get(_get_user_orders_url, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        this.user_orders = resp.data.data.user_orders
                        this.user_order_list = this.user_orders
                        this.order_total = this.user_orders.length
                        this.get_order_list(1, this.user_order_list)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        get_order_list(page_num, order_list){
            let offset = (page_num - 1) * this.limit
            this.user_orders = (offset + this.limit >= order_list.length) ? order_list.splice(offset, order_list.length) : order_list.splice(offset, this.limit)
            this.current_page_num = page_num
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
    },


})