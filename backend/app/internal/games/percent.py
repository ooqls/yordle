# def compare_words_to_percent(answer: str, guess: str) -> int:
#   total = 0
#   right_place_right_letter = 90 / len(answer)
#   wrong_place_right_letter = right_place_right_letter * 0.8
#   guess_dict = dict()
#   answer_dict = dict()
  
#   # loop through the guess and create a dictionary of letter to set of indices
#   # do the same thing for the answer
  
#   # loop through the guess and if the character at the index does not match the character in the answer,
#   # then check if that letter is elsewhere in the guess
#   # if it is, then swap it and add 1 to the total_changes
#   # if there isn't, then replace it with a random letter and add 1 to the total_changes
  
  
  
#   # replay the loop
#   i = 0
#   total_changes = 0
#   while i < len(answer):
#     if answer[i] == guess[i]:
#       i += 1
#       continue
#     else:
#       if answer[i] in guess[i:]:
        
#   for i in range(len(guess)):
#     c = guess[i]
#     if not c in guess_dict:
#       guess_dict[c] = [i]
#     else:
#       guess_dict[c].append(i)
      
  
  
#   each_letter = 10 / len(answer)
  
#   for i in range(len(guess)):
#     if guess[i] == answer[i]:
#       total += right_place_right_letter
#     elif guess[i] in answer:
#       total += wrong_place_right_letter
  
#   total += (len(guess) - max(len(guess) - len(answer), 0)) * each_letter
#   return total
import functools
  
@functools.lru_cache(maxsize=100)
def edit_distance_percent(answer, guess):
    if len(guess) == 0:
        return 0.0
    
    if len(answer) > len(guess):
        answer, guess = guess, answer

    distances = range(len(answer) + 1)
    for i2, c2 in enumerate(guess):
        distances_ = [i2+1]
        for i1, c1 in enumerate(answer):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return 1.0 - distances[-1] / (len(answer) + len(guess))

if __name__ == "__main__":
  print(edit_distance_percent("answer", "answer"))
  
  
