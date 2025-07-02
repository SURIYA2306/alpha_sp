// Init
var $ = jQuery;

$(document).ready(function() {
    var animationTime = 6,
        days = 7;

    $('#progress-time-fill, #death-group').css({ 'animation-duration': animationTime + 's' });

    function timer(totalTime, deadline) {
        var time = totalTime * 1000;
        var dayDuration = time / deadline;
        var actualDay = deadline;
        var timer = setInterval(countTime, dayDuration);

        function countTime() {
            --actualDay;
            $('.deadline-days .day').text(actualDay);
            if (actualDay == 0) {
                clearInterval(timer);
                $('.deadline-days .day').text(deadline);
            }
        }
    }

    var deadlineText = function() {
        var $el = $('.deadline-days');
        var html = '<div class="mask-red"><div class="inner">' + $el.html() + '</div></div><div class="mask-white"><div class="inner">' + $el.html() + '</div></div>';
        $el.html(html);
    }

    deadlineText();
    timer(animationTime, days);
});
// Hide loader after 6 seconds (6000ms)
setTimeout(function() {
    $('#deadline').addClass('hidden');
}, 6000);