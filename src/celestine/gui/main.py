import os

image = {}


def setup(self):
    image["image1"] = self.image_load(
        os.path.join("celestine", "file", "anitest.gif")
    )
    image["image2"] = self.image_load(
        os.path.join("celestine", "file", "test4.gif")
    )


def view(self):
    self.label_add(image["image1"])
    self.label_add(image["image2"])


def main(window):
    window.run(setup, view)
