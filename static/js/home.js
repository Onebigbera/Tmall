$(function () {

    $('.category_menu_item').mouseover(function () {
        // 隐藏所有二级子菜单
        $('.category_sub').hide();
        $(this).next().show();
    });
    $('.category_menu').mouseleave(function () {
        // 隐藏所有二级子菜单
        $('.category_sub').hide();
    });

    $('#banner').unslider({auto: true, dots: true});

    $('.selected').click(function () {
        $(this).toggle();
        $('.shop_review_wrap').toggle()
    });

    $('.detail_review_link').click(function () {
        $(this).toggle();
        $('.shop_param_part_warp').toggle()
    })
});

