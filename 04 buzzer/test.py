from constants import *

music_notes = [B4F, B4F, A4F, A4F,
               F5, F5, E5F, B4F, B4F, A4F, A4F, E5F, E5F, C5S, C5, B4F,
               C5S, C5S, C5S, C5S,
               C5S, E5F, C5, B4F, A4F, A4F, A4F, E5F, C5S,
               B4F, B4F, A4F, A4F,
               F5, F5, E5F, B4F, B4F, A4F, A4F, A5F, C5, C5S, C5, B4F,
               C5S, C5S, C5S, C5S,
               C5S, E5F, C5, B4F, A4F, REST, A4F, E5F, C5S, REST]

rhythm = [1, 1, 1, 1,
          3, 3, 6, 1, 1, 1, 1, 3, 3, 3, 1, 2,
          1, 1, 1, 1,
          3, 3, 3, 1, 2, 2, 2, 4, 8,
          1, 1, 1, 1,
          3, 3, 6, 1, 1, 1, 1, 3, 3, 3, 1, 2,
          1, 1, 1, 1,
          3, 3, 3, 1, 2, 2, 2, 4, 8, 4]

print(f"music notes length = {len(music_notes)}")
print(f"rhythm length = {len(rhythm)}")

for i in range(len(music_notes)):
    print(i)
    print(music_notes[i])
    print(rhythm[i]*0.2)
