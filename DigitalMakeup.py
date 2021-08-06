from PIL import Image, ImageDraw
import face_recognition
import numpy as np


class Makeup:
    def __init__(self):
        pass

    def show_makeup(self, image_name, filter=None):
        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(image_name)
        if filter is None:
            pil_image = self.apply_makeup(image)
        else:
            pil_image = self.face_filter(image, **filter)
        pil_image.show()

    def get_makeup(self, image, filter=None):
        if filter is None:
            pil_image = self.apply_makeup(image)
        else:
            pil_image = self.face_filter(image, **filter)
        # Convert back to Frame Image
        frame = np.asarray(pil_image)

        return frame

    def raduis(self, face):
        x = max(face["left_eye"], key=lambda v: v[0])[0]
        y = min(face["left_eye"], key=lambda v: v[0])[0]
        return abs(x - y)

    def bow_tie_coordinates(self, face):
        mid_top = max(face["chin"], key=lambda v: v[1])
        left = min(face["chin"], key=lambda v: v[0])
        right = max(face["chin"], key=lambda v: v[0])
        lip_bot = max(face["bottom_lip"], key=lambda v: v[1])
        height = mid_top[1] - lip_bot[1]
        points = [
            (left[0], mid_top[1]),
            (left[0], mid_top[1] + height),
            (right[0], mid_top[1]),
            (right[0], mid_top[1] + height),
        ]
        center = (mid_top[0], mid_top[1] + height // 2)
        width = abs(left[0] - right[0])
        diff = round(width / 3)
        return (
            points,
            (height // 3,) + center,
            (center[0] - diff, center[1], center[0] + diff, center[1]),
        )

    def apply_makeup(self, image):

        # Find all facial features in all the faces in the image
        face_landmarks_list = face_recognition.face_landmarks(image)

        # Load the image into a Python Image Library object so that we can draw on top of it and display it
        pil_image = Image.fromarray(image)

        # Create a PIL drawing object to be able to draw lines later
        d = ImageDraw.Draw(pil_image, "RGBA")
        circle = lambda r, x, y: (x - r, y - r, x + r, y + r)
        for face_landmarks in face_landmarks_list:
            # The face landmark detection model returns these features:
            #  - chin, left_eyebrow, right_eyebrow, nose_bridge, nose_tip, left_eye, right_eye, top_lip, bottom_lip

            # Draw a line over the eyebrows
            d.line(face_landmarks["left_eyebrow"], fill=(128, 0, 128, 100), width=3)
            d.line(face_landmarks["right_eyebrow"], fill=(128, 0, 128, 100), width=3)

            # # chin
            # d.polygon(face_landmarks["chin"], fill="yellow")
            # # x, y = max(face_landmarks["chin"], key=lambda v: v[1])
            # # d.ellipse(circle(20, x, y), fill="white", outline=(255, 255, 255))
            # rec, cod, line = self.bow_tie_coordinates(face_landmarks)
            # d.polygon(rec, fill="black", outline=(255, 255, 255))
            # d.line(line, fill="white", width=1)
            # d.ellipse(
            #     circle(cod[0], cod[1], cod[2]),
            #     fill="black",
            #     outline=(255, 255, 255),
            # )
            # Draw over the lips
            d.polygon(face_landmarks["top_lip"], fill=(128, 0, 128, 100))
            d.polygon(face_landmarks["bottom_lip"], fill=(128, 0, 128, 100))

        return pil_image

    def face_filter(self, image, makeup=True, chin=False, bow_tie=True):
        # Find all facial features in all the faces in the image
        face_landmarks_list = face_recognition.face_landmarks(image)

        # Load the image into a Python Image Library object so that we can draw on top of it and display it
        pil_image = Image.fromarray(image)

        # Create a PIL drawing object to be able to draw lines later
        d = ImageDraw.Draw(pil_image, "RGBA")
        circle = lambda r, x, y: (x - r, y - r, x + r, y + r)
        for face_landmarks in face_landmarks_list:
            # The face landmark detection model returns these features:
            #  - chin, left_eyebrow, right_eyebrow, nose_bridge, nose_tip, left_eye, right_eye, top_lip, bottom_lip

            # Draw a line over the eyebrows
            if makeup:
                d.line(face_landmarks["left_eyebrow"], fill=(128, 0, 128, 100), width=3)
                d.line(
                    face_landmarks["right_eyebrow"], fill=(128, 0, 128, 100), width=3
                )

            # chin
            if chin:
                d.polygon(face_landmarks["chin"], fill="yellow")

            # bow tie
            if bow_tie:
                rec, cod, line = self.bow_tie_coordinates(face_landmarks)
                d.polygon(rec, fill="black", outline=(255, 255, 255))
                d.line(line, fill="white", width=1)
                d.ellipse(
                    circle(cod[0], cod[1], cod[2]),
                    fill="black",
                    outline=(255, 255, 255),
                )

            if makeup:
                # Draw over the lips
                d.polygon(face_landmarks["top_lip"], fill=(128, 0, 128, 100))
                d.polygon(face_landmarks["bottom_lip"], fill=(128, 0, 128, 100))

        return pil_image


if __name__ == "__main__":
    test_img = "people/face_0000.png"
    # Makeup().show_makeup(image_name=test_img)
    my_filter = {"makeup": True, "chin": True, "bow_tie": True}
    Makeup().show_makeup(image_name=test_img, filter=my_filter)
