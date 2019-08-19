# Software Engineer for Organizing Technology: Follow-Up Coding Interview

Woohoo, with completion of the first coding exercise, now we’re engaging supporters with a text message as soon as possible after they make their first online donation! Let’s keep iterating on the ActBlue endpoint we were working on, as to not wake people up.

When we make the request to `profile_update` endpoint on Mobile Commons, the phone number will immediately get this text message:

> I'm Jossie w/ Team Warren--thanks for being a donor to the campaign! Which one of Elizabeth's plans is your favorite?
>
> HELP4Info/STOP2Quit/Msg&DataRatesMayApply

A colleague does have one flag tho — we’ve noticed that when ActBlue is seeing spike in volumes of donations (e.g. before a debate, or EOQ), there can be an indefinite lag between actual donation time and when we get webhook notification. (It looks like big, sustained spikes in donation volume triggers a circuit breaker in ActBlue, then ActBlue processes the excess volume when the traffic has subsided, usually in the midnight hours the next morning.)

What should we do? We’d like to opt new donors in to SMS as soon as possible; just not if it’s going to wake them up in the middle of the night.

Once you decide on the way forward with your interviewer, write tests in `test_actblue.py` and update your implementation of `upload_to_mobilecommons()`.

Tip: `dateutil.parser` and `pytz` modules might be helpful — they're already imported.
