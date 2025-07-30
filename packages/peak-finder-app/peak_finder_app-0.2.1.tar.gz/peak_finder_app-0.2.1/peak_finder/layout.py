# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Copyright (c) 2024-2025 Mira Geoscience Ltd.                                     '
#                                                                                   '
#  This file is part of peak-finder-app package.                                    '
#                                                                                   '
#  peak-finder-app is distributed under the terms and conditions of the MIT License '
#  (see LICENSE file at the root of this source code package).                      '
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#
#  This file is part of peak-finder-app.
#
#  All rights reserved.

from __future__ import annotations

import dash_daq as daq
from dash import dcc, html


trigger_run_layout = html.Div(
    id="data_selection",
    children=[
        dcc.Checklist(
            id="trend_lines",
            options=[{"label": "Create trend lines", "value": True}],
        ),
        html.Div(
            [
                dcc.Markdown(
                    "Save as", style={"width": "75%", "display": "inline-block"}
                ),
                dcc.Input(
                    id="ga_group_name",
                    style={"width": "75%", "display": "inline-block"},
                ),
            ]
        ),
        html.Button("Export", id="export"),
        dcc.Markdown(id="output_message"),
    ],
    style={
        "display": "inline-block",
        "vertical-align": "top",
        "margin-bottom": "20px",
    },
)


group_settings_layout = html.Div(
    [
        html.Div(
            id="color_picker_div",
            children=[
                dcc.Markdown(
                    children="Group Name",
                    style={
                        "width": "30%",
                        "display": "inline-block",
                    },
                ),
                dcc.Dropdown(
                    id="group_name",
                    options=[],
                    style={
                        "width": "70%",
                        "display": "inline-block",
                    },
                ),
                daq.ColorPicker(  # pylint: disable=not-callable
                    id="color_picker",
                    value={"hex": "#000000"},
                    style={
                        "width": "225px",
                        "margin-left": "22%",
                    },
                ),
            ],
        ),
    ],
    style={
        "vertical-align": "top",
    },
)


export_layout = html.Div(
    [
        html.Div(
            [
                dcc.Markdown(
                    "Save as", style={"width": "25%", "display": "inline-block"}
                ),
                dcc.Input(
                    id="ga_group_name",
                    style={"width": "25%", "display": "inline-block"},
                ),
            ]
        ),
        html.Div(
            [
                dcc.Markdown(
                    children="Output path",
                    style={"width": "25%", "display": "inline-block"},
                ),
                dcc.Input(
                    id="monitoring_directory",
                    style={
                        "width": "50%",
                        "display": "inline-block",
                        "margin_bottom": "20px",
                    },
                ),
            ]
        ),
        dcc.Checklist(
            id="live_link",
            options=[{"label": "Geoscience ANALYST Pro - Live link", "value": True}],
            value=[],
            style={"margin_bottom": "20px"},
        ),
        html.Button("Export", id="export"),
        dcc.Markdown(id="output_message"),
    ]
)


figure_layout = html.Div(
    children=[
        dcc.Loading(
            id="line_loading",
            type="default",
            children=html.Div(dcc.Graph(id="line_figure")),
        ),
        dcc.Loading(
            id="full_lines_loading",
            type="default",
            children=html.Div(dcc.Graph(id="survey_figure")),
        ),
    ],
)


launch_qt_layout = html.Div(
    [
        html.Div(
            [
                html.Button("Launch App", id="launch_app", n_clicks=0),
                dcc.Markdown(
                    children="",
                    id="launch_app_markdown",
                    style={"width": "50%", "display": "inline-block"},
                ),
            ],
            style={"margin_top": "40px"},
        ),
        dcc.Store(id="ui_json_data"),
    ]
)


