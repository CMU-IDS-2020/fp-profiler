<template>
  <div id="app">

    <div class="navbar navbar-expand-lg fixed-top navbar-light bg-light" style="">
      <div class="container">
        <div class="mr-auto">
          <h1>Profiler</h1>
        </div>
        <div class="ml-auto">
            <button class="btn btn-primary" :disabled="initState" v-on:click="moveBack">
              <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-arrow-left-circle-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.5.5a.5.5 0 0 0 0-1H5.707l2.147-2.146a.5.5 0 1 0-.708-.708l-3 3a.5.5 0 0 0 0 .708l3 3a.5.5 0 0 0 .708-.708L5.707 8.5H11.5z"/>
              </svg>
              Back
            </button>
        </div>
      </div>
    </div>

    <div class="container">
      <div v-if="initState" >
        <h6>Select your C code and/or edit the code in the editor: </h6>
        <CodeInput @response="handleResponse"></CodeInput>
      </div>
      <div v-else>
        <h2>linewise CPU usage: </h2>
        <div id="vis"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
import vegaEmbed from 'vega-embed'
import GoDiagram from './components/GoDiagram.vue'
import CodeInput from './components/CodeInput.vue'

function obtainHighlightItems(view_) {
  return view_.scenegraph().root.items[0].items[1].items[0].items[1].items[0].items[1].items;
}

export default {
  name: 'App',
  components: {
    GoDiagram,
    CodeInput
  },
  data() {
    return {
      initState: true,
      diagramData: {  // passed to <diagram> as its modelData
        nodeDataArray: [
          { key: 1, text: "Alpha", color: "lightblue" },
          { key: 2, text: "Beta", color: "orange" },
          { key: 3, text: "Gamma", color: "lightgreen" },
          { key: 4, text: "Delta", color: "pink" }
        ],
        linkDataArray: [
          { from: 1, to: 2 },
          { from: 1, to: 3 },
          { from: 3, to: 4 }
        ]
      },
    }
  },
  methods: {
    moveBack() {
      console.log("Hello");
      this.initState = true;
    },
    handleResponse(response) {
      this.initState = false;
      vegaEmbed('#vis', response).then(({spec, view}) => {
        this.vega_view = view;
      })
    },
    highlightLines(items) {
      // let items = obtainHighlightItems(this.vega_view);
      for (let item of items) {
        item.opacity = 0.5;
        this.vega_view.dirty(item);
      }
    },
    clearHighlightLines(items) {
      for (let item of items) {
        if (item.opacity > 0.0) {
          item.opacity = 0.0;
          this.vega_view.dirty(item);
        }
      }
    },
    highlightLinesByFunc(func_name) {
      let items = obtainHighlightItems(this.vega_view);
      this.clearHighlightLines(items);
      this.highlightLines(items.filter(item=>(item.datum.Func === func_name)));
    },
    highlightLinesByLnum(line_nums) {
      let items = obtainHighlightItems(this.vega_view);
      this.clearHighlightLines(items);
      this.highlightLines(items.filter(item=>(line_nums.includes(item.datum['Line Number']))));
    }
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/
  color: #2c3e50;
  margin-top: 60px;
}

body { padding-top: 40px; }
@media screen and (max-width: 768px) {
    body { padding-top: 0px; }
}
</style>
