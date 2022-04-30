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
        user_show: true,

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

        // 订单详情
        order_detail_show: false,
        order_detail_item: '',

        // 租赁日期范围
        rental_date_range: ''

    },
    mounted() {
        this.user_info = verify_user_token()
        this.get_user_orders()
    },
    methods: {
        pay_order(order_id) {
            // 支付订单
            alert(this.rental_date_range)
            console.log('rental_date_range', this.rental_date_range)
            this.order_detail_show = false
        },
        pre_pay_order(order_id) {
            // 支付房源定金
            alert(this.rental_date_range)

            this.order_detail_show = false
        },
        show_order_detail(order_index) {
            // 查看订单详情
            const order_item = this.user_orders[order_index]
            console.log('order_item', order_item)
            this.order_detail_item = order_item
            this.rental_date_range = [this.order_detail_item.start_date, this.order_detail_item.end_date]
            this.order_detail_show = true
        },
        print_contract() {
            let before = "<html><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'></head><body >";
            let print = $('#contract_content').html();
            let result = before + print + "</body></html>"

            console.log(result);
            var wind = window.open("", 'newwindow', 'height=300, width=700, top=100, left=100, toolbar=no, menubar=no, scrollbars=no, resizable=no,location=no, status=no');

            wind.document.body.innerHTML = result;

            wind.print();
            return false;
        },
        order_list_back() {
            // 返回订单列表
            $('#contract_box').hide()

            // 让用户中心
            $('#user_center').show()
        },
        show_contract(contract_content) {
            // 展示订单的合同信息

            if (!contract_content) {
                layer.msg('暂无相关合同信息，抱歉')
                return
            }
            // 填充合同信息, 先请空再填充
            let contract_container = $('#contract_content')
            contract_container.empty()
            contract_container.append(contract_content)
            $('#contract_box').show()

            // 让用户中心隐藏
            $('#user_center').hide()

        },
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
        get_order_list(page_num, order_list) {
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