visual_params_layout = html.Div(
    id="visual_params",
    children=[
        html.Div(
            [
                dcc.Markdown(
                    children="N outward lines",
                    style={
                        "width": "30%",
                        "display": "inline-block",
                    },
                ),
                dcc.Input(
                    id="n_lines",
                    type="number",
                    min=0,
                    step=1,
                    value=1,
                    style={
                        "width": "49%",
                        "display": "inline-block",
                    },
                ),
            ]
        ),
        html.Div(
            [
                dcc.Markdown(
                    children="X-axis Label",
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "vertical-align": "middle",
                    },
                ),
                dcc.Dropdown(
                    id="x_label",
                    options=["Distance", "Easting", "Northing"],
                    style={
                        "width": "70%",
                        "display": "inline-block",
                        "vertical-align": "middle",
                    },
                    value="Distance",
                ),
            ],
            style={"margin-bottom": "10px"},
        ),
        html.Div(
            [
                dcc.Markdown(
                    children="Y-axis Scaling",
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "vertical-align": "middle",
                    },
                ),
                dcc.Dropdown(
                    id="y_scale",
                    options=["linear", "symlog"],
                    style={
                        "width": "70%",
                        "display": "inline-block",
                        "vertical-align": "middle",
                    },
                    value="symlog",
                ),
            ],
            style={"margin-bottom": "10px"},
        ),
        dcc.Markdown(
            children="Linear threshold",
            style={"width": "30%", "display": "inline-block", "vertical-align": "top"},
        ),
        html.Div(
            [
                dcc.Slider(
                    id="linear_threshold",
                    min=-10,
                    max=10,
                    step=0.1,
                    marks={
                        -10: "10E-10",
                        -5: "10E-5",
                        0: "1",
                        5: "10E5",
                        10: "10E10",
                    },
                    value=-3.8,
                ),
            ],
            style={
                "width": "70%",
                "display": "inline-block",
                "vertical-align": "top",
                "margin-bottom": "10px",
            },
        ),
        dcc.Checklist(
            id="show_residuals",
            options=[{"label": "Plot residuals", "value": True}],
        ),
        dcc.Checklist(
            id="structural_markers",
            options=[{"label": "Plot markers", "value": True}],
        ),
        dcc.Checklist(
            id="color_picker_visibility",
            options=[{"label": "Select group colours", "value": True}],
            style={"width": "100%"},
        ),
        group_settings_layout,
    ],
    style={
        "display": "inline-block",
        "vertical-align": "top",
    },
)


