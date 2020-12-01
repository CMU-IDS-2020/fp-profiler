<template>
  <div id="app">
    <div class="container">
      <!-- upload a file -->
      <div class="row">
        <form class="col-6" id="upload-file" method="post" enctype="multipart/form-data">
          <div class="custom-file">
            <input @change="selectFile" type="file" name="file" class="custom-file-input" id="customFile">
            <label class="custom-file-label" for="customFile"> {{ file ? file.name : "Select file..." }} </label>
          </div>
        </form>
        <button type="button" class="btn btn-primary" @click="uploadFile">Upload</button>
      </div>
      <p> Response {{ response }} </p>
      <div id="vis"></div>
    </div>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import axios from 'axios'
import $ from 'jquery'
import vegaEmbed from 'vega-embed'

export default {
  name: 'App',
  components: {
    HelloWorld
  },
  data() {
    return {
      file: null,
      response: ':)?',
    }
  },
  methods: {
    selectFile() {
      this.file = $('#upload-file')[0][0].files[0];
    },
    uploadFile() {
      var form_data = new FormData($('#upload-file')[0]);
      $.ajax({
        type: 'POST',
        url: '/upload-file',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: response => {
          this.response = response;
          vegaEmbed('#vis', response);
        },
      });
    }
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
