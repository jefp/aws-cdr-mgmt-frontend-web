/*
 * Copyright 2017-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with
 * the License. A copy of the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
 * CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions
 * and limitations under the License.
 */

 <template >
  <v-stepper v-model="e1" fill-height>
    <v-stepper-header>
      <v-stepper-step :complete="e1 > 1" step="1">Seleccionar fecha</v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step :complete="e1 > 2" step="2">Filtro de busqueda
                  <small>Opcional</small>

      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step step="3">confirmacion</v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content step="1">
<span class="headline">   Seleccione la fecha de busqueda de los CDRs
</span>
              <v-daterange class="body-1"
              :presets="dateRangeOptions['presets']"
              @input="onDateRangeChange"
              v-model="range"
              :input-props="inputProps"
              />

                <v-spacer></v-spacer>
        <v-btn ref='button'
          color="primary"
          :disabled="Object.keys(range).length == 0"
         @click="e1 = 2"
        >
          Continue
        </v-btn>

        <v-btn flat @click="cancel()">Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-content step="2">
        <span class="headline">   Seleccione los filtros (opcional) </span>
        <v-layout row >
        <v-flex sm6 xs12 md5>
           <v-select
          :items="items"
          label="Filter"
          v-model="filter_class"
           />
        </v-flex>
           <v-flex sm6 xs10 md3  offset-xs1  offset-md1>
          <v-text-field
            label="value"
            v-model="filter"
          ></v-text-field>
        </v-flex>
        </v-layout>

        <v-btn
          color="primary"
          @click="e1 = 3"
        >
          Continue
        </v-btn>

<v-btn flat @click="cancel()">Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-content step="3">

        <h3> Desde: {{this.range.start}}</h3><br/>
        <h3> Hasta: {{this.range.end}}</h3><br/>
        <span v-if=this.filter>

        <h3> Filtros: {{this.filter_class}}</h3><br/>
        <h3> Filtros: {{this.filter}}</h3><br/>

        </span>

        <v-btn
          color="primary"
          @click="create"
        >
          Procesar
        </v-btn>

      <v-btn flat @click="cancel()">Cancel</v-btn>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>



<script>

import { format, subDays } from 'date-fns';
import  { CreateJob }  from '@/jobs/components/persist/graphqlActions';


export default {
  name: 'Req',
  data () {
    return {
      items: ['None', 'IMEI', 'CELDA', 'IMSI'],
      inputProps: { style: { width: '300px' } },
      range: {},
      filter: null,
      filter_class: null,
      e1: 0,
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
          logger: {},
      actions: {
        create: CreateJob,
      },
    }
  },
  created() {
    this.logger = new this.$Amplify.Logger('Jobs_component')
  },
    methods: {
    onDateRangeChange(range) {
      this.range = range;
    },
    create() {
      this.$Amplify.API.graphql(this.$Amplify.graphqlOperation(this.actions.create, {from: this.range.start, to: this.range.end, filter: this.filter_class+'-'+this.filter}))
      .then((res) => {
        this.logger.info(`Job created`, res);
        this.$router.push('/Jobs')
      })
      .catch((e) => {
        this.logger.error(`Error creating Job`, e)
      })
    },
    cancel(){
      this.range = {};
      this.e1 = 1 ;
      this.filter = null;
      this.filter_class = null;
    }
  },
  }
</script>
