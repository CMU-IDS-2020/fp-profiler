<template>

  <div>

    <div class="form-group">
      <legend>Profiler option</legend>
      <div class="form-check">
        <label class="form-check-label">
          <input type="radio" v-model="selectType" class="form-check-input" name="optionsRadios" :value="'cpu'">
          CPU profiling
        </label>
      </div>
      <div class="form-check">
        <label class="form-check-label">
          <input type="radio" v-model="selectType" class="form-check-input" name="optionsRadios" :value="'mem'">
          Mem profiling
        </label>
      </div>
    </div>

    <h6>Select your C code and/or edit the code in the editor: </h6>

    <div class="row mb-3">
      <form class="col-6" id="upload-file" method="post" enctype="multipart/form-data">
        <div class="custom-file">
          <input @change="selectFile" type="file" name="file" class="custom-file-input" id="customFile">
          <label class="custom-file-label" for="customFile"> {{ file ? file.name : "Select file..." }} </label>
        </div>
      </form>
      <button type="button" class="btn btn-primary" @click="uploadFile" :disabled="waiting">Upload</button>
    </div>
    <div class="card border border-dark mb-3" style="height: 610px; width: 810px;">
      <div ref="editor" style="height: 600px; width: 800px;"></div>
    </div>
    <div v-if="waiting" class="alert alert-primary">
      <h4 class="alert-heading">Profiling...</h4>
      <p class="mb-0"> Please wait... </p>
    </div>
    <div v-if="error" class="alert alert-dismissible alert-danger">
      <button type="button" class="close" data-dismiss="alert" @click="clearError">&times;</button>
      <h4 class="alert-heading">Error!</h4>
      <p class="mb-0"> {{ errorMessage }} </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
import * as monaco from 'monaco-editor'
import 'bootstrap/dist/js/bootstrap.bundle.js'

export default {
  name: 'CodeInput',
  data() {
    return {
      code: '',
      file: null,
      error: false,
      errorMessage: '',
      selectType: 'cpu',
      waiting: false,
    }
  },
  methods: {
    clearError() {
      this.error = false;
      this.errorMessage = '';
    },
    selectFile() {
      this.file = $('#upload-file')[0][0].files[0];
      var request = new XMLHttpRequest();
      var fr = new FileReader(); 
      fr.onload = () => { 
        this.editor.setValue(fr.result); 
      }
      fr.readAsText(this.file);
    },
    uploadFile() {
      this.waiting = true;
      let postUrl = '/upload-file';
      if (this.selectType != 'cpu') {
        postUrl = '/mem-profile';
      }
      axios.post(postUrl, {
        code: this.editor.getValue(),
      }).then(response => {
        console.log(response);
        if (response.data.error) {
          console.log(response.data);
          this.error = true;
          this.errorMessage = response.data.error_message;
          this.editor.setValue(response.data.source)
        } else {
          this.error = false;
          this.errorMessage = '';
          let res = response.data;
          res.type = this.selectType;
          this.$emit('response', res);
        }
        this.waiting = false;
      }).catch(function (error) {
        console.log(error);
      });
    },
  },
  async mounted() {
    const el = this.$refs.editor;
    this.editor = monaco.editor.create(el, {
      value: "",
      language: 'cpp',
    });
  },
}
</script>

