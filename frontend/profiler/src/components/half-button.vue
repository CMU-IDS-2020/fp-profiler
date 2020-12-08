<template>
  <div></div>
</template>

<script>
// Reference: https://gojs.net/latest/samples/vue.html
// This is only for the evaluation purpose of gojs library.

import go from 'gojs'
var $ = go.GraphObject.make;

export default {
    name: 'halfButton',
    props: {
        modelData: object
    },
    mounted: function() {
        var self = this;
        
        var nodeHeight = 60;
        var NodeInfoSize = new go.Size(50,25);

        var smallfont = "bold 11pt Helvetica, Arial, sans-serif";
        var legendfont = "11pt Helvetica, Arial, sans-serif";
        var titlefont = "13pt Helvetica, Arial, sans-serif";

        var myDiagram =
            $(go.Diagram, this.$el,
            {
                layout: $(go.LayeredDigraphLayout, { isInitial: false, isOngoing: false, layerSpacing: 50 }),
                hoverDelay: 100,
                allowMove: true,
                "undoManager.isEnabled": true,
                "toolManager.mouseWheelBehavior": go.ToolManager.WheelZoom,
                "ChangedSelection": function(e) { self.$emit("changed-selection", e); }
            });

        myDiagram.animationManager.initialAnimationStyle = go.AnimationManager.None;
        /* Define adornment template */
        var defaultAdornment =
            $(
                go.Adornment, "Spot",
                $(go.Panel, "Auto",
                    $(go.Shape, 
                        {   
                            fill: null, 
                            stroke: "dodgerblue", 
                            strokeWidth: 4,
                            opacity: 1
                        },
                        new go.Binding("opacity", "ifShow")),
                    $(go.Placeholder)),
                // the button to create a "next" node, at the top-right corner
                $("Button",
                    {
                    alignment: go.Spot.TopRight,
                    click: this.expand_button
                    },  // this function is defined below
                    new go.Binding("visible", "", function(node) { 
                        var data = node.data; 
                        if (data.ifShow == 1)
                            return !data.isExpanded; 
                        return false
                    }).ofObject(),
                    $(go.Shape, "PlusLine", { desiredSize: new go.Size(6, 6) })
                ),
                $("Button",
                    {
                    alignment: go.Spot.TopRight,
                    click: this.collapse_button
                    },  // this function is defined below
                    new go.Binding("visible", "", function(node) { 
                        var data = node.data; 
                        if (data.ifShow == 1)  
                            return data.isExpanded; 
                        return false;
                    }).ofObject(),
                    $(go.Shape, "MinusLine", { desiredSize: new go.Size(6, 6) })
                ),
        );

        /* Define node hover adornment template */
        var nodeHoverAdornment =
            $(
                go.Adornment, "Spot",
                {
                    background: "transparent",
                    // hide the Adornment when the mouse leaves it
                    mouseLeave: function(e, obj) {
                    var ad = obj.part;
                    ad.adornedPart.removeAdornment("mouseHover");
                    }
                },
                $(go.Placeholder,
                    {
                    background: "transparent",  // to allow this Placeholder to be "seen" by mouse events
                    isActionable: true,  // needed because this is in a temporary Layer
                    click: function(e, obj) {
                        var node = obj.part.adornedPart;
                        node.diagram.select(node);
                    }
                    }),
                // $("Button",
                //     { alignment: go.Spot.Right, alignmentFocus: go.Spot.Left },
                //     { click: function(e, obj) { alert("Show more info"); } },
                //     $(go.TextBlock, "Show more info"))
            );

        /* Define node template*/
        
        myDiagram.nodeTemplate =
            $(go.Node, "Auto",
                { selectionAdornmentTemplate: defaultAdornment,
                    portId: "",
                    cursor: "pointer",
                    toEndSegmentLength: 50, fromEndSegmentLength: 40,
                    height: nodeHeight,
                    width: 200
                },
                new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
                new go.Binding("width", "width", function (val) {return val + 1}),
            
                $(go.Panel,
                        $(go.Panel, "Auto",

                            $(go.Shape, "RoundedTopRectangle",
                            //{ desiredSize: NodeInfoSize },
                                {
                                    fill: "white",
                                    height: nodeHeight/2,
                                    width: 200-1,
                                    opacity: 1
                                },
                                new go.Binding("fill", "color"),
                                new go.Binding("opacity", "width"),
                                new go.Binding("width", "width")
                            ),
                            {
                                toolTip: $("ToolTip",
                                $(go.TextBlock, "",
                                {
                                    margin: 6,
                                    font: smallfont,
                                    editable: false,
                                    stroke: "#2F4F4F",
                                    textAlign: "center",
                                    segmentOffset: new go.Point(0, 0),
                                    //segmentOrientation: go.Link.
                                },
                                new go.Binding('text', 'nodeInfoWhole')))
                                }
                        ),
                        $(go.Panel, "Auto",
                            // desiredSize: NodeInfoSize },
                            { position: new go.Point(0, nodeHeight/2 - 1) },
                            $(go.Shape, "RoundedBottomRectangle",
                            {
                                fill: "white",
                                height: nodeHeight/2,
                                width: 200-1,
                                opacity: 1
                            },
                            new go.Binding("fill", "selfColor"),
                            new go.Binding("opacity", "ifShow"),
                            new go.Binding("width", "widht")
                            ),
                            {
                                toolTip: $("ToolTip",
                                $(go.TextBlock, "",
                                {
                                    margin: 6,
                                    font: smallfont,
                                    editable: false,
                                    stroke: "#2F4F4F",
                                    textAlign: "center",
                                    segmentOffset: new go.Point(0, 0),
                                    //segmentOrientation: go.Link.
                                },
                                new go.Binding('text', 'nodeInfoSelf')))
                            }
                        ),
                ),
                $(go.TextBlock, "Function",
                    {
                    margin: 12,
                    font: smallfont,
                    editable: true,
                    textAlign: 'center',
                    opacity: 1
                    },
                    new go.Binding("text", "name").makeTwoWay()),
                    new go.Binding("opacity", "ifShow")
            );
                        
    
        myDiagram.linkTemplate = 
            $(
                go.Link,
                {curve: go.Link.Bezier},
                $(go.Shape,
                    {
                        stroke: "#2F4F4F",
                        opacity: 1
                    },
                    new go.Binding("strokeWidth", "ewidth"),
                    new go.Binding("opacity", "ifShow")
                ),
                $(go.Shape,
                    {
                        toArrow: 'standard', 
                        fill: "#2F4F4F", 
                        scale: 1,
                        opacity: 1
                    },
                    new go.Binding("opacity", "ifShow")
                ),
                {
                toolTip: $("ToolTip",
                    $(go.TextBlock, "",
                        {
                            margin: 6,
                            font: smallfont,
                            editable: false,
                            stroke: "#2F4F4F",
                            segmentOffset: new go.Point(0, -7),
                            segmentOrientation: go.Link.OrientUpright
                        },
                        new go.Binding('text', 'calledInfo'))
                    )
                }
            )

        /* Set block width */
        baseNodeArr = this.getBaseNodeArr();
        let i;
        for (i = 0; i < baseNodeArr.length; i++ ) {
            var namelen = baseNodeArr[i].name.length;
            console.log(baseNodeArr[i].name, namelen);
            baseNodeArr[i].width = namelen * 10;
            baseNodeArr[i].width += 40;
        }

        /* Set legend */
        var x= -200;
        var baseY = 150;
        var ny = 20;
        var nx = 40

        myDiagram.add(
            $(go.Part, {location: new go.Point(x, baseY) },
                $(go.Shape, "Rectangle", {fill: "#ee9779", height: ny, width: nx})
            )
        );
        myDiagram.add(
            $(go.Part,
            {location: new go.Point(x+50, baseY+3)},
            $(go.TextBlock, "0-20%", 
                { font: legendfont, stroke: "black"}))
        );
        myDiagram.add(
            $(go.Part, {location: new go.Point(x, baseY-30) },
                $(go.Shape, "Rectangle", {fill: "#ea7254", height: ny, width: nx})
            )
        );
        myDiagram.add(
            $(go.Part,
            {location: new go.Point(x+50, baseY-30+3)},
            $(go.TextBlock, "20-40%", 
                { font: legendfont, stroke: "black"}))
        );
        myDiagram.add(
            $(go.Part, {location: new go.Point(x, baseY-60) },
                $(go.Shape, "Rectangle", {fill: "#dc4a38", height: ny, width: nx})
            )
        );
        myDiagram.add(
            $(go.Part,
            {location: new go.Point(x+50, baseY-60+3)},
            $(go.TextBlock, "40-60%", 
                { font: legendfont, stroke: "black"}))
        );
        myDiagram.add(
            $(go.Part, {location: new go.Point(x, baseY-90) },
                $(go.Shape, "Rectangle", {fill: "#bb2f29", height: ny, width: nx})
            )
        );
        myDiagram.add(
            $(go.Part,
            {location: new go.Point(x+50, baseY-90+3)},
            $(go.TextBlock, "60-80%", 
                { font: legendfont, stroke: "black"}))
        );
        myDiagram.add(
            $(go.Part, {location: new go.Point(x, baseY-120) },
                $(go.Shape, "Rectangle", {fill: "#8c1a18", height: ny, width: nx})
            )
        );
        myDiagram.add(
            $(go.Part,
            {location: new go.Point(x+50, baseY-120+3)},
            $(go.TextBlock, ">80%", 
                { font: legendfont, stroke: "black"}))
        );


        myDiagram.add(
            $(go.Part,
            {location: new go.Point(x-20, baseY-150)},
            $(go.TextBlock, "Run-time Percent",
            {font: titlefont, stroke: "black"})
            )
        );

        myDiagram.add(
            $(go.Part, {location: new go.Point(x-10, baseY + 60)},
                $(go.Shape, "RoundedTopRectangle", {fill: "#8c1a18", height: ny+5, width: nx+20})
            )
        )
        myDiagram.add(
            $(go.Part,
            {location: new go.Point(x+55, baseY + 65)},
            $(go.TextBlock, "Total time", 
                { font: legendfont, stroke: "black"}))
        );
        myDiagram.add(
            $(go.Part, {location: new go.Point(x-10, baseY + 85)},
                $(go.Shape, "RoundedBottomRectangle", {fill: "#ee9779", height: ny+5, width: nx+20})
            )
        );
        myDiagram.add(
            $(go.Part,
            {location: new go.Point(x+55, baseY + 90)},
            $(go.TextBlock, "Self time", 
                { font: legendfont, stroke: "black"}))
        );


        this.diagram = myDiagram;
        this.updateModel();

    },
    methods: {
        model: function() { return this.diagram.model; },
        getFullNodeInfo: function() {
            return this.modelData.fullNodeInfo;
        },
        getFullEdgeInfo: function() {
            return this.modelData.fullEdgeInfo;
        },
        getBaseNodeArr: function() {
            return this.modelData.baseNodeArr;
        },
        getBaseEdgeArr: function() {
            return this.modelData.baseEdgeArr;
        },
        updateModel: function() {
            // No GoJS transaction permitted when replacing Diagram.model.
            
            var drawNodeArr = [];
            let i;

            var fullNodeInfo = this.getFullNodeInfo();
            var fullEdgeInfo = this.getFullEdgeInfo();
            var baseNodeArr = this.getBaseNodeArr();
            var baseEdgeArr = this.getBaseEdgeArr();
            
            var graphTotalTime = fullNodeInfo[0].totalTime;
            var maxEdgeWidth = 5;
            var minEdgeWidth = 1;

            for (i = 0; i < baseNodeArr.length; i++) {
                if (baseNodeArr[i].hide == false) {
                    baseNodeArr[i].timePct = baseNodeArr[i].time / graphTotalTime;
                    baseNodeArr[i].selfColor = this.find_color(baseNodeArr[i].timePct);
                    baseNodeArr[i].color = this.find_color(fullNodeInfo[i].totalTime / graphTotalTime);
                    baseNodeArr[i].nodeInfoSelf = "Self time: " + fullNodeInfo[i].selfTime.toFixed(2) + "s\n";
                    baseNodeArr[i].nodeInfoWhole = "Total time: " +  fullNodeInfo[i].totalTime.toFixed(2) + "s\n";
                    var called= "Called: " + fullNodeInfo[i].called + " times";
                    if (fullNodeInfo[i].selfcalled)
                        called += " (" + fullNodeInfo[i].selfcalled + " selfcall)";
                    baseNodeArr[i].nodeInfoSelf += called;
                    baseNodeArr[i].nodeInfoWhole += called;
                    baseNodeArr[i].ifShow = 1;   
                }
                else {
                    baseNodeArr[i].ifShow = 0.2;
                    baseNodeArr[i].nodeInfoSelf = "";
                    baseNodeArr[i].nodeInfoWhole = "";
                }
                drawNodeArr.push(baseNodeArr[i]);
            }
            
            var drawEdgeArr = [];
            for (i = 0; i < baseEdgeArr.length; i++) {
                if (baseEdgeArr[i].hide == false) {
                    var estimate = "";
                    if (Math.abs(baseEdgeArr[i].validTime - fullEdgeInfo[i].time) > 1e-5)
                        estimate = "Estimated "

                    baseEdgeArr[i].calledInfo = estimate + baseEdgeArr[i].validcalled + " calls";
                    if (baseEdgeArr[i].from == baseEdgeArr[i].to) 
                    baseEdgeArr[i].calledInfo += " (self called)"; // self cycle
                    else
                        baseEdgeArr[i].calledInfo += " (" + baseEdgeArr[i].validTime.toFixed(2) + "s" + ")";
                    baseEdgeArr[i].ewidth = (maxEdgeWidth - minEdgeWidth) * (baseEdgeArr[i].validTime / graphTotalTime) + minEdgeWidth;
                    baseNodeArr[i].ifShow = 1;
                }
                else {
                    baseNodeArr[i].ifShow = 0.2;
                    baseNodeArr[i].calledInfo = "";
                }
                drawEdgeArr.push(baseEdgeArr[i]);
            }

            this.diagram.model = new go.GraphLinksModel(
                drawNodeArr,
                drawEdgeArr
            )
            this.diagram.layoutDiagram(true);
        },
        
        collapse_update: function (node_i, percent_decrease) {
            let i;

            var fullNodeInfo = this.getFullNodeInfo();
            var fullEdgeInfo = this.getFullEdgeInfo();
            var baseNodeArr = this.getBaseNodeArr();
            var baseEdgeArr = this.getBaseEdgeArr();

            for (i = 0; i < fullNodeInfo[node_i].child.length; i++) {

                let cur_child_edge_id = fullNodeInfo[node_i].child[i];
                let cur_child_id = fullEdgeInfo[cur_child_edge_id].to;

                // neglect self cycle
                if (cur_child_id == node_i)
                    continue;

                // this edge already invalid
                if (baseEdgeArr[cur_child_edge_id].hide == true)
                    continue;

                let total_time_from_this_parent = fullEdgeInfo[cur_child_edge_id].time;
                let total_node_time = fullNodeInfo[cur_child_id].totalTime;
                let total_this_parent_contribution = total_time_from_this_parent/total_node_time; // total contribution of this parent
                let child_percnet_decrease = total_this_parent_contribution * percent_decrease

                // change child percent
                baseNodeArr[cur_child_id].percent -= child_percnet_decrease;

                // contribute to node_i's time from cur_child_id's time
                baseNodeArr[cur_child_id].time -= baseEdgeArr[cur_child_edge_id].validTime * percent_decrease;
                baseNodeArr[node_i].time += baseEdgeArr[cur_child_edge_id].validTime * percent_decrease;
                
                // update edge's valid time
                // for grandchild, valid time decrease by parent collapse unknown, this is estimated 
                baseEdgeArr[cur_child_edge_id].validTime = fullEdgeInfo[cur_child_edge_id].time * baseNodeArr[node_i].percent;
                
                // update edge's valid called time
                // for grandchild, called time decrease by parent collapse unknown, this is estimated
                baseEdgeArr[cur_child_edge_id].validcalled = Math.floor(fullEdgeInfo[cur_child_edge_id].called * baseNodeArr[node_i].percent);

                /* Downside update */
                this.collapse_update(cur_child_id, child_percnet_decrease);
            }
        },

        hide_child: function(child_node, child_edge) {
            var baseNodeArr = this.getBaseNodeArr();
            var baseEdgeArr = this.getBaseEdgeArr();

            // clear valid time
            baseEdgeArr[child_edge].validTime = 0;

            // clear precision error
            baseNodeArr[child_node].time = 0;
            baseNodeArr[child_node].percent = 0;

            // hide the node
            baseNodeArr[child_node].hide = true;
            baseNodeArr[child_node].isExpanded = false;

        },

        collapse: function(node_i) {
            var fullNodeInfo = this.getFullNodeInfo();
            var fullEdgeInfo = this.getFullEdgeInfo();
            var baseNodeArr = this.getBaseNodeArr();
            var baseEdgeArr = this.getBaseEdgeArr();

            // no children to collapse
            if (fullNodeInfo[node_i].child.length == 0)
                return;

            // collapse children 
            let i;

            for (i = 0; i < fullNodeInfo[node_i].child.length; i++ ) {
                let cur_child_edge_id = fullNodeInfo[node_i].child[i];
                let cur_child_id = fullEdgeInfo[cur_child_edge_id].to;

                // neglect already hidden/invalid edge
                if (baseEdgeArr[cur_child_edge_id].hide == true)
                    continue;

                // hide this edge
                baseEdgeArr[cur_child_edge_id].hide = true;

                // neglect self-cycle
                if (cur_child_id == node_i) {
                    baseNodeArr[cur_child_id].isExpanded = false;
                    continue;
                }

                // contribute to the node's time from cur_child_id's time
                // cur_child_id's time may become negative, which would be compensated from its children
                baseNodeArr[node_i].time += baseEdgeArr[cur_child_edge_id].validTime;
                baseNodeArr[cur_child_id].time -= baseEdgeArr[cur_child_edge_id].validTime;

                // the time percentage contributed by this edge
                var percent_decrease = (fullEdgeInfo[cur_child_edge_id].time/(fullNodeInfo[cur_child_id].totalTime)) * baseNodeArr[node_i].percent;

                /* Deal with its children */

                // the child has no other parents
                if (fullNodeInfo[cur_child_id].parent.length == 1) {
                    // recursively collapse grandchild
                    this.collapse(cur_child_id);
                    
                    // decrease the percentage contributed by this edge
                    // must update percent after recursive collapse (when deleting, assume the node exist)
                    baseNodeArr[cur_child_id].percent -= percent_decrease;
                    this.hide_child(cur_child_id, cur_child_edge_id);
                    continue;
                }

                // the child has more than one parents
                baseNodeArr[cur_child_id].hide = false;

                // multi-parent, but all has been cleared up, same as only one parent
                if (Math.abs(baseNodeArr[cur_child_id].percent - percent_decrease) < 1e-5) {
                    this.collapse(cur_child_id);
                
                    // must delay decreasing percent, because delete assumes the node exist
                    baseNodeArr[cur_child_id].percent -= percent_decrease;
                    this.hide_child(cur_child_id, cur_child_edge_id);
                    continue;
                }

                // down-side update assumes a updated percent, thus must first decreasing percent
                baseNodeArr[cur_child_id].percent -= percent_decrease;
                // decrease child time contributed by this edge from the child time 
                this.collapse_update(cur_child_id, percent_decrease);


                // delete this edge
                baseEdgeArr[cur_child_edge_id].validTime = 0;

            }
        },

        expand_update: function(node_i, percent_increase) {
            var fullNodeInfo = this.getFullNodeInfo();
            var fullEdgeInfo = this.getFullEdgeInfo();
            var baseNodeArr = this.getBaseNodeArr();
            var baseEdgeArr = this.getBaseEdgeArr();

            let i;
            for (i = 0; i < fullNodeInfo[node_i].child.length; i++ ) {
                let cur_child_edge_id = fullNodeInfo[node_i].child[i];
                let cur_child_id = fullEdgeInfo[cur_child_edge_id].to;

                if (cur_child_id == node_i) 
                    continue;

                let total_time_from_parent = fullEdgeInfo[cur_child_edge_id].time;
                let total_node_time = fullNodeInfo[cur_child_id].totalTime;
                let parent_contribution = total_time_from_parent/total_node_time;
                let child_percent_increase = parent_contribution * percent_increase;

                baseNodeArr[cur_child_id].percent += child_percent_increase;

                // contribute to cur_child_id's time from node_i's time
                baseNodeArr[cur_child_id].time += fullEdgeInfo[cur_child_edge_id].time * percent_increase;
                baseNodeArr[node_i].time -= fullEdgeInfo[cur_child_edge_id].time * percent_increase;

                // update edge's valid time
                baseEdgeArr[cur_child_edge_id].validTime = fullEdgeInfo[cur_child_edge_id].time * baseNodeArr[node_i].percent;


                // already fully expand
                if (Math.abs(baseNodeArr[cur_child_id].percent - 1) < 1e-5) {
                    // clear the precision error
                    baseNodeArr[cur_child_id].percent = 1;
                    baseNodeArr[cur_child_id].time = fullNodeInfo[cur_child_id].selfTime;
                    baseEdgeArr[cur_child_edge_id].validcalled = fullEdgeInfo[cur_child_edge_id].called;
                }

                this.collapse_update(cur_child_id, child_percent_increase);
            }
        },

        expand: function(node_i) {
            var fullNodeInfo = this.getFullNodeInfo();
            var fullEdgeInfo = this.getFullEdgeInfo();
            var baseNodeArr = this.getBaseNodeArr();
            var baseEdgeArr = this.getBaseEdgeArr();

            // each time only expand one child, so would not recursively expand


            if (fullNodeInfo[node_i].child.length == 0)
                return;

            let i;

            for (i = 0; i < fullNodeInfo[node_i].child.length; i++ ) {
                let cur_child_edge_id = fullNodeInfo[node_i].child[i];
                let cur_child_id = fullEdgeInfo[cur_child_edge_id].to;

                // unhide this edge
                baseEdgeArr[cur_child_edge_id].hide = false;

                if (cur_child_id == node_i)
                    continue;

                // recover edge
                baseEdgeArr[cur_child_edge_id].validTime = baseNodeArr[node_i].percent * fullEdgeInfo[cur_child_edge_id].time;

                baseNodeArr[node_i].time -= baseEdgeArr[cur_child_edge_id].validTime;

                // the child has no other parents
                if (fullNodeInfo[cur_child_id].parent.length == 1) {
                    baseNodeArr[cur_child_id].isExpanded = false;
                    baseNodeArr[cur_child_id].percent = baseNodeArr[node_i].percent;
                    // unhide the node
                    baseNodeArr[cur_child_id].hide = false;
                    // recover the time (both child time and grandchild time because this is the leaf node)
                    baseNodeArr[cur_child_id].time += baseEdgeArr[cur_child_edge_id].validTime;
                    // not recursively expand
                    continue;
                }

                // the child has more than one parents
                // this node alredy exists, add to its valid time
                let cur_edge_time = baseEdgeArr[cur_child_edge_id].validTime;
                let full_node_time = fullNodeInfo[cur_child_id].totalTime;
                let percent_increase = cur_edge_time/full_node_time;
                // increase the percentage by the contribution of this edge
                baseNodeArr[cur_child_id].percent += percent_increase;

                // this node is recovered first time
                if (baseNodeArr[cur_child_id].hide == true) {
                    baseNodeArr[cur_child_id].isExpanded = false;
                    baseNodeArr[cur_child_id].hide = false;
                }

                // contribute to cur_child_id's time from node_i's time
                baseNodeArr[cur_child_id].time += baseEdgeArr[cur_child_edge_id].validTime;
                // if it is a leaf node, continue to dispense time
                if (baseNodeArr[cur_child_id].isExpanded)
                    this.expand_update(cur_child_id, percent_increase);
            }
            // clear precision error
            if (Math.abs(baseNodeArr[node_i].percent - 1) < 1e-5) {
                baseNodeArr[node_i].time = fullNodeInfo[node_i].selfTime;
                baseNodeArr[node_i].percent = 1;

            }
        },

        find_color: function(timePct) {
            if (timePct < 0.2)
                return "#ee9779";
            else if (timePct < 0.4)
                return "#ea7254";
            else if (timePct < 0.6)
                return "#dc4a38";
            else if (timePct < 0.8)
                return "#bb2f29";
            else
                return "#8c1a18";
        },

        expand_button: function(e, obj) {
            var node = obj.part.adornedPart;
            node.data.isExpanded = true;
            this.expand(node.data.key);
            this.updateModel();
        },

        collapse_button: function(e, obj) {
            var node = obj.part.adornedPart;
            // set parent_node.isExpanded = false
            node.data.isExpanded = false;
            this.collapse(node.data.key);
            this.updateModel();
        }
    }   
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>