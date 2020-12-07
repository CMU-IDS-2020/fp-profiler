<template>
  <div>
    <div class="row mb-3">
      <form class="col-6" id="upload-file" method="post" enctype="multipart/form-data">
        <div class="custom-file">
          <input @change="selectFile" type="file" name="file" class="custom-file-input" id="customFile">
          <label class="custom-file-label" for="customFile"> {{ file ? file.name : "Select file..." }} </label>
        </div>
      </form>
    <button type="button" class="btn btn-primary" @click="uploadFile">Upload</button>
    </div>
    <div class="card border border-dark" style="height: 610px; width: 810px;">
      <div ref="editor" style="height: 600px; width: 800px;"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
import * as monaco from 'monaco-editor';

export default {
  name: 'CodeInput',
  data() {
    return {
      code: '',
      file: null,
    }
  },
  methods: {
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
      axios.post('/upload-file', {
        code: this.editor.getValue(),
      }).then(response => {
        console.log(response);
        this.$emit('response', response.data.vega_json);
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

