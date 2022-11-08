import logging
import json
from flask_admin import expose
from flask import current_app, request
from flask_restful import Api, Resource
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Pie, Tab, Bar3D
from pyecharts.commons.utils import JsCode
from app import db
from app.utils import YamlLoader
from . import api_bp

logger = logging.getLogger()
api = Api()

"""统一图标风格"""
general_chart_style = {
    'colors': ['#00CC99', 'darkgray'],
    'notes': '说明：当前统计数据来源信息'
}

"""
routes & functions
"""


@api_bp.route('/general_pies')
def get_general_pies():
    window_width = request.args.get('w') or 1
    is_simple: bool = True
    if int(window_width) > 767:
        is_simple = False

    data = get_general_pies_data()
    c = draw_general_pies(data, is_simple)
    return c.dump_options_with_quotes()


common_graphic_opts = opts.GraphicGroup(
    graphic_item=opts.GraphicItem(bounding="raw", left=110, bottom=10, z=100),
    children=[
        # opts.GraphicRect(
        #     graphic_item=opts.GraphicItem(left='center', top='center', z=100,),
        #     graphic_shape_opts=opts.GraphicShapeOpts(width=400, height=50),
        #     graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(fill='rgba(0,0,0,0.3)')
        # ),
        opts.GraphicText(
            graphic_item=opts.GraphicItem(left='left', top='bottom', z=100, ),
            graphic_textstyle_opts=opts.GraphicTextStyleOpts(text=general_chart_style['notes'], font='12px sans-serif')
        ),
    ]
)


def get_general_pies_data():
    return {'a_list': [500, 2000], 'b_list': [300, 1200]}


def draw_general_pies(data, is_simple: False) -> Pie:
    a_list = data.get('a_list')
    b_list = data.get('b_list')
    rate_a = round((a_list[0] / (a_list[0] + a_list[1])) * 100, 1)
    rate_b = round((b_list[0] / (b_list[0] + b_list[1])) * 100, 1)
    all_list = [a_list[0] + b_list[0], a_list[1] + b_list[1]]
    rate_all = round((all_list[0] / (all_list[0] + all_list[1])) * 100, 1)
    total_a = round((a_list[0] + a_list[1]), 1)
    total_b = round((b_list[0] + b_list[1]), 1)
    total_all = round(total_a + total_b, 1)
    if is_simple:
        pie = Pie().add(
            "",
            [list(z) for z in zip(["已完成", "待完成"], all_list)],
            center=["50%", "50%"],
            radius=[60, 100],
            label_opts=opts.LabelOpts(formatter=f"整体 {rate_all}%\n合计：{total_all}件", position="left"),
        ).set_global_opts(
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="5%", pos_left="75%", orient="vertical"
            ),
            graphic_opts=common_graphic_opts,
        ).set_colors(general_chart_style['colors']).add_js_funcs()

    else:
        pie = Pie().add(
            "",
            [list(z) for z in zip(["已完成", "待完成"], all_list)],
            center=["15%", "30%"],
            radius=[60, 100],
            label_opts=opts.LabelOpts(formatter=f"整体 {rate_all}%\n合计：{total_all}件", position="left"),
        ).add(
            "",
            [list(z) for z in zip(["已完成", "待完成"], a_list)],
            center=["35%", "30%"],
            radius=[60, 80],
            label_opts=opts.LabelOpts(formatter=f"A类 {rate_a}%\n总计：{total_a}件", position="bottom"),
        ).add(
            "",
            [list(z) for z in zip(["已完成", "待完成"], b_list)],
            center=["55%", "30%"],
            radius=[60, 80],
            label_opts=opts.LabelOpts(formatter=f"B类 {rate_b}%\n总计：{total_b}件", position="bottom"),
        ).set_global_opts(
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="5%", pos_left="75%", orient="vertical"
            ),
            graphic_opts=common_graphic_opts,
        ).set_colors(general_chart_style['colors']).add_js_funcs()

    return pie
