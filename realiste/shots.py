"""Découpage plan par plan des 10 épisodes pour la version ULTRA-RÉALISTE.

Chaque plan = (début, fin, image_guide, prompt_image_de_départ, prompt_mouvement).
- début / fin : timing exact dans l'animatique (episodes/epXX.mp4) et la bande-son.
- image_guide : instant extrait de l'animatique comme guide de composition.
Les prompts sont en anglais (meilleure compréhension des générateurs).
[NUBO], [CHICK] et [STYLE] sont remplacés par les blocs ci-dessous.
"""

NUBO = ("NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), "
        "round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, "
        "a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur "
        "tuft like an antenna on top of its head, about the size of a cat")

CHICK = "a tiny fluffy yellow chick sits motionless somewhere in the background, easy to miss"

STYLE = ("ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with "
         "individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key "
         "light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, "
         "no text, no subtitles, no watermark")

MOTION = ("smooth natural motion, consistent character design, no morphing, no extra limbs, "
          "Nubo never speaks")

EPISODES = [
    ("ep01_atchoum", "ATCHOUM", [
        (0.0, 1.2, 0.8, "Close-up of [NUBO] standing in a cozy lavender living room with a framed sun picture "
         "and a wooden shelf, eyes squeezed, body inflating, about to sneeze. [CHICK] on the shelf.",
         "Nubo inhales twice, body swelling, tuft trembling, static camera."),
        (1.2, 2.8, 1.8, "[NUBO] mid-sneeze in the living room; a tiny marble-sized copy of Nubo bounces on the floor.",
         "Big cartoon sneeze, Nubo squashes, a tiny Nubo pops out and bounces, the two look at each other."),
        (2.8, 5.0, 3.6, "[NUBO] sneezing again, several tiny fluffy orange Nubos bouncing around on the wooden floor.",
         "Two more sneezes, each spawning more tiny Nubos that bounce and roll, playful."),
        (5.0, 9.0, 7.0, "A living room rapidly filling with hundreds of tiny fluffy orange Nubos like a ball pit, "
         "[NUBO] half buried in the middle, tuft standing straight up.",
         "Rapid machine-gun sneezes, the orange ball pit rises fast and swallows the room."),
        (9.0, 13.0, 10.5, "The whole room filled with tiny orange fluffy creatures; only [NUBO]'s two eyes and "
         "tuft stick out of the orange sea. Silence.",
         "Nubo looks left, looks right, slow blink. Very still."),
        (13.0, 15.8, 14.6, "A vintage red gumball machine on a mint-green grocery counter, its glass globe packed "
         "with tiny orange fluffy Nubos. [CHICK] on the counter.",
         "Fast camera pull-back revealing the gumball machine, a coin drops into the slot, the crank turns by itself."),
        (15.8, 18.0, 17.0, "Inside the metal chute of the gumball machine, [NUBO] sitting after rolling out, "
         "looking straight at the camera.",
         "Nubo rolls in and lands, turns its eyes to the camera, blinks twice, then starts inhaling to sneeze."),
    ]),
    ("ep02_grille_pain", "LE GRILLE-PAIN", [
        (0.0, 1.0, 0.7, "Extreme slow motion: a golden slice of toast spinning straight toward the camera, crumbs "
         "floating, blurred pastel mint kitchen behind.", "Toast flies at the lens in slow motion."),
        (1.0, 3.0, 1.3, "[NUBO] in a mint-tiled kitchen next to a pastel pink retro toaster, holding a toast above its "
         "head proudly. [CHICK] on a shelf.", "Nubo catches the toast, tosses it aside, slides a fresh slice into the toaster."),
        (3.0, 6.0, 4.3, "A pancake popping out of the pink toaster and gliding through the kitchen like a frisbee, "
         "[NUBO] watching, tuft curled like a question mark.", "Ding, the pancake shoots up and glides away, Nubo's eyes follow."),
        (6.0, 9.0, 7.8, "A grey pigeon bursting out of the pink toaster and flying away, [NUBO] startled, tuft "
         "standing straight up.", "Nubo puts a striped sock in, ding, a live pigeon flaps out and flies off."),
        (9.0, 12.4, 10.5, "[NUBO] standing on top of the pink toaster peering into the slot, its tuft pulled by "
         "suction.", "Nubo hops onto the toaster, leans over, gets sucked into the slot stretching like rubber."),
        (12.4, 17.0, 15.5, "The pink toaster glowing orange from its slots, a pigeon and a pancake waiting next to "
         "it on the counter like in a waiting room.", "Lever down, ticking timer, the toaster trembles and glows."),
        (17.0, 20.0, 18.6, "[NUBO] perfectly toasted golden-brown with grill marks, a wisp of smoke from its tuft, "
         "standing proudly on the counter.", "Nubo shoots out in slow motion, lands, looks at camera, blinks twice; "
         "a toast pops toward the lens."),
    ]),
    ("ep03_la_plante", "LA PLANTE", [
        (0.0, 5.5, 3.0, "[NUBO] on a sunny windowsill with pink curtains spraying water on a tiny cactus in a "
         "terracotta pot. [CHICK] on the sill.", "With each spray the cactus doubles in size with a bouncy boing, "
         "the pot cracks, Nubo's tuft stands up."),
        (5.5, 10.2, 9.6, "A giant cactus towering over [NUBO], a huge pink flower blooming at its top, glowing "
         "golden center.", "The bud swells and blooms in slow motion, petals unfolding, warm glow."),
        (10.2, 15.0, 12.6, "Macro view into the glowing center of a pink flower revealing a miniature windowsill "
         "where a tiny Nubo sprays a tiny cactus.", "Continuous seamless zoom into the flower ending exactly on the "
         "opening framing (infinite Droste loop); the tiny Nubo blinks at camera."),
    ]),
    ("ep04_0317", "03:17", [
        (0.0, 2.4, 1.5, "Grainy green night-vision security camera footage of a dark kitchen, high fisheye angle, "
         "timestamp 03:17:04, [NUBO] tiptoeing toward a tall fridge.", "Nubo tiptoes across the floor, CCTV jitter."),
        (2.4, 5.5, 3.6, "Same CCTV view, fridge door open showing a colorful disco party inside: dancing eggs, "
         "lemon, sausage and cheese with tiny eyes, a disco ball, colored lights spilling out.",
         "The food dances to the beat, lights flash, Nubo stares."),
        (5.5, 9.0, 7.6, "Same CCTV view, fridge open with normal light, all food items perfectly still and innocent.",
         "Door closes and reopens: everything frozen, one egg wobbles slightly."),
        (9.0, 15.8, 12.5, "Same CCTV view, all the food inside the fridge turned toward the security camera, "
         "staring; [NUBO] in front of the fridge.", "Slow creepy push-in, then Nubo slowly turns to the camera."),
        (17.6, 20.0, 18.6, "Night-vision fisheye close-up of [NUBO]'s face pressed against the camera lens.",
         "Nubo blinks twice, heavy CCTV noise, then static."),
    ]),
    ("ep05_concours_de_regard", "CONCOURS DE REGARD", [
        (0.0, 1.0, 0.5, "Extreme close-up of [NUBO]'s narrowed determined eyes, western standoff style.",
         "Slow push-in, intense."),
        (1.0, 1.8, 1.4, "Extreme close-up of a goldfish's round unblinking eye through glass, water bubbles.",
         "Fish eye perfectly still, bubbles rise."),
        (1.8, 6.0, 3.0, "[NUBO] face to face with a round glass fishbowl containing a goldfish on a wooden table, "
         "lavender striped wall. [CHICK] on the table.", "Alternating dramatic zooms, a sweat drop, a tumbleweed rolls by."),
        (6.0, 10.0, 8.5, "A crowd of colorful fluffy creatures gathers behind the duel holding signs with drawings "
         "of Nubo and of a fish.", "The crowd pops in and cheers silently."),
        (10.0, 14.0, 12.5, "Time-lapse: [NUBO] with a long grey beard still staring at the goldfish; night, snow and "
         "autumn leaves passing.", "Day turns to night, snow, leaves, the beard grows, the fish never moves."),
        (14.0, 17.0, 15.7, "[NUBO] with a grey beard blinking, the crowd erupting with confetti.",
         "Nubo's eyes tremble then blink, gong, the crowd jumps."),
        (17.0, 21.2, 19.8, "A tiny golden trophy on the fishbowl, fireworks, bearded [NUBO] slumped and defeated.",
         "Fireworks, Nubo collapses, then looks at camera and blinks twice."),
        (21.2, 22.0, 21.6, "Extreme close-up of the goldfish's eye.", "Still, loop back to the opening close-up."),
    ]),
    ("ep06_mauvais_etage", "MAUVAIS ÉTAGE", [
        (0.0, 1.6, 0.6, "View from inside a warm wooden elevator: doors open on a brown bear in a striped swimsuit "
         "sitting in a bubbling hot tub, staring. [NUBO] in the foreground left by the button panel.",
         "Ding, doors open, the bear stares, Nubo presses the close button, doors close."),
        (1.6, 2.8, 2.0, "Elevator interior, doors closed, [NUBO] waiting, floor lights above the doors.",
         "Nubo bobs to the elevator music (reusable travel shot)."),
        (2.8, 4.9, 3.5, "Elevator doors open on outer space: Earth and a waving astronaut floating.",
         "Astronaut waves, Nubo presses close."),
        (5.6, 7.5, 6.8, "Elevator doors open on a wall of grandmothers in glasses all knitting small orange Nubo dolls.",
         "All grannies look up at the same time, Nubo frantically presses close."),
        (8.2, 10.1, 9.0, "Elevator doors open on the inside of a whale: ribs, ankle-deep water, a red and white "
         "lighthouse with a rotating beam.", "Beam sweeps, a drip falls, Nubo presses close."),
        (11.0, 13.9, 11.8, "Elevator doors open on a grey real office; a giant real human eye fills the doorway "
         "and looks at Nubo. [NUBO] terrified, tuft up, sweating.", "The eye opens and turns to Nubo, Nubo presses close "
         "ten times, doors close agonizingly slowly."),
        (15.2, 19.8, 18.8, "Elevator doors open on a cream landing with a plant where another identical [NUBO] waits.",
         "Both Nubos stare at each other, then both turn to the camera and blink twice in sync."),
        (19.8, 24.0, 20.5, "The two identical Nubos crossing in the elevator doorway, swapping places.",
         "One steps out, one steps in, doors close, ding, doors open again on the bear."),
    ]),
    ("ep07_ne_pas_appuyer", "NE PAS APPUYER", [
        (0.0, 3.0, 1.8, "A big glossy red button on a lavender wall under a no-hands pictogram sign, [NUBO] next to "
         "it. [CHICK] on the floor beside the button.", "Nubo presses, confetti bursts, Nubo spins happily."),
        (3.0, 6.2, 4.0, "A grand piano crashed on the floor right next to [NUBO], dust, confetti everywhere, Nubo's "
         "tuft standing straight up.", "Click, a piano falls from above and crashes beside Nubo, camera shake."),
        (6.2, 9.0, 8.7, "Gravity flipped: [NUBO] and the piano stuck upside down on the ceiling, the chick still "
         "on the floor; Nubo's arm stretching like rubber down to the button.",
         "Everything falls up to the ceiling, Nubo's arm stretches all the way down to press the button."),
        (9.0, 12.8, 10.6, "STYLE BREAK: the same corridor rendered as a crude handmade felt stop-motion puppet set, "
         "Nubo turned into a felt puppet looking at its own hands in horror.",
         "Everything falls back down and the world becomes cheap felt stop-motion; Nubo panics."),
        (12.8, 16.0, 14.0, "[NUBO] (back to ultra-realistic) slowly walking backward away from the red button.",
         "Nubo backs away very slowly, never breaking eye contact with the button, exits frame."),
        (16.0, 17.6, 17.3, "The tiny yellow chick next to the red button, alone in the corridor.",
         "The chick slides by itself to the button, hops and presses it. Cut to black."),
    ]),
    ("ep08_lessive", "LESSIVE", [
        (0.0, 1.4, 0.5, "View through the round glass door of a washing machine: [NUBO] spinning in the drum with "
         "striped socks, dizzy spiral eyes.", "Drum spins, Nubo tumbles."),
        (1.4, 4.7, 3.5, "A pea-sized tiny [NUBO] in front of an open washing machine in a mint-tiled laundry room, "
         "looking up at a care label. [CHICK] on a shelf.", "Ding, door opens, shrunken Nubo hops out, looks at label, "
         "jumps back in."),
        (4.7, 6.6, 5.6, "The washing machine shaking, tiny Nubo spinning visible behind the glass.",
         "Machine rumbles and vibrates."),
        (6.6, 10.4, 7.6, "An enormous over-puffed fluffy [NUBO] bursting out of the washing machine, filling the room.",
         "Ding, giant fluffy Nubo squeezes out, blinks, then wiggles back inside."),
        (10.4, 12.3, 11.2, "The washing machine hopping wildly on the floor.", "Violent spin cycle, the machine jumps."),
        (12.3, 15.0, 13.4, "An orange hand-knitted sweater with two glossy eyes lying in front of the washing machine.",
         "Ding, the sweater slides out onto the floor."),
        (15.0, 18.0, 17.5, "A grey cat proudly wearing the orange knitted sweater with two eyes on its chest.",
         "The cat walks in, puts on the sweater, struts; the sweater's eyes blink twice at the camera."),
    ]),
    ("ep09_joyeux_anniversaire", "JOYEUX ANNIVERSAIRE", [
        (0.0, 3.0, 0.9, "[NUBO] with puffed cheeks behind a polka-dot party table, a pink two-layer birthday cake "
         "with one striped candle, pink wall with bunting.", "Nubo blows, the flame goes out, then relights with a pop."),
        (3.0, 6.3, 3.6, "[NUBO] blowing hard, bunting and streamers flying away.", "Harder blow, decorations fly off, "
         "candle relights."),
        (6.3, 9.4, 7.2, "The walls of the room ripping away revealing outer space and a grey moon surface with "
         "Earth in the sky.", "The walls are blown away like paper, the candle relights."),
        (9.4, 15.0, 12.5, "[NUBO] flattened like a deflated balloon next to the cake on the moon, the candle still "
         "burning.", "Ultimate blow, tablecloth flies away, Nubo deflates, silence."),
        (15.0, 17.2, 16.2, "The candle flame grown huge, leaning toward flat [NUBO].",
         "The flame inhales, grows, and blows on Nubo; Nubo's tuft goes out like a wick with smoke."),
        (17.2, 20.0, 19.2, "Flat [NUBO] with a smoking tuft on the moon looking at camera.",
         "Nubo blinks twice, then its tuft relights with a pop."),
    ]),
    ("ep10_le_selfie", "LE SELFIE", [
        (0.0, 1.0, 0.5, "Phone front-camera selfie POV: [NUBO] winking in a pastel forest, a tiny moose far away "
         "between the trees.", "Camera flash, selfie pose."),
        (1.0, 3.0, 1.5, "Wide shot, [NUBO] holding a phone up in a pastel forest, empty forest. [CHICK] in the grass.",
         "Nubo changes pose."),
        (3.0, 5.0, 3.5, "Selfie POV: [NUBO] winking, the moose now mid-distance behind.", "Flash."),
        (5.0, 7.0, 5.5, "Selfie POV: [NUBO] with tuft trembling, a huge moose standing right behind it.",
         "Flash, horror sting."),
        (7.0, 10.0, 8.9, "Wide shot, [NUBO] turned around, empty forest, shrugging with a question-mark tuft.",
         "Nubo turns around, sees nothing, shrugs, lifts the phone again."),
        (10.0, 12.0, 10.6, "Selfie POV: a giant smiling moose holding the phone, [NUBO] squeezed against its cheek, "
         "stunned.", "Flash, the moose grins."),
        (12.0, 15.0, 13.0, "Wide shot, the moose and [NUBO] side by side happily looking at the phone.",
         "They admire the photo together."),
        (15.0, 18.0, 17.4, "The moose chewing, crumbs of phone falling, [NUBO] next to it.",
         "The moose eats the phone with a crunch, then both turn to the camera and blink twice in sync. Flash."),
    ]),
]
