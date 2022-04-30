const get_order_detail_url = api_domain + '/api/v1/order/orders/{order_id}';

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
        let {order_id} = getUrlQueryParams()
        this.get_order_by_id(order_id)
    },
    methods: {
        get_order_by_id(order_id){
            let _get_order_detail_url = get_order_detail_url.format({'order_id': order_id})
            axios.get(_get_order_detail_url, {'headers': get_token_headers()})
                .then(resp => {
                    if(resp.status === 200 && resp.data.code === 0){

                    }
                })
                .catch(error => {

                })
        },
        show_contract(order_id) {
            // 查看合同信息
            window.location.href = 'contract.html?order_id=' + order_id
        },
    }
})