from twython import Twython
import numpy
import json


def auth():
    with open("access.json", 'r') as f:
        db = json.load(f)
    return Twython(db["app_key"], access_token=db["access_token"])

def main(image):
    # get the most recent meatspac tweet
    twitter = auth()
    tweet = twitter.search(q="meatspac", result_type="recent", count=1)["statuses"][0]["text"]
    # divide image by tweet length and modulate
    out_image = glitch(image, tweet)
    return out_image

def glitch(image, tweet):
    tweet_len = len(tweet)
    image_len = len(image)
    width = int(image_len/tweet_len)
    ranges = [range(x,x+width) for x in range(0, image_len, width)]
    truncate = ranges[-1][-1]-image_len
    ranges[-1] = ranges[-1][:-(truncate+1)]
    tweet = [ord(letter) for letter in tweet]
    tweet.append(tweet[0])
    for idx, part in enumerate(ranges):
        rgb = numpy.random.randint(0,3)
        for row in part:
            mod = tweet[idx]
            for pix_idx, pixel in enumerate(image[row]):
                image[row][pix_idx][rgb] = (image[row][pix_idx][rgb]+mod)%256
    return image

