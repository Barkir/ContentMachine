# Brief plan
# 1. This is a bot whom is sent a message (link to a video or to a post or some prompt for a post)
# 2. He converts it to a telegram post with a picture and posts it to a channel.

# Transcribing module mustn't be located here! We must call a transcribing api if we see a link to a video.
# Here's a brief pipeline.

# Sending message ->
# if it is a link then
#   call transcribing module
#   call a function to turn transcribition into a post
#   send it to the user and get the approve
#   post it
# if it is an idea for a post then
#   call a function to turn idea to post
#   send it to the user and get the approve
#   post it