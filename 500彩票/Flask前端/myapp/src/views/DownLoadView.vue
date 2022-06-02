<template>
  <div>
    <el-card>
      <div>
        <el-date-picker
          v-model="queryForm.value1"
          type="daterange"
          range-separator="To"
          start-placeholder="开始时间"
          end-placeholder="结束时间"
          unlink-panels
        />
        <el-button
          type="primary"
          :icon="Search"
          @click="initgetGamesDataList"
          class="date-picker"
          >查询</el-button
        >
        <el-button
          type="primary"
          :icon="Tools"
          class="date-picker"
          @click="startspider"
          >启动爬虫</el-button
        >
        <el-button
          type="primary"
          :icon="Download"
          class="date-picker"
          @click="deriveExcel"
          >下载数据</el-button
        >
        <el-dropdown class="logout">
          <span class="el-dropdown-link">
            <el-avatar shape="square" :size="40" :src="squareUrl" />
            <el-icon class="el-icon--right">
              <arrow-down />
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
      <el-table :data="tableData" height="430px" style="width: 100%" id="table">
        <el-table-column
          :width="item.width"
          :prop="item.prop"
          :label="item.label"
          v-for="(item, index) in options"
          :key="index"
        >
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { options } from "./options";
import { ref, reactive } from "vue";
import { Search, Download, Tools } from "@element-plus/icons-vue";
import XLSX from "xlsx";
import { useStore } from "vuex";
import { getGamesData, startSpider } from "@/api/getdata.js";
const store = useStore();

const squareUrl = ref(
  "https://img0.baidu.com/it/u=1056811702,4111096278&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500"
);
// 下载数据的文件名
const state = reactive({
  date: "",
  time: "",
  week: "",
  showIndex: 0,
});
const myDate = new Date();
let month = (myDate.getMonth() + 1).toString().padStart(2, "0");
let day = myDate.getDate().toString().padStart(2, "0");
let hour = myDate.getHours().toString().padStart(2, "0");
let minutes = myDate.getMinutes().toString().padStart(2, "0");
let seconed = myDate.getSeconds().toString().padStart(2, "0");
state.date = myDate.getFullYear() + "-" + month + "-" + day;
state.time = hour + "时" + minutes;
const file_name = "500彩票-" + state.date + " " + state.time + "分.xlsx";
const tableData = ref([]);
// 下载数据
const deriveExcel = () => {
  let workbook = XLSX.utils.table_to_book(document.getElementById("table")); //需要在table上定义一个id
  XLSX.writeFile(workbook, file_name);
};
const queryForm = ref({
  query: "",
  pagenum: 1,
  pagesize: 2,
  value1: "",
});
const initgetGamesDataList = async () => {
  // 获取加密数据
  const res = await getGamesData(queryForm.value);
  tableData.value = res.data;
};
const startspider = async () => {
  await startSpider();
};
initgetGamesDataList();
const logout = () => {
  store.dispatch("app/logout");
};
</script>

<style lang="scss">
.date-picker {
  margin-bottom: 10px;
  margin-left: 20px;
}
.logout {
  margin-left: 500px;
}
</style>
