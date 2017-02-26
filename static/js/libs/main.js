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
                function exampleData() {
                    return  [
                        {
                            "label": "One",
                            "value" : 29.765957771107
                        } ,
                        {
                            "label": "Two",
                            "value" : 0
                        } ,
                        {
                            "label": "Three",
                            "value" : 32.807804682612
                        } ,
                        {
                            "label": "Four",
                            "value" : 196.45946739256
                        } ,
                        {
                            "label": "Five",
                            "value" : 0.19434030906893
                        } ,
                        {
                            "label": "Six",
                            "value" : 98.079782601442
                        } ,
                        {
                            "label": "Seven",
                            "value" : 13.925743130903
                        } ,
                        {
                            "label": "Eight",
                            "value" : 5.1387322875705
                        }
                    ];
                }


                nv.addGraph(function() {
                    var chart = nv.models.pieChart()
                        .x(function(d) { return d.label })
                        .y(function(d) { return d.value })
                        .showLabels(true);

                    d3.select("#chart svg")
                        .datum(exampleData())
                        .transition().duration(350)
                        .call(chart);

                    return chart;
                });
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