// 订单模块
const get_user_orders_url = api_domain + '/api/v1/order/orders/{user_id}';
const alipay_order_url = api_domain + '/api/v1/payment/alipay/orders/{order_id}';

let vm = new Vue({
    el: "#app",
    data: {
        // 登录成功的用户信息
        user_info: {
            user_id: '',
            role:'',
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
        search_order_by_state() {
            // 通过订单的状态来搜索
            if (!this.order_search_state) {
                return
            }
            if (this.order_search_state === 'all') {
                this.get_order_list(1, this.user_order_list)
                return
            }
            let order_list = this.user_order_list.filter(item => {
                return item.state === this.order_search_state
            })
            this.get_order_list(1, order_list)
        },
        pay_order(order_id, pay_scene) {
            console.log('rental_date_range', this.rental_date_range)
            let [start_date, end_date] = this.rental_date_range
            if (!start_date || !end_date) {
                return lay.msg('请选择正确的租赁日期范围', {icon: 1, time: 2000})
            }

            let json_body = {
                pay_scene: pay_scene
            }
            // 先判断租赁日期是否有改变
            if (start_date !== this.order_detail_item.start_date || end_date !== this.order_detail_item.end_date) {
                // 有一个发送变化就要传递
                json_body.start_date = start_date
                json_body.end_date = end_date
            }
            console.log('order_pay_item', json_body)

            let _alipay_order_url = alipay_order_url.format({'order_id': order_id})
            axios.post(_alipay_order_url, json_body, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        // 请求成功, 重定向到阿里支付界面
                        let alipay_url = resp.data.data.alipay_url
                        window.location.href = alipay_url
                    } else {
                        layer.msg(resp.data.message, {icon: 2, time: 2000})
                    }
                })
                .catch(error => {
                    console.log(error)
                    layer.msg('请求失败', {icon: 2, time: 2000})
                })
        },
        full_pay_order(order_id) {
            // 全额支付订单
            this.order_detail_show = false
            this.pay_order(order_id, 'full_payment')
        },
        pay_order_balance(order_id) {
            // 已预订支付余款
            this.order_detail_show = false
            this.pay_order(order_id, 'balance_payment')
        },
        deposit_pay_order(order_id) {
            // 支付房源定金
            this.order_detail_show = false
            this.pay_order(order_id, 'deposit_payment')
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
        show_contract(order_index) {
            // 展示订单的合同信息
            let order_item = this.user_orders[order_index]
            console.log('order_item', order_item)
            this.order_detail_item = order_item
            let contract_content = this.order_detail_item.contract_content
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
                        // 格式化时间
                        this.user_orders.forEach(item => {
                            item.update_ts = get_date_str(item.update_ts * 1000)
                        })
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
    },


})
