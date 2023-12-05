import { mapMutations } from 'vuex';
export const mixinWebsocket = {
    data(){
        return{
            ws: null,
        }
    },
    methods:{
        ...mapMutations(['setWsNotify']),
        //初始websocket
        initWebsocket(){
            let wsURL = `ws://localhost:8765`;
            this.ws = new WebSocket(wsURL); //建立連線
            this.ws.onopen = this.websocketonopen;
            this.ws.error = this.websocketonerror;
            this.ws.onmessage = this.websocketonmessage;
            this.ws.onclose = this.websocketclose;
        },
        websocketonopen(){
            console.log('ws 連線成功~~');
        },
        websocketonerror(e){
            console.error('ws 連線失敗',e);
        },
        websocketonmessage(e){
            // 後端通知前端，前端取得資料
            let _data = e.data;
            //當有後端資料送到前端，利用vuex存到共用的state
            this.setWsNotify({
                id:uuid.v4(), 
                data: JSON.parse(_data)
            });
            console.log('ws 取得資料',_data);
        },
        websocketsend(data){
            //前端丟資料
            console.log('send data',data);
        },
        websocketclose(){
            console.log('ws 關閉連線')
        }
    }
}