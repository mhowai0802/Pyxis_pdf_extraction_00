<template>
  <div style="text-align: left">Pyxis financial analysis Tool</div>
  <div class="form-container">
    <input
      type="text"
      class="form-input"
      v-model="input1"
      placeholder="Link of pdf"
    />
    <input
      type="text"
      class="form-input"
      v-model="input2"
      placeholder="Target company"
    />
    <button class="form-button" @click="handleSubmit">
      Insert Data To Mongodb
    </button>
  </div>

  <div class="form-container">
    <input
      type="text"
      class="form-input"
      v-model="input3"
      placeholder="Target Company"
    />
    <button class="form-button" @click="handleSubmit_02">Read Data</button>
  </div>
  
  <div>
    <Table :columns="tableColumns" :items="tableData" style="text-align: left"/>
  </div>
  <h2 style="text-align: left">NVDA Financial statement</h2>
  <div >
    <Table :columns="tableColumns_02" :items="tableData_02" style="text-align: left"/>
  </div>
  <div >
    <button class="form-button" @click="handleSubmit_03">Read Chart Data</button>
  </div>

</template>

<script>
import axios from "axios";
import Table from './Table.vue';


export default {
components: {
    Table
  },
  data() {
    return {
      input1: "",
      input2: "",
      input3: "",
      response_data: [],
      tableColumns: [
        { key: 'Name', label: 'Name' },
        { key: 'Date', label: 'Date' },
        { key: 'Total current assets', label: 'Total current assets' },
        { key: 'Total current liabilities', label: 'Total current liabilities' },
        { key: 'Inventory', label: 'Inventory' }
      ],
      tableData: [],
      tableColumns_02: [
        { key: 'Q4 FY23', label: 'Q4 FY23' },
        { key: 'Q1 FY24', label: 'Q1 FY24' },
        { key: 'Q2 FY24', label: 'Q2 FY24' },
        { key: 'Q3 FY24', label: 'Q3 FY24' },
        { key: 'Q4 FY24', label: 'Q4 FY24' }
      ],
      tableData_02: []
    }
  },
  methods: {
    handleSubmit() {
      // Access the input values and perform the necessary actions
      const value1 = this.input1;
      const value2 = this.input2;
      // Do something with the input values
      console.log("Input 1:", value1);
      console.log("Input 2:", value2);
      const path = "http://localhost:5000/link_to_mongo_db";
      axios
        .post(path, {
          Link: value1,
          Target: value2,
        })
        .then((res) => {
          console.log(res.data);
          this.msg = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
      this.input1 = "";
      this.input2 = "";
    },
    handleSubmit_02() {
      // Access the input values and perform the necessary actions
      const value3 = this.input3;
      // Do something with the input values
      console.log("Input 3:", value3);
      const path = "http://localhost:5000/read_data_from_mongo_db";
      axios
        .post(path, {
          Target: value3,
        })
        .then((res) => {
          console.log(res.data);
          this.tableData = [
          {'Name':res.data['Name'],
           'Date':res.data['Date'],
          'Total current assets': '$' + res.data['Total current assets'],
          'Total current liabilities':'$' + res.data['Total current liabilities'],
          'Inventory':'$' + res.data['Inventory']}
          ]
        })
        .catch((err) => {
          console.error(err);
        });
      this.input3 = "";
    },
    handleSubmit_03() {
    const path = "http://localhost:5000/read_chart_from_mongo_db";
    axios
      .post(path, {})
      .then((res) => {
        console.log(res.data)
        this.tableData_02 = [
          {'Q4 FY23':res.data['Q4 FY23'],
           'Q1 FY24':res.data['Q1 FY24'],
          'Q2 FY24': res.data['Q2 FY24'],
          'Q3 FY24':res.data['Q3 FY24'],
          'Q4 FY24':res.data['Q4 FY24']}
          ]
      })
      .catch((err) => {
        console.error(err);
      });
        }
  },
};
</script>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
}

.form-input {
  padding: 10px;
  margin-bottom: 10px;
  width: 200px;
  border: 1px solid #ddd;
  border-radius: 4px;
  align-self: start;
}

.form-button {
  padding: 5px 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  align-self: start;
}

.form-button:hover {
  background-color: #0056b3;
}
</style>
