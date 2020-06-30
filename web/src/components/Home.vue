<template>
  <v-container fluid pa-0>
    <v-layout justify-end row fill-height>
      <v-flex xs12 md3 lg3>
          <v-daterange class="body-1"
              :presets="dateRangeOptions['presets']"
              @input="onDateRangeChange"
              v-model="range"
              :input-props="inputProps"
            />
      </v-flex>
    </v-layout>
    <v-container fluid>
        <v-layout row fill-height>
      <v-flex xs12 md4 lg4>
      <v-card>
        <v-card-title primary-title v-model="api">
          <div>
            <h3 class="headline mb-0">Total files in the system: <br/>
            <b> {{this.api['global']['total_files'] }} </b>
            </h3>
          </div>
        </v-card-title>
      </v-card>
    </v-flex>
          <v-flex xs12 md4 lg4>
      <v-card>
        <v-card-title primary-title v-model="api">
          <div>
            <h3 class="headline mb-0">Total cdrs in the system:<br/>
            <b>  {{this.api['global']['total_cdr'] }}</b>
            </h3>
          </div>
        </v-card-title>
      </v-card>
    </v-flex>
          <v-flex xs12 md4 lg4>
      <v-card>
        <v-card-title primary-title v-model="api">
          <div>
            <h3 class="headline mb-0">Total size in the system:<br/>
            <b> {{ getReadableFileSizeString(this.api['global']['size'])}} </b>
            </h3>
          </div>
        </v-card-title>
      </v-card>
    </v-flex>
  </v-layout>

<v-layout row fill-height pt-4>
      <v-flex xs12 md12 lg12>
  <div class="echarts">
    <IEcharts
      :option="bar"
      :loading="loading"
    />
  </div>
    </v-flex>
 </v-layout>
  </v-container>
  </v-container>
</template>



<script>


import { format, subDays } from 'date-fns';
import aws_exports from '../aws-exports';


import { Auth,API, Storage, Logger } from 'aws-amplify'

import IEcharts from 'vue-echarts-v3/src/full.js';
import AmplifyStore from '../store/store';


export default {
  name: 'Home',
  components: {
      IEcharts
    },
  data () {
    return {
      loading: true,
      inputProps: { style: { width: '300px'} },
      range: {start: format(subDays(new Date(),30), 'YYYY-MM-DD'), end: format(new Date(), 'YYYY-MM-DD')},
      api: {'global': {'total_files': 'loading', 'size': 'loading', 'total_cdr': 'loading'}},
      dateRangeOptions: {
        presets: [
          {
            label: 'Today',
            range: [
              format(new Date(), 'YYYY-MM-DD'),
              format(new Date(), 'YYYY-MM-DD'),
            ],
          },
          {
            label: 'Yesterday',
            range: [
              format(subDays(new Date(), 1), 'YYYY-MM-DD'),
              format(subDays(new Date(), 1), 'YYYY-MM-DD'),
            ],
          },
          {
            label: 'Last 30 Days',
            range: [
              format(subDays(new Date(), 30), 'YYYY-MM-DD'),
              format(subDays(new Date(), 1), 'YYYY-MM-DD'),
            ],
          },
        ],
      },
      yMax:500,
      bar:{
         autoresize:true,
         title:{
            text:'Total CDR'
         },
         tooltip:{},
         xAxis:{
            data:[],
            axisLabel:{
               inside:true,
               textStyle:{
                  color:'#fff'
               }
            },
            axisTick:{
               show:false
            },
            axisLine:{
               show:false
            },
            z:10
         },
         yAxis:{
            axisLine:{
               show:false
            },
            axisTick:{
               show:false
            },
            axisLabel:{
               textStyle:{
                  color:'#999'
               }
            }
         },
         dataZoom:[
            {
               type:'inside'
            }
         ],
         series: [{
          name: 'Sales',
          type: 'bar',
          data: [5, 20, 36, 10, 10, 20]
        }]
      }
    }
  },
  created() {
    this.logger = new this.$Amplify.Logger('Jobs_component');
    setInterval(() => this.getStats(), 10000)
  },
methods: {
  onDateRangeChange(range) {
      this.loading = true;
      this.range = range;
    },
    fval(js,k,keys){
      var r = [];
      for (var i = 0; i < keys.length; i++){
        r.push(js[keys[i]][k]);
        console.log(r);

      }
      return r;
    },
    remove(arr,elem){
      return arr.filter(function(value, index, arr){
          return value != elem ;
    });
    }
    ,
     getReadableFileSizeString(fileSizeInBytes) {
    var i = -1;
    var byteUnits = [' kB', ' MB', ' GB', ' TB', 'PB', 'EB', 'ZB', 'YB'];
    do {
        fileSizeInBytes = fileSizeInBytes / 1024;
        i++;
    } while (fileSizeInBytes > 1024);

    return Math.max(fileSizeInBytes, 0.1).toFixed(1) + byteUnits[i];
},
      async getStats() {
      let apiName = aws_exports['API']['endpoints'][0]['name'];
      let path = aws_exports['API']['endpoints'][0]['path'];
      let session = await Auth.currentSession();
      let myInit = {
        headers: {
          Authorization: session.idToken.jwtToken
        },
        queryStringParameters: {
          from:  this.range.start,
          to: this.range.end
        }
      }
      API.get(apiName, path, myInit).then(response => {
        this.api=response;
        this.loading = false;
        this.bar.xAxis.data = this.remove(Object.keys(response),'global');
        this.bar.series[0].data = this.fval(response,'total_cdr',this.bar.xAxis.data);
      }).catch(error => {
       console.log(error)
    });

  }
}
  }
</script>

<style scoped>
  .echarts {
    height: 400px;
  }
</style>


