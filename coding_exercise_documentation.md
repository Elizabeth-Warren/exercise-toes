# Software Engineer for Organizing Technology: Coding Exercise

Woohoo, let’s work together to engage with new donors over text message to thank them and get them involved in the campaign.

This short exercise should take about 30 minutes.

## Background

The campaign has a text message list with phone number 24477. Supporters can text FIGHT (or other keywords) to 24477 to subscribe to different kinds of updates. We use this text message list for organizing (e.g. inviting people in certain zip/area codes to events) and for fundraising (e.g. blast fundraising texts at end of quarter). We use a platform called Mobile Commons to set up these texts. 

We have lots of online donation forms on the ActBlue platform. [Here’s one example.](https://secure.actblue.com/donate/jkbforelizabethwarren) These forms account for the majority of donations to the campaign. All have SMS opt-in language (the “By providing your cell phone number...” disclaimer at the bottom), so as soon as somebody makes a donation, if they’ve supplied their cell phone number, we can subscribe them to our text message list on Mobile Commons. 

We have a few options for how to do this. We already have set up a daily job in our data warehouse to upload all new phone numbers from donors to Mobile Commons. But in past campaigns, we’ve found that opt-out rates are lower when we subscribe a phone number and engage them with a text message immediately after a transaction, instead of the next day.

ActBlue offers webhook functionality, so we can set up an endpoint that ActBlue will hit whenever we get a new donation. Mobile Commons offers an API with which we can POST to to subscribe a phone number. So the goal here is to set up a webhook that will immediately subscribe new donors to our text message list.

## Step 1: Set up Docker and run tests

Install Docker if you haven’t already ([instructions for Mac](https://docs.docker.com/docker-for-mac/install/)). Clone the `exercise-toes` repo (the repo containing this document):

https://github.com/Elizabeth-Warren/exercise-toes

From inside the `exercise-toes` repo, run these commands to set up and run its container:

`make build up`

Leave this running. In a separate console, run tests with:

`make test`

They should all pass. Reach out to jkatzbrown@elizabethwarren.com if something isn’t behaving, we want to help!

## Step 1: Implement `upload_to_mobilecommons()` in actblue/actblue.py

First, you’ll want to read through `actblue/test_actblue.py`. The goal of this step is to make all the tests therein pass.

Next, open `actblue/actblue.py` and take a look at `upload_to_mobilecommons()`. Right now it simply raises NotImplementedError.

Remove the `raise(NotImplementedError)` and run `make test`. This makes two tests fail.

Now, let’s implement `upload_to_mobilecommons()` so the tests pass!

You can refer to ActBlue’s webhook documentation and the sample incoming donation payload used in tests `actblue/sample_donation.json`. See Appendix 1 below for the relevant Mobile Commons API endpoint documentation (unfortunately their documentation is not publicly accessible :-/).

## Step 2: Send us your `actblue.py`

Reply to the email we sent you with your actblue.py. Thank you thank you!

(Next steps of the interview process may involve a screen-share coding interview building on top of your work in this repo.)

## Appendix 1. Mobile Commons `profile_update` endpoint documentation

Mobile Commons API documentation is behind a login wall, so it's pasted here:

URL:	https://secure.mcommons.com/api/profile_update

Protocol:	HTTP POST

Parameters:	

- phone_number (Required)
- email
- postal_code
- first_name
- last_name
- street1
- street2
- city
- state
- country
- opt_in_path_id: This will subscribe the user to this campaign and send the message flow in this opt-in path. The value should be your opt-in path key.
