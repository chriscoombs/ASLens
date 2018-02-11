# ASLens

Before deploying model to DeepLens, ensure MXNet is updated on device.

Copy contents of greengrassHelloWorld.py into Lambda.

S3 model artifact path for model:
s3://deeplens-230118/aslens/output

Once the project is synced with DeepLens device, copy contents of letters directory to artifacts directory.

Add ggc_user to audio group.

Add audio devices to Greengrass group (ensure that group is set to audio). Add resources to Lambda function. Deploy the group.

Ensure that playsound and dependencies are deployed on the device.

Restart the Greengrass service.
