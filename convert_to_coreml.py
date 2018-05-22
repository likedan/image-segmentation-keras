import coremltools
import VGGUnet

modelFN = VGGUnet.VGGUnet
weight_file = "weights/r.7"

model = modelFN(2, input_height=224, input_width=224)
model.load_weights(weight_file)

coreml_model = coremltools.converters.keras.convert(model,
	input_names="image",
	image_input_names="image",
	image_scale=1/255.0,
	class_labels=["bg", "item"],
	is_bgr=True)
coreml_model.save("fashion_item_segmentation.mlmodel")