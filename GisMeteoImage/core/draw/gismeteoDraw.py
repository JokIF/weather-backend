from GisMeteoImage.core.classes import Manual, ManualData
from GisMeteoImage.core.draw.drawer import BaseDrawer
from GisMeteoImage.core.draw.mixins import ICON_ACTION, TEXT_ACTION


class GismeteoDrawer(BaseDrawer):
    MANUAL = Manual(
        (
            (
                ManualData(
                    ICON_ACTION,
                    "icon",
                    (619, 326),
                    {"end_coords": (808, 515), "image_size": (189, 189)}
                ),
                ManualData(
                    TEXT_ACTION,
                    "city",
                    (570, 204),
                    {"font_size": 36, "fill": "black", "anchor": "mt"}
                ),
                ManualData(
                    TEXT_ACTION,
                    "temperature",
                    (619, 348),
                    {"font_size": 165, "fill": "black", "anchor": "rt"}
                ),
                ManualData(
                    TEXT_ACTION,
                    "humidity", #добавить %
                    (340, 637),
                    {"font_size": 30, "fill": "black", "anchor": "mt"}
                ),
                ManualData(
                    TEXT_ACTION,
                    "pressure",
                    (530, 637),
                    {"multiline": True, "font_size": 30, "fill": "black", "align": "center", "anchor": "ma"}
                ),
                ManualData(
                    TEXT_ACTION,
                    "wind",
                    (740, 637),
                    {"multiline": True, "font_size": 30, "fill": "black", "align": "center", "anchor": "ma"}
                ),
                ManualData(
                    TEXT_ACTION,
                    "time",
                    (986, 96),
                    {"font_size": 26, "fill": "black", "anchor": "rb"}
                ),
                ManualData(
                    TEXT_ACTION,
                    "month",
                    (986, 136),
                    {"font_size": 26, "fill": "black", "anchor": "rb"}
                ),
                ManualData(
                    TEXT_ACTION,
                    "weekday",
                    (986, 176),
                    {"font_size": 26, "fill": "black", "anchor": "rb"}
                ),
            ),
            (
                ManualData(
                   TEXT_ACTION,
                   "time",
                   (358, 825),
                   {"font_size": 36, "fill": "black", "anchor": "mb"} 
                ),
                ManualData(
                    TEXT_ACTION,
                    "temperature",
                    (358, 991),
                    {"font_size": 36, "fill": "black", "anchor": "mt"}
                ),
                ManualData(
                    ICON_ACTION,
                    "icon",
                    (275, 825),
                    {"end_coords": (441, 991), "image_size": (166, 166)}
                )
            ),
            (
                ManualData(
                   TEXT_ACTION,
                   "time",
                   (530, 825), # +172 0
                   {"font_size": 36, "fill": "black", "anchor": "mb"} 
                ),
                ManualData(
                    TEXT_ACTION,
                    "temperature",
                    (530, 991),
                    {"font_size": 36, "fill": "black", "anchor": "mt"}
                ),
                ManualData(
                    ICON_ACTION,
                    "icon",
                    (447, 825),
                    {"end_coords": (613, 991), "image_size": (166, 166)}
                )
            ),
            (
                ManualData(
                   TEXT_ACTION,
                   "time",
                   (702, 825), # +344 0
                   {"font_size": 36, "fill": "black", "anchor": "mb"} 
                ),
                ManualData(
                    TEXT_ACTION,
                    "temperature",
                    (702, 991),
                    {"font_size": 36, "fill": "black", "anchor": "mt"}
                ),
                ManualData(
                    ICON_ACTION,
                    "icon",
                    (619, 825),
                    {"end_coords": (785, 991), "image_size": (166, 166)}
                )
            )
        )
    )