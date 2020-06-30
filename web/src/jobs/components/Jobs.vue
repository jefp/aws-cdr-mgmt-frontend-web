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

 <template>
  <v-container grid-list-md text-xs-center>
    <v-layout row wrap>
      <v-flex xs12>
          <v-card-text class="px-0">Mostrando los ultimos 100 trabajos</v-card-text>
        <v-card dark>
          <v-card-text class="px-0">Trabajos solicitados</v-card-text>
        </v-card>
        <v-card>
            <v-data-table ref="table"
              :headers="headers"
              :items="jobs"
              :sort-by="['createdAt','lastUpdated']"
              :sort-desc="[false,true]"
              class="elevation-1"
              multi-sort
            >
      <template slot="items" slot-scope="props">
     <tr>
      <td>{{ props.item.id }}</td>
      <td>{{ props.item.from }}</td>
      <td>{{ props.item.to }}</td>
      <td>{{ props.item.filter }}</td>
      <td class="font-weight-bold">
        {{ props.item.jobStatus }}
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <span v-on="on">{{ props.item.jobStatus }}</span>
        </template>
        <span>{{ props.item.jobStatusDescription }}</span>
      </v-tooltip>
        <a :href="props.item.results" v-if="props.item.jobStatus === 'completed'">(download)</a>
      </td>
      <td>{{ props.item.createdAt }}</td>
      <td>{{ props.item.lastUpdated }}</td>
     </tr>
    </template>
  </v-data-table>

      </v-card>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
import Vue from 'vue'
import { Logger } from 'aws-amplify'
import { JS } from 'fsts'

import AmplifyStore from '../../store/store'

import  { ListJobs }  from '@/jobs/components/persist/graphqlActions';

import Job from './Job'

Vue.component('a-job', Job)

export default {
  name: 'Jobs',
  data () {
    return {
        headers: [
          {
            text: 'id',
            sortable: false,
            value: 'name'
          },
          { text: 'From', value: 'from' },
          { text: 'To', value: 'to' },
          { text: 'Filter', value: 'filter' },
          { text: 'Status', value: 'status' },
          { text: 'Created at', value: 'createdAt'},
          { text: 'Last update', value: 'lastUpdated'}
          ],
      job: '',
      jobs: [],
      filter: 'all',
      logger: {},
      actions: {
        list: ListJobs
      },
      pagination: {
      page: 1,
      rowsPerPage: 50,
      totalItems: 0
    },
    }
  },
  created() {
    this.logger = new this.$Amplify.Logger('Jobs_component')
    this.list();
  },
  completed(input) {
    return true;
  },
  computed: {
    userId: function() { return AmplifyStore.state.userId },
    tablePagination: function() {console.log('xxx');}
  },
  methods: {
    list() {
      this.$Amplify.API.graphql(this.$Amplify.graphqlOperation(this.actions.list, {limit: this.pagination.rowsPerPage}))
      .then((res) => {
        this.jobs = res.data.listJobs.items;
        this.logger.info(`Jobs successfully listed`, this.jobs)
       // this.$refs.table.refresh();
      })
      .catch((e) => {
        this.logger.error(`Error listing Jobs`, e)
      });
    }
  }
}
</script>
