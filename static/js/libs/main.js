jQuery(document).ready(function($){

    $.ajax({
        url: '/getreviews',
        type: 'GET',
        dataType: 'json',

        success: function (data) {

            if(!jQuery.isEmptyObject(data)) {
                data.map((d) => {
                    var review = d["content"];
                    var company = d["company_id"];
                    var date = d["date"];
                    var timeLineContent = "<div class=\"cd-timeline-block\"> <div class=\"cd-timeline-img\"> " +
                        "<img src=\"/static/img/cd-icon-picture.svg\" alt=\"Picture\"> </div> <div class=\"cd-timeline-content\"> " +
                        "<h2>" + company + "</h2> <p>" + review + "</p> <a href=\"#0\" class=\"cd-read-more\">Read more</a> " +
                        "<span class=\"cd-date\"> " + date +"</span> </div> </div>";
                    $("#cd-timeline").append("");
            });
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

    });
});