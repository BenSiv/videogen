# AuraRadar Video Spoken Script - Prompter Format

Hi everyone. 

Today, we are more connected online than ever, 
but many of us feel lonely in the real world.

Why is that?

---

Well, the social and dating apps we use 
have a big conflict of interest.

Their business model is built to keep us swiping on our screens 
so they can show us ads.

If we actually meet someone and leave the app, 
they lose a customer.

Plus, they track our location and swipe history 
on their central servers all the time.

---

I wanted to build something different.

A tool that helps us connect with people physically close to us, 
with absolute privacy.

This is AuraRadar:

A completely free, open-source app 
that connects you directly to the people around you, 
without any middleman.

---

Let's look at how it works in real life.

When you open the app, 
there is no sign-up or central server.

Your profile and chats are saved only on your own device, 
fully encrypted.

You just put in a few simple vibe tags—
like programming, books, or coffee.

---

The app scans your local physical space.

When another user is nearby, 
they show up on your screen.

If you both like each other's profiles, 
you match immediately.

---

A secure, direct chat opens up right away.

You can send a quick message to say hello 
and coordinate a face-to-face meetup.

Once you match, the app gets out of your way 
so you can talk in real life.

---

But using location apps in public can feel unsafe.

If you are on a crowded bus or at a cafe, 
you don't want strangers to see exactly where you are sitting.

To solve this, we built Ghost Mode.

---

When you turn on Ghost Mode, 
your phone goes completely silent.

It doesn't broadcast any wireless signals.

But it still listens.

It silently saves a temporary list of profiles nearby, 
while keeping you completely invisible to everyone else.

---

When you get home safely, you can check who was around, 
swipe Like, 
and the app sends an encrypted message that only their phone can unlock.

When they swipe back, you match.

It is spontaneous connection, with absolute safety.

---

Now, let's talk about the tech in very simple terms.

AuraRadar uses a fast React frontend, 
but the core engine is written in Rust.

First, there are no central servers.

Discovery is handled phone-to-phone using a local mesh network.

It works even if you don't have internet or mobile data.

---

Second, how do we prove you are close to someone 
without revealing your raw GPS coordinates?

We use zero-knowledge mathematics.

---

Your phone encrypts your location.

The other phone does some quick math on that encrypted data 
to check if you are within range, 
but it can never see your actual coordinates.

Your location never leaves your phone!

---

AuraRadar is a proof-of-concept showing that we can build social tools 
that respect our privacy and help us build real-world communities.

The project is fully open source under the AGPL v3 license.

We are looking for beta testers to help us test it!

---

If you want to try it on your Android device, 
send an email to bensiv92@gmail.com with your Google Play email.

Check out the code on GitHub, drop a star, 
and let's build a decentralized, local-first web together.

Thanks for watching!
