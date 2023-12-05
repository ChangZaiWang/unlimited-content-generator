<template>
  <div class="input-url" :class="className">
    <input
      v-model="url"
      v-if="property1 === 'default'"
      class="you-tube default"
      type="text"
      :placeholder="text"
    />
  </div>
</template>

<script>

export default {
    name: "InputUrl",
    props: {
        text: {
            type: String,
            default: "請在這裡貼上您的 YouTube 連結",
        },
        property1: {
            type: String,
            default: "default",
            validator: function (value) {
                return ["variant-2", "default"].indexOf(value) !== -1;
            },
        },
        className: {
            type: String,
            default: "",
        },
    },
    data() {
        return {
            url: "",
        };
    },
    methods: {
        updateUrl() {
            this.$emit("input-change", data().url);
            console.log(this.url);
        }
    },
};
</script>

<style>
.input-url {
  align-items: center;
  background-color: #ffffff;
  border: 2px solid;
  border-color: #620d0d;
  border-radius: 45px;
  box-shadow: inset 0px 4px 4px #00000040;
  display: flex;
  gap: 10px;
  height: 57px;
  overflow: hidden;
  padding: 0px 20px;
  position: relative;
  width: 659px;
}

.input-url .you-tube {
  position: relative;
  width: 619px;
}

.input-url .default {
  color: #00000066;
  border: none;
  height: 40px;
  width: 600;
  font-family: "Zen Maru Gothic", Helvetica;
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 0;
  line-height: normal;
}

</style>
