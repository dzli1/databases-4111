Databases Project Part 3

David Li	dl3664

Kevin Wang	kjw2169

We implemented the search for song, create playlist, and song recommendation functions. We were not able to implement the listening history, as it was not feasible to have users actually "listen" to songs on our webpage.

The Song Search webpage was interesting because it involved joining across multiple tables, showing off the relationships between song, artist, genre, and album. Instead of only searching for one term, we allow users to search by (1) title, (2) artist, or (3) genre. We also allow users to see all songs in the database if they leave all three fields blank.

The Create Playlist webpage was interesting because it involved actually creating new values in the database, showing off the relationships between user, song, and playlist. We used INSERT to update our playlist table and reflect the user's actions.
