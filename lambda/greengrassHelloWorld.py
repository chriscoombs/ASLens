import os
import greengrasssdk
from threading import Timer
import time
import awscam
import cv2
from threading import Thread
import mo
from playsound import playsound

global detected = ""

client = greengrasssdk.client("iot-data")

iotTopic = "$aws/things/{}/infer".format(os.environ["AWS_IOT_THING_NAME"])

def greengrass_infinite_infer_run():
    try:
        modelType = "classification"
        model_name = "image-classification"
        input_width = 224
        input_height = 224
        max_threshold = 0.75
        error, model_path = mo.optimize(model_name,input_width,input_height)
        outMap = { 0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7 : "h", 8 : "i", 9 : "k", 10 : "l", 11 : "m", 12 : "n", 13 : "o", 14 : "p", 15 : "q", 16 : "r", 17 : "s", 18 : "t", 19 : "u", 20 : "v", 21 : "w", 22 : "x", 23 : "y", 24 : "z" }
        client.publish(topic=iotTopic, payload="Object detection starts now")
        mcfg = {"GPU": 1}
        model = awscam.Model(model_path, mcfg)
        client.publish(topic=iotTopic, payload="Model loaded")
        ret, frame = awscam.getLastFrame()
        if ret == False:
            raise Exception("Failed to get frame from the stream")

        doInfer = True
        while doInfer:
            # Get a frame from the video stream
            ret, frame = awscam.getLastFrame()
            # Raise an exception if failing to get a frame
            if ret == False:
                raise Exception("Failed to get frame from the stream")

	        margin = (frame.shape[1] - frame.shape[0]) / 2
            cropped = frame[0:frame.shape[0], margin:frame.shape[1] - margin]
            frameResize = cv2.resize(cropped, (input_width, input_height))
            inferOutput = model.doInference(frameResize)
            parsed_results = model.parseResult(modelType, inferOutput)["classification"]
            client.publish(topic=iotTopic, payload = str(parsed_results))
            for obj in parsed_results:
                if obj["prob"] > max_threshold and detected != outMap[obj["label"]]:
		            detected = outMap[obj["label"]]
                    client.publish(topic=iotTopic, payload = outMap[obj["label"]])
		    playsound("../letters/" + outMap[obj["label"]] + ".mp3");

    except Exception as e:
        msg = "Test failed: " + str(e)
        client.publish(topic=iotTopic, payload=msg)

    # Asynchronously schedule this function to be run again in 15 seconds
    Timer(15, greengrass_infinite_infer_run).start()

# Execute the function above
greengrass_infinite_infer_run()

# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
