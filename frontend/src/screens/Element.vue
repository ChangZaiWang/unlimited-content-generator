<template>
  <div class="element">
    <div class="div">
      <div class="overlap">
        <div class="group">
          <div class="text-wrapper">YouTube連結轉換</div>
          <div class="text-wrapper-2">一鍵轉換您的影片內容</div>
        </div>
      </div>
      <div class="overlap-group">
        <InputUrl class="input-url-instance" property1="default" text="請在這裡貼上您的 YouTube 連結" />
        <Property1Default class="bottum-go" color="#B25757" fill="#E7D9D9" stroke="#630E0E" />
      </div>
    </div>
  </div>
</template>

<script>
import InputUrl from "../components/InputUrl";
import Property1Default from "../icons/Property1Default";

export default {
  name: "Element",
  components: {
    InputUrl,
    Property1Default,
  },
  data() {
    return {
      connected: false,
      message: '',
      messages: [],
      url: '',
    };
  },
  methods: {
    download() {
      if (this.url) {
        // 使用 WebSocket 向後端發送請求
        this.$socket.sendObj({
          type: 'download',
          url: this.url,
        });
      } else {
        alert('請輸入URL');
      }
    }
  },
};


</script>

<style>
.element {
  background-color: #ffffff;
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
}

.element .div {
  background-color: #ffffff;
  height: 832px;
  position: relative;
  width: 1280px;
}

.element .overlap {
  background-color: #c5d9c499;
  box-shadow: 0px 4px 4px #00000040;
  height: 279px;
  left: 0;
  position: absolute;
  top: 0;
  width: 1280px;
}

.element .group {
  height: 192px;
  left: 51px;
  position: relative;
  top: 45px;
  width: 1183px;
}

.element .text-wrapper {
  color: #022608;
  font-family: "Zen Maru Gothic", Helvetica;
  font-size: 80px;
  font-weight: 700;
  height: 75px;
  left: 258px;
  letter-spacing: 0;
  line-height: normal;
  position: absolute;
  text-align: center;
  top: 0;
  white-space: nowrap;
  width: 663px;
}

.element .text-wrapper-2 {
  color: #022608;
  font-family: "Zen Maru Gothic", Helvetica;
  font-size: 60px;
  font-weight: 700;
  height: 75px;
  left: 0;
  letter-spacing: 0;
  line-height: normal;
  position: absolute;
  text-align: center;
  top: 117px;
  width: 1179px;
}

.element .overlap-group {
  background-color: #e1cfcfcc;
  height: 553px;
  left: 0;
  position: absolute;
  top: 279px;
  width: 1280px;
}

.element .input-url-instance {
  left: 311px !important;
  position: absolute !important;
  top: 203px !important;
}

.element .bottum-go {
  height: 62px !important;
  left: 983px !important;
  position: absolute !important;
  top: 201px !important;
  width: 62px !important;
}
</style>