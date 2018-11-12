$(function () {
    $('.selected').click(function () {
        $('.shop_review_wrap').hide();
        $('.shop_param_part_warp').show();
    });

    $('.detail_review_link').click(function () {
        $('.shop_review_wrap').show();
        $('.shop_param_part_warp').hide();
    })
});

