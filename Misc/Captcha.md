# Captcha
## The Challenge
This challage is more an engineering the hacking challange. We get a webserver that askes us to solve a captcha. The picture of the captcha
is a base 64 encoded string that we can find in the html of the side.

![example](https://github.com/Timon33/CSCG2020WriteUps/blob/master/Misc/0ANCPPM.png)

If we sumbit the correct text seen in the picture we get to the next
stage, at each stage the number of captchas we have to solve at the same time increases. At the Baby stage it is only 1, then 3, 10 and 100
at a time, after that we get the flag. The problem is that we only have 30 secounds - far to less time to solve 100 captchas by hand. So
we have to solve the captchas using a computer. But aren't captchas desinged to not be solved by computers? Well yes but these captchas are
fairly simple can we can solve them using marchine learning.

## Getting the Data
For marchine learning we need quite a lot of data to train on. We can use python with a module like requests to get the captcha and save it,
then submit are wrong value for the captcha and get the respons again. If we fail the first baby capcha the server fells bad for us and
gives us the solution. We can use this to save the captcha as a image that has the correct result as the filename. The script `dataMiner.py`
will collect 10000 sampels from the server in a few minutes.

## The Plan
We could try to build some Neural Network to directly predict the hole captcha but this is difficult becuase the numbers of characters chages.
The way i did it, wich was inspired from [this blog post](https://medium.com/@ageitgey/how-to-break-a-captcha-system-in-15-minutes-with-machine-learning-dbebb035a710)
was to first split the image into the individual characters and save them and the their lable. Then we can use a small Convolutional Neural Network
and train it to identify the letters. Later when solving the challenge
we can again split up the image into letters and predict them one their own, then we pice the predictions together to get the full solution.

## Implementaion
### Preparing the data
Once we have the training data we can use openCV to get the outlines of the letters, cut and save them.
A problem i encountered with this aproach is, that sometimes 2 letters stick together. To solve this we cut a box in half if it is relativly
wide. Also we discrad any boxes that are very small because they are almost everytime the points of an "i". This way of splitting letter
sometimes fails but i tryed diffrent values and got a accuracy of 95% for the splitting process.
You can find the full code in `extract_single_letters_from_captchas.py`.


### The CNN
I used Keras, a high level marchine learning libary, to build the cnn model. The `train_model.py` script uses our prepared data to train on
and archives a accuracy of over 99% in my case. I also experimented with models to predict the length of a given captcha to improve the splitting
process, but i didn't really work out for me.

## Solving the Challange
The last part is to actually interact with the server using a script to get the captchas and send the results back. `client.py` solves the
challenge in a few minutes depending on your luck, because it only has 94% accuracy but needs to get up to 100 right a time. The script
Request the first stage, then downloads the captcha(s), solves it and sends back the respones as a post request. If we dont land on the
fail page we keep going until we save the Bot stage and get to the flag. We save a local copy of the html respone for the flag, you can find it under flag.html.

![flag](https://github.com/Timon33/CSCG2020WriteUps/blob/master/Misc/Flag.png).
