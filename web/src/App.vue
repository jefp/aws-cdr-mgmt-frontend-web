/*
 * Copyright 2017-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with
 * x the License. A copy of the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
 * CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions
 * and limitations under the License.
 */

<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Telco</span>
        <span class="font-weight-light">CDR MGMT</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-img
        :src="require('./assets/wireless-308829_1280.svg')"
        class="my-3"
        max-height="200"
        max-width="100"
      ></v-img>
    </v-toolbar>
    <v-content>
    <router-view/>
    <v-menu/>
    </v-content>
  </v-app>
</template>

<script>
import Vue from 'vue'
import Menu from '@/components/Menu';
Vue.component('v-menu', Menu)

window.LOG_LEVEL = 'VERBOSE';

export default {
  name: 'app'
}
</script>
