# when a user takes a picture of a prescription, we need to extract the following information:
# - family_member_prescription_is_for
# - medication_name
# - medication_dosage
# - medication_frequency
# - medication_start_date
# - medication_end_date
# - medication_notes
# - medication_refills_left
# - medication_refills_needed

from pydantic_ai import ImageUrl
import base64
from dataclasses import dataclass


@dataclass
class PrescriptionLableExtraction:
    ...


async def read_label_medication_bottle() -> ImageUrl:
    """
    Read the label on a medication bottle and return the text
    """
    # image_path = '/Users/msmay/Documents/repos/family-med-nanny/slack_to_fastapi/prescription_bottle_one.jpg'
    image_path = '/Users/msmay/Documents/repos/family-med-nanny/slack_to_fastapi/prescription_bottle_two.jpg'
    with open(image_path, 'rb') as image_file:
        b64_image = base64.b64encode(image_file.read()).decode('utf-8')

    return ImageUrl(url=f'data:image/png;base64,{b64_image}')
