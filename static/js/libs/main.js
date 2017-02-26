jQuery(document).ready(function($){
    var done = [];

    if($("#CompanyName").length != 0) {
        var cName = $("#CompanyName").text();
        $.ajax({
            type: "POST",
            url: "/companyPage",
            // The key needs to match your method's input parameter (case-sensitive).
            data: {"company": cName},
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                console.log(data);
                var emot = data["emotional"];
                var social = data["social"];
                function EmotData() {
                    var dataJson = [];
                    for(var k in emot){
                        var d = {};
                        d["label"] = k;
                        d["value"] = emot[k];
                        dataJson.push(d);
                    }
                    return dataJson;
                }

                function SocData() {
                    var dataJson = [];
                    for(var k in social){
                        var d = {};
                        d["label"] = k;
                        d["value"] = social[k];
                        dataJson.push(d);
                    }
                    return dataJson;
                }


                nv.addGraph(function() {
                    var chart = nv.models.pieChart()
                        .x(function(d) { return d.label })
                        .y(function(d) { return d.value })
                        .showLabels(true);

                    d3.select("#viz1")
                        .datum(EmotData())
                        .style("width","450px")
                        .style("height","450px")
                        .style("float","left")
                        .style("margin-top","20px")
                        .transition().duration(350)
                        .call(chart);

                    return chart;
                });

                nv.addGraph(function() {
                    var chart = nv.models.pieChart()
                        .x(function(d) { return d.label })
                        .y(function(d) { return d.value })
                        .showLabels(true);

                    d3.select("#viz2")
                        .datum(SocData())
                        .style("width","450px")
                        .style("height","450px")
                        .style("float","left")
                        .style("margin-left","140px")
                        .style("margin-top","20px")
                        .transition().duration(350)
                        .call(chart);

                    return chart;
                });

                var toolTipDiv = d3.select("#viz")
                    .append("div")
                    .attr("class", "tooltip");

                var circle = d3.select("#viz3")
                    .append("circle")
                    .attr("cx", 30)
                    .attr("cy", 30);

                if(data["sentiment_type"] == "positive"){
                    circle.style("fill","green")
                        .attr("r", data["sentiment_score"]*20)
                        .on("mouseover", function (d) {
                            d3.select(this)
                                .attr("r", data["sentiment_score"]*21);
                            toolTipDiv.transition()
                                .duration(2000)
                                .style("opacity", 0.9)
                                .style("left", (d3.event.pageX ) + "px")
                                .style("top", (d3.event.pageY ) + "px");

                            toolTipDiv.html("<p>(Sentiment: " + data["sentiment_type"] + ", " + (data["sentiment_score"]*100) + "% )</p>");
                        })
                        .on("mouseout", function (d) {
                            d3.select(this)
                                .attr("r", data["sentiment_score"]*20)
                                .style("fill", "green");
                            toolTipDiv.transition()
                                .duration(2000)
                                .style("opacity", 0);
                        })

                }else{
                    console.log("negative")
                    circle.style("fill","red")
                        .attr("r", data["sentiment_score"]*-20)
                        .on("mouseover", function (d) {
                            d3.select(this)
                                .attr("r", data["sentiment_score"]*-21);
                            toolTipDiv.transition()
                                .duration(2000)
                                .style("opacity", 0.9)
                                .style("left", (d3.event.pageX ) + "px")
                                .style("top", (d3.event.pageY ) + "px");

                            toolTipDiv.html("<p>(Sentiment: " + data["sentiment_type"] + ", " + (data["sentiment_score"]*100) + "% )</p>");
                        })
                        .on("mouseout", function (d) {
                            d3.select(this)
                                .attr("r", data["sentiment_score"]*-20)
                                .style("fill", "red");
                            toolTipDiv.transition()
                                .duration(2000)
                                .style("opacity", 0);
                        })

                }

            },
            failure: function (errMsg) {
                console.log(errMsg);
            }
        });
    }


    $.get("/getreviews", function (data,resp) {
            var reviews = data.results;
            if(!jQuery.isEmptyObject(reviews)) {
                reviews.map((d) => {
                    var review = d["content"];
                    var company = d["companyname"];
                    var date = d["date"];
                    var timeLineContent = "<div class=\"cd-timeline-block\"> <div class=\"cd-timeline-img\"> " +
                        "<img src=\"/static/img/cd-icon-picture.svg\" alt=\"Picture\"> </div> <div class=\"cd-timeline-content\"> " +
                        "<h2> <a href=\"/company?name=" + company + "\" > " +  company  + "</a> </h2> <p>" + review + "</p> " +
                        "<span class=\"cd-date\"> " + date +"</span> </div> </div>";
                    $("#cd-timeline").append(timeLineContent);

            })
            }

            var timelineBlocks = $('.cd-timeline-block'),
                offset = 0.8;

            //hide timeline blocks which are outside the viewport
            hideBlocks(timelineBlocks, offset);
            //on scolling, show/animate timeline blocks when enter the viewport
            $(window).on('scroll', function(){
                (!window.requestAnimationFrame)
                    ? setTimeout(function(){ showBlocks(timelineBlocks, offset); }, 100)
                    : window.requestAnimationFrame(function(){ showBlocks(timelineBlocks, offset); });
            });

            function hideBlocks(blocks, offset) {
                blocks.each(function(){
                    ( $(this).offset().top > $(window).scrollTop()+$(window).height()*offset ) && $(this).find('.cd-timeline-img, .cd-timeline-content').addClass('is-hidden');
                });
            }

            function showBlocks(blocks, offset) {
                blocks.each(function(){
                    ( $(this).offset().top <= $(window).scrollTop()+$(window).height()*offset && $(this).find('.cd-timeline-img').hasClass('is-hidden') ) && $(this).find('.cd-timeline-img, .cd-timeline-content').removeClass('is-hidden').addClass('bounce-in');
                });
            }
        }

    );
});