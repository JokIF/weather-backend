from PIL.ImageFont import FreeTypeFont
from PIL.ImageDraw import ImageDraw
from PIL.Image import Image, open as ImageOpen


TEXT_ACTION = "action_text"
ICON_ACTION = "action_icon"

class TextDrawMixin:
    def action_text(self, 
                    content: str, 
                    frame: ImageDraw,
                    coords: tuple[int, int], 
                    font: FreeTypeFont,
                    **kwargs
                    ):
        content = str(content)
        text_func = frame.multiline_text if kwargs.pop("multiline", None) else frame.text
        text_func(
            xy=coords,
            text=content,
            font=font,
            **kwargs
        )


class IconDrawMixin:
    def action_icon(self, 
                    content: str, 
                    frame: ImageDraw,
                    coords: tuple[int, int], 
                    font: FreeTypeFont,
                    **kwargs
                    ):
        icon = ImageOpen(fp=content)
        end_coords = kwargs.pop("end_coords")
        box = (*coords, *end_coords)
        image_size = kwargs.pop("image_size")
        if image_size:
            icon = icon.resize(size=image_size)

        frame._image.paste(
            im=icon,
            box=box,
            **kwargs
        )
        icon.close()


class BaseDrawMixin(TextDrawMixin, IconDrawMixin):
    pass
