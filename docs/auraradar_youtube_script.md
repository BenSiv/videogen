# AuraRadar YouTube Video Launch and Production Plan

This document provides a highly structured production plan and full scripting blueprint for presenting AuraRadar on YouTube. 

To help you get the most out of videogen, this plan includes a detailed section on how to structure your recordings, how to map them to videogen's processing pipelines, and a customized script template.

---

## Production Strategy and Videogen Workflow

Your videogen tool is the perfect partner for this video because it automates the tedious talking head editing. You do not need to record a single flawless take. Instead, you can speak naturally, pause to think, repeat sentences if you trip over words, and let the software handle the cuts.

### Recommended Recording Workflow

1. **Set Up Camera and Mic**: Place your setup in a quiet, well-lit room.
2. **Record One Long Clip (raw_talk.mp4)**: If you stumble or make a mistake, do not stop recording. Simply pause for 2 seconds, look back at the camera, and say the sentence again naturally.
3. **Run Videogen**: Place raw_talk.mp4 into videogen/videos/, run Whisper to auto-transcribe, select the best takes, and let the compiler generate coherent_storyline.mp4.
4. **Overlay B-Roll**: Import the compiled A-roll and overlay screen captures of the AuraRadar UI (React desktop/mobile), terminal screens (running make run), or diagrams.

---

## Conversational Video Script and Storyboard

* **Target Length**: ~4 - 5 Minutes (Shorter, more focused, and conversational)
* **Tone**: Warm, friendly, direct, and conversational. Easy to speak naturally for non-native English speakers.

### Section 1: The Problem (0:00 - 1:00)

| Time | Visual on Screen | Speaker Script / Audio |
| :--- | :--- | :--- |
| **0:00** | Talking head. You look at the camera warmly and smile. | "Hi everyone. Today, we are more connected online than ever, but many of us feel lonely in the real world. Why is that? <br><br>Well, the social and dating apps we use have a big conflict of interest. Their business model is built to keep us swiping on our screens so they can show us ads. If we actually meet someone and leave the app, they lose a customer. <br><br>Plus, they track our location and swipe history on their central servers all the time." |
| **0:35** | Screen capture of AuraRadar mobile/desktop UI. Sleek glassmorphism look, clean design. | "I wanted to build something different. A tool that helps us connect with people physically close to us, with absolute privacy. <br><br>This is AuraRadar: a completely free, open-source app that connects you directly to the people around you, without any middleman." |

---

### Section 2: How it Works & The Demo (1:00 - 2:15)

| Time | Visual on Screen | Speaker Script / Audio |
| :--- | :--- | :--- |
| **1:00** | Show profile creation and scanning interface. The radar sweeps. | "Let's look at how it works in real life. When you open the app, there is no sign-up or central server. Your profile and chats are saved only on your own device, fully encrypted. <br><br>You just put in a few simple vibe tags—like programming, books, or coffee." |
| **1:30** | Show a nearby resonance popup, viewing the profile card, and swiping like. | "The app scans your local physical space. When another user is nearby, they show up on your screen. If you both like each other's profiles, you match immediately." |
| **1:55** | Show chat interface. real-time P2P messaging. | "A secure, direct chat opens up right away. You can send a quick message to say hello and coordinate a face-to-face meetup. Once you match, the app gets out of your way so you can talk in real life." |

---

### Section 3: Safety & Ghost Mode (2:15 - 3:15)

| Time | Visual on Screen | Speaker Script / Audio |
| :--- | :--- | :--- |
| **2:15** | B-roll of a crowded bus, subway, or busy coffee shop. | "But using location apps in public can feel unsafe. If you are on a crowded bus or at a cafe, you don't want strangers to see exactly where you are sitting. <br><br>To solve this, we built Ghost Mode." |
| **2:35** | Screen recording toggling Ghost Mode active (sleek blue shield). | "When you turn on Ghost Mode, your phone goes completely silent. It doesn't broadcast any wireless signals. But it still listens. It silently saves a temporary list of profiles nearby, while keeping you completely invisible to everyone else." |
| **2:55** | Simple graphic showing a secure encrypted envelope going to a match after getting home. | "When you get home safely, you can check who was around, swipe 'like', and the app sends an encrypted message that only their phone can unlock. When they swipe back, you match. It is spontaneous connection, with absolute safety." |

---

### Section 4: Under the Hood Made Simple (3:15 - 4:15)

| Time | Visual on Screen | Speaker Script / Audio |
| :--- | :--- | :--- |
| **3:15** | Visual showing a serverless P2P mesh network. | "Now, let's talk about the tech in very simple terms. AuraRadar uses a fast React frontend, but the core engine is written in Rust. <br><br>First, there are no central servers. Discovery is handled phone-to-phone using a local mesh network. It works even if you don't have internet or mobile data." |
| **3:45** | Clean visual of the ZK handshake: <br>Your coordinates are encrypted -> other phone checks distance -> returns true/false without ever knowing where you are. | "Second, how do we prove you are close to someone without revealing your raw GPS coordinates? We use zero-knowledge mathematics. <br><br>Your phone encrypts your location. The other phone does some quick math on that encrypted data to check if you are within range, but it can never see your actual coordinates. Your location never leaves your phone!" |

---

### Section 5: The Outro (4:15 - End)

| Time | Visual on Screen | Speaker Script / Audio |
| :--- | :--- | :--- |
| **4:15** | Talking head. You look back at the camera and smile. | "AuraRadar is a proof-of-concept showing that we can build social tools that respect our privacy and help us build real-world communities. <br><br>The project is fully open source under the AGPL v3 license. We are looking for beta testers to help us test it! <br><br>If you want to try it on your Android device, send an email to bensiv92@gmail.com with your Google Play email. Check out the code on GitHub, drop a star, and let's build a serverless, local-first web together. Thanks for watching!" |