detection_params_layout = html.Div(
    id="detection_params",
    children=[
        html.Div(
            [
                dcc.Markdown(
                    children="Line ID:",
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "vertical-align": "middle",
                    },
                ),
                dcc.Dropdown(
                    id="selected_line",
                    options=[],
                    style={
                        "width": "70%",
                        "display": "inline-block",
                        "vertical-align": "middle",
                    },
                ),
            ],
            style={"margin-bottom": "20px"},
        ),
        html.Div(
            [
                dcc.Markdown(
                    children="Masking Data",
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "vertical-align": "middle",
                    },
                ),
                dcc.Dropdown(
                    id="masking_data",
                    style={
                        "width": "70%",
                        "display": "inline-block",
                        "vertical-align": "middle",
                    },
                ),
            ],
            style={"margin-bottom": "20px"},
        ),
        dcc.Markdown(
            children="Smoothing",
            style={"width": "30%", "display": "inline-block", "vertical-align": "top"},
        ),
        html.Div(
            [
                dcc.Slider(
                    id="smoothing",
                    min=0,
                    max=64,
                    step=1,
                    marks=None,
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True,
                    },
                ),
            ],
            style={
                "width": "70%",
                "display": "inline-block",
                "vertical-align": "top",
                "margin-bottom": "10px",
            },
        ),
        dcc.Markdown(
            children="Minimum Amplitude (%)",
            style={"width": "30%", "display": "inline-block", "vertical-align": "top"},
        ),
        html.Div(
            [
                dcc.Slider(
                    id="min_amplitude",
                    min=0.0,
                    max=100.0,
                    step=0.1,
                    marks=None,
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True,
                    },
                ),
            ],
            style={
                "width": "70%",
                "display": "inline-block",
                "vertical-align": "top",
                "margin-bottom": "10px",
            },
        ),
        html.Div(
            [
                dcc.Markdown(
                    children="Minimum Data Value",
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "vertical-align": "middle",
                    },
                ),
                dcc.Input(
                    id="min_value",
                    type="number",
                    style={
                        "width": "70%",
                        "display": "inline-block",
                        "vertical-align": "middle",
                    },
                ),
            ],
            style={"margin-bottom": "10px"},
        ),
        dcc.Markdown(
            children="Minimum Width (m)",
            style={"width": "30%", "display": "inline-block", "vertical-align": "top"},
        ),
        html.Div(
            [
                dcc.Slider(
                    id="min_width",
                    min=1,
                    max=1000,
                    step=1,
                    marks=None,
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True,
                    },
                ),
            ],
            style={
                "width": "70%",
                "display": "inline-block",
                "vertical-align": "top",
                "margin-bottom": "10px",
            },
        ),
        dcc.Markdown(
            children="Max Peak Migration",
            style={"width": "30%", "display": "inline-block", "vertical-align": "top"},
        ),
        html.Div(
            [
                dcc.Slider(
                    id="max_migration",
                    min=1,
                    max=1000,
                    step=1,
                    marks=None,
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True,
                    },
                ),
            ],
            style={
                "width": "70%",
                "display": "inline-block",
                "vertical-align": "top",
                "margin-bottom": "10px",
            },
        ),
        dcc.Markdown(
            children="Minimum # Channels",
            style={"width": "30%", "display": "inline-block", "vertical-align": "top"},
        ),
        html.Div(
            [
                dcc.Slider(
                    id="min_channels",
                    min=1,
                    max=10,
                    step=1,
                    marks=None,
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True,
                    },
                ),
            ],
            style={
                "width": "70%",
                "display": "inline-block",
                "vertical-align": "top",
                "margin-bottom": "10px",
            },
        ),
        html.Div(
            [
                dcc.Markdown(
                    children="Merge N Peaks",
                    style={
                        "width": "30%",
                        "display": "inline-block",
                    },
                ),
                dcc.Input(
                    id="n_groups",
                    value=1,
                    type="number",
                    debounce=True,
                    style={
                        "width": "70%",
                        "display": "inline-block",
                    },
                ),
                dcc.Markdown(
                    children="Max Group Separation",
                    style={
                        "width": "30%",
                        "display": "inline-block",
                    },
                ),
                dcc.Input(
                    id="max_separation",
                    value=100,
                    type="number",
                    debounce=True,
                    style={
                        "width": "70%",
                        "display": "inline-block",
                    },
                ),
                dcc.Checklist(
                    id="flip_sign",
                    options=[{"label": "Flip Y (-1x)", "value": True}],
                ),
            ]
        ),
    ],
    style={
        "display": "inline-block",
        "vertical-align": "top",
    },
)


stored_params_layout = html.Div(
    [
        dcc.Store(id=label, data=0)
        for label in [
            "survey_trigger",
            "line_indices_trigger",
            "lines_computation_trigger",
            "figure_lines_trigger",
            "figure_markers_trigger",
            "figure_residuals_trigger",
            "figure_colours_trigger",
            "figure_click_data_trigger",
        ]
    ]
)


peak_finder_layout = html.Div(
    [
        dcc.Markdown(
            children="#### Peak Finder",
            style={"margin-bottom": "20px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            options=["Line figure", "Survey figure"],
                            multi=True,
                            id="figure_selection",
                            value=["Line figure"],
                            style={"width": "50%"},
                        ),
                        figure_layout,
                    ],
                    style={"width": "70%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            options=[
                                "Detection parameters",
                                "Visual parameters",
                            ],
                            id="widget_selection",
                            value="Detection parameters",
                            style={"width": "70%", "margin-bottom": "20px"},
                        ),
                        visual_params_layout,
                        detection_params_layout,
                    ],
                    style={"width": "30%", "display": "inline-block"},
                ),
            ],
        ),
        trigger_run_layout,
        stored_params_layout,
    ],
)


workspace_layout = html.Div(
    [
        dcc.Upload(
            id="upload",
            children=html.Button("Upload Workspace/ui.json"),
            style={"margin_bottom": "40px"},
        ),
        html.Div(
            [
                dcc.Markdown(
                    children="Object:",
                    style={
                        "width": "20%",
                        "display": "inline-block",
                        "margin-top": "20px",
                        "vertical-align": "bottom",
                    },
                ),
                dcc.Dropdown(
                    id="objects",
                    style={
                        "width": "65%",
                        "display": "inline-block",
                        "margin_bottom": "40px",
                        "vertical-align": "bottom",
                    },
                ),
            ]
        ),
    ]
)


object_selection_layout = html.Div([workspace_layout, launch_qt_layout])
