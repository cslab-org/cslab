    //var e = document.getElementById('thumbnail')
    //e.innerHTML = "<img src='Kerala.png'>";
    var width = document.getElementById('svgcanvas').clientWidth,
        height = document.getElementById('svgcanvas').clientHeight,
        textWidth = 80,
        margin = {left:50+textWidth, right:50+textWidth , top:30, bottom:50},
        
        //colors = d3.scale.category10(),
        y = d3.scale.linear() // <-A
            .domain([0, 60000])
            .range([height-margin.bottom, margin.top]);
       
    
    var data = { '2014': [ 
            49111, 45171, 28614, 22592, 22095, 18066, 15713, 7859
        ],

        '2015': [
            54298, 46946, 24760, 22166, 26983, 18397, 19809, 8749
        ],

        'teams': [
            'Kerala', 'Kolkata', 'North-East', 'Mumbai', 'Chennai', 'Goa', 'Delhi', 'Pune'
        ],

        'names': [
            'Kerala Blasters', 'Atletico de Kolkata', 'North East United', 'Mumbai FC',
            'Chennayin FC', 'FC Goa', 'Delhi Dynamos', 'Pune FC'] };

    var tip = d3.tip()
      .attr('class', 'd3-tip')
      .offset([-10, 0])
      .html(function(d, i) {
        return ("<img class='thumbnail' src=/static/demo/isl/"+d+".png>" + 
                "<div class='team-tooltip'>" +
                    "<div class='team-tooltip-header'>"+data['names'][i]+"</div>" +
                    "<div class='team-tooltip-stat'><i>2014</i>: "+data['2014'][i]+"</div>" +
                    "<div class='team-tooltip-stat'><i>2015</i>: "+data['2015'][i]+"</div>" +
                "</div>");
      })    
    
    /*var line = d3.svg.line() // <-D
            .x(function(d){return x(d.x);})
            .y(function(d){return y(d.y);});
      */  
    var svg = d3.select("#svgcanvas").append("svg");
    
    svg.attr("height", height)
        .attr("width", width);
        
     /*svg.selectAll("path")
            .data(data)
        .enter()
            .append("path") // <-E
            .attr("class", "line")            
            .attr("d", function(d){return line(d);}); // <-F
       */     
    
    renderLines(svg);
    svg.call(tip);
       
    renderDots(svg, data['2014'], 0);
    renderDots(svg, data['2015'], 1);

    renderTextRight(svg);
    renderTextLeft(svg);
    renderConnectingLinesRight(svg);
    renderConnectingLinesLeft(svg);
       
    renderAxes(svg);

    // Y-axis Label - Avg #people in home ground
    /*svg.append("text") 
                .text('Avg # people for home matches')
                .attr('class', 'label')
                .attr('x', -(height-margin.bottom)/2)
                .attr('y', textWidth/2+20) 
                .attr('text-anchor', 'middle')
                .attr("transform", "rotate(-90)")
    */
    // Labels 2014 and 2015
    svg.append("text") 
                .text('2014')
                .attr('class', 'label-header')
                .attr('x', margin.left)
                .attr('y', height - margin.bottom + 30) 
                .attr('text-anchor', 'middle')
                
    svg.append("text") 
                .text('2015')
                .attr('class', 'label-header')
                .attr('x', width - margin.right)
                .attr('y', height - margin.bottom + 30) 
                .attr('text-anchor', 'middle')
                

    function renderLines(svg) {

        svg.append("g").selectAll("line.line")
            .data(data['teams'])
            .enter()
                .append("line")
                .attr("class", "line")
                .attr('x1', margin.left)
                .attr('y1', function(d, i) {
                    return y(data['2014'][i]);
                })
                .attr('x2', (width-margin.right))
                .attr('y2', function(d, i) {
                    return y(data['2015'][i]);
                })
                .style("stroke", function (d, i) { 
                    if (data['2014'][i] > data['2015'][i])
                        return 'red';
                    else
                        return 'steel blue';
                })
                .on('mouseover', tip.show)
                .on('mouseout', tip.hide)
                //.append("svg:title")
                //.text(function(d) { return d; })
                
                
    }

    
    function renderConnectingLinesRight(svg) {

        svg.append("g").selectAll("line.connecting-line")
            .data(data['teams'])
            .enter()
                .append("line")
                .attr("class", "connecting-line")
                .attr('x1', width - margin.right)
                .attr('y1', function(d, i) {
                    return y(data['2015'][i]);
                })
                .attr('x2', (width-margin.right+50))
                .attr('y2', function(d, i) {
                    return y(data['2015'][i]);
                })
    }

    function renderConnectingLinesLeft(svg) {

        svg.append("g").selectAll("line.connecting-line")
            .data(data['teams'])
            .enter()
                .append("line")
                .attr("class", "connecting-line")
                .attr('x1', textWidth)
                .attr('y1', function(d, i) {
                    if (i==4) // avoid overlap
                        return y(data['2014'][i]) + 10;    
                    return y(data['2014'][i]);
                })
                .attr('x2', (margin.left))
                .attr('y2', function(d, i) {
                    return y(data['2014'][i]);
                })
    }

    function renderTextRight(svg) {

        svg.append("g").selectAll("text.right")
            .data(data['teams'])
            .enter().append("text") 
                .text(function(d) {
                    return d;
                })
                .attr('class', 'right')
                .attr('x', width-margin.right)
                .attr('y', function(d, i) {
                    return y(data['2015'][i]);
                }) 
                .attr("dy", ".25em")
                .style("font-size", "12px")
                .attr('height', 20)
                .attr('width', 50)
                .attr("transform", function(){
                  return "translate(" + 50 
                    + ", 0)";
                })
        
    }

    function renderTextLeft(svg) {

        svg.selectAll("text.left")
            .data(data['teams'])
            .enter().append("text") 
                .text(function(d) {
                    return d;
                })
                .attr('class', 'left')
                .attr('x', margin.left)
                .attr('y', function(d, i) {
                    if (i==4) // avoid overlap
                        return y(data['2014'][i]) + 10;    
                    return y(data['2014'][i]);
                }) 
                .attr("dy", ".25em")
                .attr('text-anchor', 'end')
                .style("font-size", "12px")
                .attr('height', 20)
                .attr('width', 50)
                .attr("transform", function(){
                  return "translate(" + (-50) 
                    + ", 0)";
                })
        
    }

    function renderDots(svg, data, x) { // <-B
        var kind = '.circle0',
            x_offset = margin.left;
        if (x) {
            kind = '.circle1';
            x_offset = width - margin.right;
        }

        
        svg.append("g").selectAll("circle"+kind)
            .data(data)
            .enter().append("circle") // <-C
                .attr("class", kind+" dot")
                .attr("cx", x_offset)
                .attr("cy", function(d) { return y(d); })
                .attr("r", 4.5);
        
    }

    function renderAxes(svg){ // <-G
                
        var y14Axis = d3.svg.axis()
                .scale(y)
                .orient("left");
        
        svg.append("g")        
            .attr("class", "axis")
            .attr("transform", function(){
                return "translate(" + margin.left 
                    + ", 0)";
            })
            .call(y14Axis);

        var y15Axis = d3.svg.axis()
                .scale(y)
                .orient("right");
        
        svg.append("g")        
            .attr("class", "axis")
            .attr("transform", function(){
                return "translate(" + (width - margin.right) 
                    + ", 0)";
            })
            .call(y15Axis);
        
    
    }
        
    