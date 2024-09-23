# SC2 Adversary Scoring System #

Because SC2 Zephyrus Parser is a bit outdated, you won't be able to run this application immediately.
I will clean up my fork and publish it soon.

Starcraft 2 will never be a dead game.
As financial support for pros and the tournament system wanes, I wanted to find a way to maintain the competitive intrigue.
I watch way too many starcraft 2 streamers, but often their ladder grinding can be monotenous, devoid of any "story" or emotional investment.

The initial goals of this system are simple: Display to the player (and maybe audience) the map score between the player and the opponent - while in the loading screen.
I do this by:
- Listening for the loading screen
- Parsing the opponent username (good luck with barcodes...)
- Printing the player's map score vs the opponent
- Upon game completion, parsing the replay to save the result

Goals:
- Add the ability to create notes on opponents that display on load
- OBS integration
- More elegant way of parsing barcodes
- Import all replays so that you don't have to start tracking from scratch (will be difficult with patches, etc.)

The program currently works. It is barely held together with a hacked together version of [SC2 Zephyrus Parser](https://github.com/ZephyrBlu/zephyrus-sc2-parser)
