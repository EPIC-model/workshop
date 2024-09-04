Next: [Accessing the Cirrus cluster](01-cluster_access.md), Previous: [Main page](../README.md), Up: [Main page](../README.md)

# Installing X-Windows

To open images from Cirrus or to use `ncview`, your computer needs an X-Window system.
If you're using a Linux distribution, you most likely already have X-Window running.
If you're using MacOS, you can use [XQuartz](https://www.xquartz.org/).
If you're using Windows with WSL or mobaXterm, you'll need [XMing](https://sourceforge.net/projects/xming/).

To test if the X server is working correctly, after logging in to cirrus with the `-X` option (more on how to [connect to cirrus later](01-cluster_access.md)), you can use the following commands:

```bash
module load ImageMagick
display
```

A window with ImageMagick's wizard should pop up, like this:

![ImageMagick's output of the display command without any parameters.](../figures/ImageMagick.png "ImageMagick's output of the display command without any parameters.")

Next: [Accessing the Cirrus cluster](01-cluster_access.md), Previous: [Main page](../README.md), Up: [Main page](../README.md)
