# AuraRadar Video Spoken Script - Prompter Format

We are living in a profound paradox. 

We have never been more digitally connected, 
yet we are in the midst of a global loneliness pandemic.

---

The commercial social and dating apps we rely on 
have a fundamental, structural conflict of interest.

Their business models are designed to keep you swiping endlessly on their platform 
to monetize your attention.

If you actually find a real connection and get off their app, 
they lose a customer.

Worse, standard apps force you to surrender your absolute data sovereignty—
sending your location history, preferences, and private swipes to centralized databases.

---

I wanted to build something entirely different.

A tool that returns the power of connection back to your immediate physical space, 
with absolute privacy.

Say hello to AuraRadar: 

A completely open-source, serverless, local-first proximity network 
designed to get you off your screen and into real-world, face-to-face conversations.

---

Let's look at how this works in practice.

When you launch AuraRadar, there are no central servers to log into.

Your profile, your type, and your interactions reside entirely on your physical device, 
fully encrypted in a local SQLCipher database.

You set up your public vibe tags—
like Rust development, sci-fi novels, or indie music.

---

Once active, the app scans your physical proximity for other peers.

Using a specialized P2P mesh network, it discovers nearby active profiles.

When a co-present peer enters your orbit, 
they appear on your radar as a Resonance.

---

You can inspect their profile, interests, and distance.

If there's a mutual resonance and you both swipe Like, 
the app triggers an immediate match celebration.

---

Instantly, a secure, local peer-to-peer chat thread is established.

You can send an encrypted greeting to break the ice 
and coordinate a face-to-face meetup right then and there.

Once you connect, the app gets out of your way.

---

Now, if you've ever used a location-based app, 
you know there is a serious safety hazard.

If you're on a crowded bus or in a tight coffee shop, 
turning on a proximity scanner can feel incredibly vulnerable.

If anyone can see exactly where you are sitting, 
you risk unwanted, intrusive physical approaches.

We call this the Transit Space Nightmare.

---

To solve this, AuraRadar implements Ghost Mode, 
also known as Asymmetric Discovery.

When you activate Ghost Mode, your phone goes completely radio-silent.

It broadcasts absolutely nothing.

However, it continues to passively listen to active broadcasters in the room, 
creating a temporary, secure list of silhouettes stored only on your device.

You are completely invisible to the room.

---

Once you return to the safety of your home, 
you can review your history and swipe on people you crossed paths with.

Because you're no longer in physical range, 
the app packages your swipe into a cryptographically locked digital envelope 
that only the recipient's phone can decrypt.

They get the notification later, and when they swipe back, the match is completed.

Spontaneous connection, absolute physical safety.

---

Let's open the hood and talk about the architecture.

AuraRadar is built as a hybrid native application.

The user interface is a high-performance React frontend 
styled with custom glassmorphism.

But the real engine is written in native Rust, 
bridged securely to the frontend using Tauri v2.

---

First, there are no central servers.

Proximity discovery is handled entirely through an autonomous P2P swarm.

Under the hood, we leverage libp2p for mesh networking.

To bypass OS-level multicast blocks and mobile hotspot restrictions, 
we built a dedicated subnet dialing thread running on port 14224.

This directly establishes TCP handshakes between mobile nodes, 
even when behind complex NATs.

---

But how do we prove two people are close to each other 
without exposing their raw GPS coordinates?

If a malicious node queries the app repeatedly, 
they could triangulate your exact location.

AuraRadar solves this using Zero-Knowledge Proximity Handshakes 
based on continuous Euclidean distances.

---

Here is the math.

Peer A encrypts their coordinates using the Paillier homomorphic cryptosystem 
and sends the ciphertexts to Peer B.

Because Paillier is additively homomorphic, 
Peer B can compute the encrypted squared distance between them 
without learning Peer A's actual coordinates.

To prevent Peer A from learning the distance upon decryption, 
Peer B multiplies it by a high-entropy random blinding factor r.

Peer A decrypts the blinded value, 
and generates a compact Bulletproof range proof 
proving that the blinded distance is less than the maximum allowable range.

Peer B verifies the Bulletproof.

Proximity is verified, coordinates remain 100% secret, 
and no trusted setup is ever required.

---

For mobile devices, this whole process is compiled down 
to highly optimized native Rust libraries 
exposed to a persistent Android Foreground Service.

This keeps the proximity scanning active in the background, 
firing local notifications even when your phone is in your pocket.

---

AuraRadar is more than just a software utility.

It is an exploration in reclaiming our digital spaces.

It is a proof-of-concept that local-first, serverless networks 
can replace extractive attention-economy platforms 
and help us build healthy, safe, face-to-face communities.

---

The entire project is completely open source under the AGPL v3 license.

We are actively seeking beta testers to join our Google Play private test group.

If you want to install it on your Android device 
and help us test proximity mesh routing in the wild, 
send an email to bensiv92@gmail.com with your Google Play email address!

Check out the code on GitHub, drop a star, 
and let's build a decentralized, local-first web together.

Thanks for watching.
