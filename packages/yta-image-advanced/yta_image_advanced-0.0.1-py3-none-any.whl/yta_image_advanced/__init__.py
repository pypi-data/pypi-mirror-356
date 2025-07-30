"""
Welcome to Youtube Autonomous Advanced Image module.

TODO: Try to apply the same 'with_' and 'apply_'
logic that in the 'yta_audio_editor' project to
keep the original image as it was or to transform
it in the instance.
"""
from yta_image_advanced.edition.filter import ImageFilter
from yta_image_advanced.edition.filter.motion_blur import MotionBlurDirection
from yta_image_advanced.description.descriptor import DefaultImageDescriptor
from yta_image_base import Image as ImageBase, _Color
from typing import Union
from PIL import Image as PillowImage


class _Transform:
    """
    Class to simplify the access to our image
    transformations for our custom Image class.
    This class must be used in our custom Image
    class.
    """

    image: any
    """
    Instance of our custom Image class to simplify
    the way we applicate transformations.
    """

    def __init__(
        self,
        image: 'Image'
    ):
        # TODO: Maybe receive the Pillow image instead (?)
        self.image = image.image

    def to_gameboy(
        self,
        output_filename: Union[str, None] = None
    ):
        return ImageFilter.to_gameboy(self.image, output_filename)
    
    def to_sticker(
        self,
        output_filename: Union[str, None] = None
    ):
        return ImageFilter.to_sticker(self.image, output_filename)
        
class _Filter:
    """
    Class to simplify the access to our filters 
    for our custom Image class. This class must
    be used in our custom Image class.
    """

    image: any
    """
    Instance of our custom Image class to simplify
    the way we applicate filters.
    """

    def __init__(
        self,
        image: 'Image'
    ):
        # TODO: Maybe receive the Pillow image instead (?)
        self.image = image.image

    def pixelate(
        self,
        pixel_size: int,
        output_filename: Union[str, None] = None
    ):
        return ImageFilter.pixelate(self.image, pixel_size, output_filename)

    def motion_blur(
        self,
        kernel_size: int = 30,
        direction: MotionBlurDirection = MotionBlurDirection.HORIZONTAL,
        output_filename: Union[str, None] = None
    ):
        return ImageFilter.motion_blur(self.image, kernel_size, direction, output_filename)
    
class Image:
    """
    You can access to the transformations by simply
    using the '.filter' and '.transform' properties.

    TODO: Write
    """

    @property
    def as_pillow(
        self
    ) -> PillowImage.Image:
        return self.image.as_pillow
    
    @property
    def as_numpy(
        self
    ) -> 'np.ndarray':
        return self.image.as_numpy
    
    @property
    def as_opencv(
        self
    ) -> 'np.ndarray':
        return self.image.as_opencv
    
    @property
    def as_base64(
        self
    ) -> str:
        return self.image.as_base64
    
    # TODO: This must be moved to an AI-related module
    @property
    def description(
        self
    ) -> str:
        """
        A description of the image, given by an engine that
        has been trained to describe images.
        """
        if not hasattr(self, '_description'):
            self._description = DefaultImageDescriptor().describe(self.image)

        return self._description

    @property
    def green_regions(
        self
    ):
        """
        The green regions that have been found in the image.
        This method will make a search the fist time it is
        accessed.
        """
        return self.image.green_regions

    @property
    def alpha_regions(
        self
    ):
        """
        The alpha (transparent) regions that have been found
        in the image. This method will make a search the
        first time it is accessed.
        """
        return self.image.alpha_regions

    def __init__(
        self,
        image: Union[
            str,
            'np.ndarray',
            PillowImage.Image
        ]
    ):
        self.image = ImageBase(image)
        self.color: _Color = self.image.color
        """
        A shortcut to the available color changes. The
        color changes, once they are applied, return a new
        image. The original image remains unchanged.
        """
        self.transform: _Transform = _Transform(self)
        """
        A shortcut to the available transformations. The
        transformations, once they are applied, return a
        new image. The original image remains unchanged.
        """
        self.filter: _Filter = _Filter(self)
        """
        A shortcut to the available filters. The filters,
        once they are applied, return a new image. The
        original image remains unchanged.
        """

    def resize(
        self,
        size: tuple
    ):
        """
        This method returns the image modified but
        does not modify the original image.
        """
        # TODO: Do not use 'FileReturn.file_converted'
        return self.image.resize(size).file_converted
    
    def remove_background(
        self
    ):
        """
        Remove the background of the image.
        """
        # TODO: Do not use 'FileReturn.file_converted'
        return self.image.remove_background().file_converted
    
    # TODO: Modify to work with '.apply' and '.with'
    # methods, and implement the use of the things
    # that the 'ImageEditor' class is able to 
    # modify

        