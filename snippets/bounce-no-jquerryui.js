// Jquerry bounce without jquerry UI available

$(document).ready(function() {
    bounce($(".header-chevron"), 9999, '10px', 500);
});


function bounce(element, times, distance, speed) {
    for(i = 0; i < times; i++) {
        element.animate({marginTop: '-='+distance},speed)
            .animate({marginTop: '+='+distance},speed);
    }
}
