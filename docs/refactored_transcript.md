# AuraRadar: Connection with Absolute Privacy

Hi everyone.

Today, we are more connected online than ever, but many of us find it difficult—actually, many of us find it difficult to connect in the real world.

Well, why is that?

It seems like all the platforms we use to connect—social media, dating apps—they all have a big conflict of interest. They want to keep you swiping and scrolling, but never actually leaving the app to connect with people in the real world.

For dating apps, if someone actually goes out on a date and finds a partner, the app loses a customer! It’s just not in their interest to help you meet.

On top of that, you’re giving away so much of your most personal data—your location, your preferences—to these companies that store everything on their databases.

So, I wanted to build something different. A tool that helps us connect physically with people, but with absolute privacy.

I call it AuraRadar. 

The idea is that you project your "aura" to your surroundings. It’s a completely free, open-source app that connects you directly with the people around you, without any middleman.

Let’s take a look at how it works in real life.

When you open the app, there is no sign-up. You just set up your Aura profile. All your interactions—your profile, your chats—are stored fully encrypted on your own device. They are not sent anywhere else.

The app scans your local physical space. When another user nearby is also projecting their aura, they show up on your screen. If you both like each other’s profiles, you match immediately.

A secure, direct chat opens up right away. You can send a quick message, say hello, and coordinate a face-to-face meetup. Once you match, the app gets out of your way so you can talk in real life.

But using location apps in public can feel unsafe. If you are on a crowded bus or at a cafe, you might not feel like projecting your aura at that moment. For that, we built Ghost Mode.

When you toggle Ghost Mode, your phone goes completely silent. It doesn't broadcast your aura, but it is still listening. It silently saves a temporary list of profiles nearby while keeping you completely invisible to everyone else.

When you get home safely, or to your safe space, you can check who was around. You can swipe "like," and the app sends an encrypted message that only their phone can unlock. When they swipe back, you match.

It’s spontaneous connection, with absolute safety.

Now, let’s talk about the tech in very simple terms.

AuraRadar uses a fast React frontend, but the core engine is written in Rust. First, there are no central servers. Discovery is handled phone-to-phone using a local mesh network. It works even if you don’t have internet or mobile data.

Second, how do we prove you are close to someone without revealing your raw GPS coordinates? We use zero-knowledge mathematics.

Your phone encrypts your location. The other phone does some quick math on that encrypted data to check if you are within range, but it can never see your actual coordinates. Your location never leaves your phone!

AuraRadar is a proof-of-concept showing that we can build social tools that respect our privacy and help us build real-world connections.

The project is fully open source under the AGPL v3 license. We are looking for beta testers to help us test it!

Currently, it’s available only for Android. If you want to be part of the testing group, see the details down below in the description of the video.

Check out the code on GitHub, drop a star, and let’s build a decentralized, local-first web together.

Thank you so much for watching!
