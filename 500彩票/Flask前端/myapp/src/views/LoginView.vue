<template>
  <div class="login">
    <div class="login_title">
      <h2>轨道交通数据可视化登录</h2>
      <div class="login_context">
        <div class="login_logo">
          <!-- <img src="../assets/R-C.jpg" alt="" /> -->
        </div>
        <el-form ref="formRef" :model="form" :rules="rules" class="login_box">
          <el-form-item label="账 号：" prop="username">
            <el-input v-model="form.username" />
          </el-form-item>
          <el-form-item label="密 码：" prop="password">
            <el-input v-model="form.password" type="password" />
          </el-form-item>
          <el-button type="primary" class="btns" @click="handleLogin"
            >登录</el-button
          >
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useStore } from "vuex";
const store = useStore();
const form = ref({
  username: "王刻",
  password: "123456",
});
const rules = ref({
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
});
const formRef = ref(null);
// 统一验证
const handleLogin = () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      store.dispatch("app/login", form.value);
    } else {
      console.log("error submit!!");
      return false;
    }
  });
};
</script>

<style lang="scss">
.login {
  /* 高度 */
  height: 100%;
}
.login_title {
  /* 字体水平左右居中 */
  text-align: center;
}

.login_context {
  /* 宽度 */
  width: 450px;
  /* 高度 */
  height: 300px;
  /* 背景色 */
  background: #fff;
  /* 属性定位 */
  position: absolute;
  /* 属性定位，顶部占比 */
  top: 50%;
  /* 属性定位，左侧占比 */
  left: 50%;
  /* 水平垂直居中 */
  transform: translate(-50%, -50%);
  /* 四个角的圆角角度 */
  border-radius: 20px;
  /* 阴影 */
  box-shadow: 0 0 5px 2px #ddd;
}

.login_logo {
  /* 宽度 */
  width: 150px;
  /* 高度 */
  height: 150px;
  /* 属性定位 */
  position: absolute;
  /* 属性定位，顶部占比 */
  top: -75px;
  /* 属性定位，左侧占比 */
  left: 49%;
  /* logo左侧边距 */
  margin-left: -75px;
  /* 带有边框属性 */
  border: 1px solid #eee;
  /* 四个角的圆角角度 */
  border-radius: 50%;
  /* 背景色 */
  background: #fff;
  /* 设置内边距属性 */
  padding: 10px;
  /* 阴影 */
  box-shadow: 0 0 2px 2px #ddd;
}

.login_logo img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgb(238, 238, 238);
}

.login_box {
  width: 100%;
  position: absolute;
  bottom: 20px;
  padding: 0 50px;
  /* 边框边距 */
  box-sizing: border-box;
}

.btns {
  width: 100px;
}
</style>
