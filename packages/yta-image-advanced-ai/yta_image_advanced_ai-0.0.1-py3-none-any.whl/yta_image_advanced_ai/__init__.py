from yta_image_advanced_ai.descriptor import DefaultImageDescriptor
from yta_image_advanced import Image as AdvancedImage


class Image(AdvancedImage):
    """
    Advanced Image class that includes AI-related
    functionality.
    """

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

    def some_ai_functionality(
        self
    ):
        """
        TODO: Just for testing
        """
        return self.image