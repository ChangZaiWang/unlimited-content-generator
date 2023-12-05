<template>
  <button @click="python" class="property-1-default" :class="className">
    <svg
      fill="none"
      height="62"
      viewBox="0 0 62 62"
      width="62"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle
        class="circle"
        cx="31"
        cy="31"
        :fill="color"
        r="30"
        :stroke="stroke"
        stroke-width="2"
      />
      <path
        class="path"
        d="M31 4C45.9153 4 58 16.0847 58 31C58 45.9153 45.9153 58 31 58C16.0847 58 4 45.9153 4 31C4 16.0847 16.0847 4 31 4ZM18.371 35.7903H31V43.5093C31 44.6742 32.4153 45.2621 33.2319 44.4347L45.6758 31.9254C46.1875 31.4137 46.1875 30.5972 45.6758 30.0855L33.2319 17.5653C32.4044 16.7379 31 17.3258 31 18.4907V26.2097H18.371C17.6524 26.2097 17.0645 26.7976 17.0645 27.5161V34.4839C17.0645 35.2024 17.6524 35.7903 18.371 35.7903Z"
        :fill="fill"
      />
    </svg>
  </button>
</template>

<script>
import { mapMutations } from 'vuex';
import InputUrl from '../components/InputUrl';

export default {
  name: "Property1Default",
  props: {
    url: String,
    color: {
      type: String,
      default: "#B25757",
    },
    stroke: {
      type: String,
      default: "#630E0E",
    },
    fill: {
      type: String,
      default: "#E7D9D9",
    },
    className: {
      type: String,
      default: "",
    },
  },
  methods: {
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
    },

    python() {
      this.initWebsocket();
      console.log(InputUrl.data)
    }
  }
};
</script>

<style>
.property-1-default {
  border: none;
  cursor: pointer;
  outline: none;
  background-color: #e7d8d9ff;
}
</style>
