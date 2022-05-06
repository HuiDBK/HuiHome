// 系统公告
const get_news_url = api_domain + '/api/v1/common/news';

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

        // 分页数据
        news_list: [],
        news_total: 0,
        current_page_num: 1,
        offset: 0,
        limit: 6,
        page_sizes: [3, 6],
    },
    mounted() {
        this.user_info = verify_user_token()
        this.get_news_list(1)
    },
    methods: {
        get_news_list(page_num) {
            // 获取租房需求列表
            this.current_page_num = page_num
            let json_body = {
                limit: this.limit,
                offset: (this.current_page_num - 1) * this.limit
            }
            axios.post(get_news_url, json_body, {'headers': get_token_headers()})
                .then(resp => {
                    if (resp.status === 200 && resp.data.code === 0) {
                        this.news_list = resp.data.data.data_list
                        this.news_list.forEach(item => {
                            item.create_ts = get_date_str(item.create_ts * 1000, true)
                        })
                        this.news_total = resp.data.data.total
                        console.log('news_list', this.news_list)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
    }
})