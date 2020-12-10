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
        <CodeInput @response="handleResponse"></CodeInput>
      </div>
      <div v-else-if="!initState && viewType == 'cpu'">
        <h2>Your CPU usage: </h2>
        <div v-if="hasCallGraph" class="mb-3">
          <fullButton :modelData="diagramData" ref='goDiagram' style="border: solid 1px black; width:100%; height:400px"></fullButton>
        </div>
      </div>
      <div v-else>
        <h2>Your Mem usage: </h2>
      </div>
      <div v-if="!initState">
        <div id="vis"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
import vegaEmbed from 'vega-embed'
import fullButton from './components/full-button.vue'
import CodeInput from './components/CodeInput.vue'

function obtainHighlightItems(view_) {
  return view_.scenegraph().root.items[0].items[1].items[0].items[1].items[0].items[1].items;
}

function obtainSingleHighlightItems(view_) {
  return view_.scenegraph().root.items[0].items[1].items[0].items[1].items[0].items[2].items;
}

function locateFuncName(baseNodeArr, idx) {
  return baseNodeArr[idx].name;
}

export default {
  name: 'App',
  components: {
    fullButton,
    CodeInput
  },
  data() {
    return {
      initState: true,
      viewType: 'cpu',
      hasCallGraph: false,
      diagramData: {  // passed to <diagram> as its modelData
        fullNodeInfo: [
            {"ID": 0, "name": "main", "selfTime": 0.0, "totalTime": 2.44, "parent": [], "child": [0, 1], "called": 1}, 
            {"ID": 1, "name": "fb", "selfTime": 2.29, "totalTime": 2.29, "parent": [0, 2], "child": [2], "called": 1}, 
            {"ID": 2, "name": "sum", "selfTime": 0.15, "totalTime": 0.15, "parent": [1], "child": [], "called": 1}
        ],

        fullEdgeInfo: [
            {"from": 0, "to": 1, "called": 1, "time": 2.29, "cTime": 2.29, "gcTime": 0.0}, 
            {"from": 0, "to": 2, "called": 1, "time": 0.15, "cTime": 0.15, "gcTime": 0.0}, 
            {"from": 1, "to": 1, "called": 331160280, "time": 0, "cTime": 0, "gcTime": 0}
        ],


        baseNodeArr: [
            {"key": 0, "name": "main", "time": 0.0, "isExpanded": true, "percent": 1, "hide": false, "timePct": 0.0}, 
            {"key": 1, "name": "fb", "time": 2.29, "isExpanded": true, "percent": 1, "hide": false, "timePct": 0.9385245901639344}, 
            {"key": 2, "name": "sum", "time": 0.15, "isExpanded": true, "percent": 1, "hide": false, "timePct": 0.06147540983606557}
        ],

        baseEdgeArr:[
            {"from": 0, "to": 1, "validcalled": 1, "validTime": 2.29, "validCTime": 2.29, "validGcTime": 0.0, "hide": false}, 
            {"from": 0, "to": 2, "validcalled": 1, "validTime": 0.15, "validCTime": 0.15, "validGcTime": 0.0, "hide": false}, 
            {"from": 1, "to": 1, "validcalled": 331160280, "validTime": 0, "validCTime": 0, "validGcTime": 0, "hide": false}
        ],
        // supplied later in execution.
        highlightFunc: undefined,
      },
    }
  },
  methods: {
    moveBack() {
      this.initState = true;
    },
    handleResponse(response) {
      console.log(response);
      this.initState = false;
      this.response = response.vega_json;
      this.viewType = response.type;
      if (response.type == 'cpu') {
        // refresh the view of graph
        this.hasCallGraph = true;
        for (let key of ['fullNodeInfo', 'fullEdgeInfo', 'baseNodeArr', 'baseEdgeArr']) {
          if (!(key in response)) {
            this.hasCallGraph = false;
            break;
          }
        }
        if (this.hasCallGraph) {
          this.diagramData.fullNodeInfo = response.fullNodeInfo;
          this.diagramData.fullEdgeInfo = response.fullEdgeInfo;
          this.diagramData.baseNodeArr = response.baseNodeArr;
          this.diagramData.baseEdgeArr = response.baseEdgeArr;
          this.funcNameCallerGraph = this.buildFuncCallerGraph();
          this.funcNameCalleeGraph = this.buildFuncCalleeGraph();
          this.diagramData.highlightFunc = this.highlightLinesByFunc.bind(this)
          vegaEmbed('#vis', this.response).then(({spec, view}) => {
            this.vega_view = view;
            console.log(this.$refs);
            this.$refs['goDiagram'].updateModel();
          });
        } else {
          vegaEmbed('#vis', this.response).then(({spec, view}) => {
            this.vega_view = view;
          });
        }
      } else {
        vegaEmbed('#vis', this.response).then(({spec, view}) => {
          this.vega_view = view;
        });
      }

    },
    buildFuncCallerGraph() {
        let funcNameGraph = new Object();
        for (let edge of this.diagramData.baseEdgeArr) {
            let name = locateFuncName(this.diagramData.baseNodeArr, edge.from);
            if (!(name in funcNameGraph)) {
              funcNameGraph[name] = new Array();
            }
            let name2 = locateFuncName(this.diagramData.baseNodeArr, edge.to);
            funcNameGraph[name].push(name2);
        }

        for (let node of this.diagramData.baseNodeArr) {
          if (!(node.name in funcNameGraph)) {
            funcNameGraph[node.name] = new Array();
          }
        }
        return funcNameGraph;
    },
    buildFuncCalleeGraph() {
        let funcNameGraph = new Object();
        for (let edge of this.diagramData.baseEdgeArr) {
          let name = locateFuncName(this.diagramData.baseNodeArr, edge.to);
            if (!(name in funcNameGraph)) {
              funcNameGraph[name] = new Array();
            }
            let name2 = locateFuncName(this.diagramData.baseNodeArr, edge.from);
            funcNameGraph[name].push(name2);
        }

        for (let node of this.diagramData.baseNodeArr) {
          if (!(node.name in funcNameGraph)) {
            funcNameGraph[node.name] = new Array();
          }
        }
        return funcNameGraph;
    },
    highlightLines(items, color='red') {
      // let items = obtainHighlightItems(this.vega_view);
      for (let item of items) {
        item.opacity = 1;
        item.stroke = color;
        this.vega_view.dirty(item);
      }
      // this.vega_view.loader();
      this.vega_view.runAsync();
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
      items = obtainSingleHighlightItems(this.vega_view);
      this.clearHighlightLines(items);

      // determine if the block is recursive
      items = obtainHighlightItems(this.vega_view);
      if (this.funcNameCallerGraph[func_name].includes(func_name)) {
          this.highlightLines(items.filter(item=>(item.datum.Func === func_name)), 'brown');
      }
      else {
          this.highlightLines(items.filter(item=>(item.datum.Func === func_name)));
      }

      // highlight the callers and callees.
      items = obtainSingleHighlightItems(this.vega_view);
      this.highlightLines(items.filter(item=>(
            this.funcNameCallerGraph[func_name].includes(item.datum.Func)
            && item.datum.Func !== func_name)), 'yellow');
      this.highlightLines(items.filter(item=>(
            this.funcNameCalleeGraph[func_name].includes(item.datum.Func)
            && item.datum.Func !== func_name)), 'green');
    },
    // this one is deprecated.
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
  /*font-family: Avenir, Helvetica, Arial, sans-serif;*/
  /*-webkit-font-smoothing: antialiased;*/
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
