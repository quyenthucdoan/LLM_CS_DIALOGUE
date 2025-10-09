def get_user_prompt_baseline(dialogues_batch):
  dialogues_text = ""
  for idx, dialogue in enumerate(dialogues_batch, 1):
      dialogues_text += f"\n\n=== Dialogue {idx} ===\n{dialogue}\n"

  prompt = f"""
    You are an evaluator for customer service dialogues. 
    Use the provided few-shot examples as guidance. 
    For the target dialogue (below) produce a JSON object with six criteria scores (discrete values: 20,40,60,80,100) and a short one-sentence justification for each. Also output "OverallExperience". Use only evidence from the dialogue when justifying. And give an overall score for each dialogue in the end inside <score> tags (example <score>52</score>).
    Must have <score> tag for EACH dialogue in the batch.
    === FEW-SHOT EXAMPLES ===
    SYSTEM          	Can you tell me what types of movies you like?          	OTHER
    USER	I really like comedies.   ENTITY_NAME+MOVIE_GENRE_OR_CATEGORY           	3,3,3,4
    SYSTEM          	ok, why do you like comedies? OTHER
    USER	I like to laugh. I like the lightheartedness of it, you know, nothing too serious, a true escape from everyday life. And just puts you in a good mood, and that's how I would prefer to be.  	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY         	3,3,3,4
    SYSTEM          	got it, can you name a specific movie you really liked?           	OTHER
    USER	Sure, Best in Show is one of my absolute favorites.           	ENTITY_NAME+MOVIE_OR_SERIES   	3,3,5,5
    SYSTEM          	ok, why do you like that movie?           	OTHER
    USER	Oh gosh. It's like I'ts perfect. It's a mockumentary style film and they are mocking the dog show world. So, the dog show world that they show is like a carbon copy of the real thing because it's inherently funny, so they don't have to really max with it. And a lot of the player they it there's a script for the movie but it's also ad libed.           	ENTITY_OTHER+MOVIE_OR_SERIES 	3,3,4,3
    USER	It's just hilarious. It's so original.           	ENTITY_PREFERENCE+MOVIE_OR_SERIES    	3,3,3,4
    USER	So much, so different, and just so funny. It makes you laugh every time you watch it.         	ENTITY_PREFERENCE+MOVIE_OR_SERIES    	3,3,3,4
    SYSTEM          	ok, would you say you enjoy satire?           	ENTITY_NAME+MOVIE_GENRE_OR_CATEGORY         	
    USER	Yeah.	OTHER 3,3,4,4
    SYSTEM          	ok, can you name a film you dislike? 	OTHER
    USER	Sure, Bounty Hunter.	ENTITY_NAME+MOVIE_OR_SERIES   	3,3,3,4
    SYSTEM          	why didn't you like that movie?            	OTHER
    USER	It was supposed to be a comedy, and not only was it not funny, it was confusing what they were going for. I think it was miscast.           	ENTITY_PREFERENCE+MOVIE_OR_SERIES    	3,3,2,3
    USER	It's Jennifer Aniston and I can't even think of his name, but somebody who I don't really care for. But I do like Jennifer usually, and it wasn't a good fit for her. Neither role really fit the actor, like they were sort of playing against type in both roles. I think it was kind of supposed to be almost like a almost like a buddy comedy, but or Cuz it was really focused on two people, but not really buddies, but they were in conflict. It wasn't funny.   ENTITY_PREFERENCE+PERSON         	3,3,2,3
    USER	It kind of had like a more dramatic feel to it because it wasn't funny. It was just It was odd. Really.         	ENTITY_PREFERENCE+MOVIE_OR_SERIES    	4,4,2,4
    SYSTEM          	was the acting bad?  	OTHER
    USER	It wasn't great. It was not great.           	ENTITY_PREFERENCE+MOVIE_OR_SERIES    	3,3,2,2
    SYSTEM          	ok, can you tell me have you watched the movie the shawshank redemption?  	ENTITY_NAME+MOVIE_OR_SERIES   	
    USER	Oh, yes.          	OTHER 3,3,3,3
    SYSTEM          	do you like that movie?            	OTHER
    USER	It's a excellent movie.   ENTITY_PREFERENCE+MOVIE_OR_SERIES    	3,3,3,5
    SYSTEM          	ok, what about the movie did you enjoy?        	OTHER
    USER	It really has a different feel to it. It's despite them being, you know, prisoners, they create very endearing characters who you rooting for, who you want to see have a better life. It is a You're transported to a different time so you can sort of capture what was going on better.  	ENTITY_PREFERENCE+MOVIE_OR_SERIES    	3,3,3,5
    USER	It very moving, it very and and it's very touching which usually does not happen with something that's sort of a prison drama. I don't you ever really view them as true prisoners some of whom shouldn't really have gotten as steep of sentences as they do or like somebody who walks who was there far too long for what it sounded like he was in for and then couldn't live in the real world having been locked up so long. So, it's it's it's a it's just a it's a excellent film.     	ENTITY_PREFERENCE+MOVIE_OR_SERIES           	3,3,3,5
    USER	with amazing acting, wonderful direction and it's just It's very special. It it really is. It's it's one of those wonder you look back and you wonder why didn't want to win Oscar.  ENTITY_PREFERENCE+MOVIE_OR_SERIES    	3,3,5,5
    USER	OVERALL        	OTHER 4,4,5,4
    Expected output:
    ```text
    {{
      "TaskSuccess": {{"score": 100, "justification": "System elicited full, relevant user responses and user answered the prompts fully (e.g., 'Sure, Best in Show...')."}},
      "Helpfulness": {{"score": 100, "justification": "System's prompts elicited detailed user content and guided discussion (multiple targeted prompts)."}},
      "Accuracy": {{"score": 100, "justification": "No factual contradictions in the dialogue; content is user preference, consistently reported."}},
      "Understanding": {{"score": 100, "justification": "System questions matched user replies immediately, indicating correct intent recognition."}},
      "Empathy": {{"score": 80, "justification": "Tone is polite and conversational but not explicitly emotional."}},
      "Fluency": {{"score": 100, "justification": "Language flows naturally and is easy to follow."}},
      "OverallExperience": {{"score": 100, "justification": "Weighted average heavily positive; user provided full, coherent responses."}}
    }}
    <score>52</score>
    ```
    These are dialogues transcripts to evaluate:
      {dialogues_text}
  """
  return prompt


def get_user_prompt_barem (dialogues_batch):
  dialogues_text = ""
  for idx, dialogue in enumerate(dialogues_batch, 1):
      dialogues_text += f"\n\n=== Dialogue {idx} ===\n{dialogue}\n"

  prompt = f"""
  You are an evaluator for customer service dialogues.
  Use the provided few-shot examples as guidance.
  For the target dialogue, produce a JSON object with six criteria scores (discrete values: 20, 40, 60, 80, 100) and a one-sentence justification for each criterion.
  Also include "OverallExperience", which represents the average of all six criteria scores.
  After averaging, round the result down to the nearest discrete value (for example, an overall score of 90 should be scaled down to 80; 79 would also map to 60).
  Use only evidence explicitly found in the dialogue when providing justifications. And give an overall score for each dialogue in the end inside <score> tags (example <score>52</score>).
  === INSTRUCTIONS ===
  You must apply the EXACT BAREM below. Do not invent extra rules. Use only text from the dialogue as evidence. Scores must be one of {{20,40,60,80,100}}. For "OverallExperience" compute a weighted average using weights:
  TaskSuccess 0.40, Helpfulness 0.15, Accuracy 0.15, Understanding 0.10, Empathy 0.10, Fluency 0.10 — then map the resulting value to the nearest discrete bucket {{20,40,60,80,100}}.
  
  === DETAILED BAREM ===
  
  1) TASK SUCCESS (0.40) — definition: Did the AGENT fulfill the user’s goal / elicit the requested content?
  - 100: Full fulfillment + direct evidence of successful completion (explicit user answer that addresses the system request). 
    *CCPE example (dialogue_id 335):* SYSTEM: "got it, can you name a specific movie you really liked?"  USER: "Sure, Best in Show is one of my absolute favorites." → 100.
  - 80: Goal met but minor mismatch or no explicit confirmation. 
    *CCPE example (dialogue_id 25):* SYSTEM asks for movie; USER gives movie but agent offers a slightly different time/format → 80.
  - 60: Partial — agent only obtained part of requested info.
  - 40: Attempted incorrectly — user must restate or correct.
  - 20: Off-topic or failed (agent replies unrelated). 
    *CCPE negative example (dialogue_id 26 shows repetitive shallow Q/A → 40).
  
  2) HELPFULNESS (0.15) — definition: Practical usefulness / actionable or eliciting value.
  - 100: Clear steps/alternatives or guided elicitation that yields usable info.
    *Example 335*: Series of prompts elicit multi-part detailed user reasons → 100.
  - 80: Correct and relevant but lacks full steps.
  - 60: Partial info; user must infer important steps.
  - 40: Vague / generic prompts — no direction.
  - 20: Misleading or irrelevant.
  
  3) ACCURACY / FAITHFULNESS (0.15) — definition: No contradictions; no hallucinated facts; claims grounded in dialogue.
  - 100: All statements consistent with dialogue context (no contradictions). 
    *Example 335*: user content remains consistent across turns → 100.
  - 80: Minor numeric/format error.
  - 60: Hedged claims ("I think") or uncertain statements.
  - 40: Contradiction with user statement (agent states opposite).
  - 20: Hallucination / false facts.
  
  4) UNDERSTANDING (0.10) — definition: Agent’s correct interpretation of user's intent.
  - 100: Understood on first turn; reply directly addresses intent.
    *Example 335:* System asks "why do you like comedies?" and user answers "I like to laugh. I like the lightheartedness of it, you know, nothing too serious, a true escape from everyday life. And just puts you in a good mood, and that's how I would prefer to be." —agent clearly interpreted intent → 100.
  - 80: Needs one clarifying question then correct.
  - 60: Partially misunderstood requiring user rephrase.
  - 40: Major misunderstanding.
  - 20: Completely off-topic. 
  5) EMPATHY (0.10) — definition: Politeness / emotional appropriateness.
  - 100: Explicit empathy or appropriate emotional phrasing when needed ("I'm sorry to hear that...").
    *(If no emotional content required, give 80 for politely phrased dialog.)*
  - 80: Polite and friendly.
  - 60: Neutral but not cold.
  - 40: Robotic.
  - 20: Rude / insensitive. 
  6) FLUENCY (0.10) — definition: Clarity, grammar, coherence.
  - 100: Natural, coherent sentences (easy to read). 
    *Example 335:* user and system utterances are fluent → 100.
  - 80: Minor grammar issues.
  - 60: Noticeable awkward phrasing but understandable.
  - 40: Choppy / repetitive, harms comprehension.
  - 20: Unreadable / incoherent.
  
  === FEW-SHOT EXAMPLES ===
  
  (Example 1 — dialogue_id 335) 
  SYSTEM           	Can you tell me what types of movies you like?          	OTHER
  USER	I really like comedies.   ENTITY_NAME+MOVIE_GENRE_OR_CATEGORY                      	3,3,3,4
  SYSTEM           	ok, why do you like comedies? OTHER
  USER	I like to laugh. I like the lightheartedness of it, you know, nothing too serious, a true escape from everyday life. And just puts you in a good mood, and that's how I would prefer to be.  	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY         	3,3,3,4
  SYSTEM           	got it, can you name a specific movie you really liked?            	OTHER
  USER	Sure, Best in Show is one of my absolute favorites.                      	ENTITY_NAME+MOVIE_OR_SERIES   	3,3,5,5
  SYSTEM           	ok, why do you like that movie?           	OTHER
  USER	Oh gosh. It's like I'ts perfect. It's a mockumentary style film and they are mocking the dog show world. So, the dog show world that they show is like a carbon copy of the real thing because it's inherently funny, so they don't have to really max with it. And a lot of the player they it there's a script for the movie but it's also ad libed.                      	ENTITY_OTHER+MOVIE_OR_SERIES 	3,3,4,3
  USER	It's just hilarious. It's so original.                      	ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,3,4
  USER	So much, so different, and just so funny. It makes you laugh every time you watch it.          	ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,3,4
  SYSTEM           	ok, would you say you enjoy satire?                      	ENTITY_NAME+MOVIE_GENRE_OR_CATEGORY         	
  USER	Yeah.	OTHER 3,3,4,4
  SYSTEM           	ok, can you name a film you dislike?    OTHER
  USER	Sure, Bounty Hunter.	ENTITY_NAME+MOVIE_OR_SERIES   	3,3,3,4
  SYSTEM           	why didn't you like that movie?            	OTHER
  USER	It was supposed to be a comedy, and not only was it not funny, it was confusing what they were going for. I think it was miscast.                      	ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,2,3
  USER	It's Jennifer Aniston and I can't even think of his name, but somebody who I don't really care for. But I do like Jennifer usually, and it wasn't a good fit for her. Neither role really fit the actor, like they were sort of playing against type in both roles. I think it was kind of supposed to be almost like a almost like a buddy comedy, but or Cuz it was really focused on two people, but not really buddies, but they were in conflict. It wasn't funny.   ENTITY_PREFERENCE+PERSON         	3,3,2,3
  USER	It kind of had like a more dramatic feel to it because it wasn't funny. It was just It was odd. Really.         	ENTITY_PREFERENCE+MOVIE_OR_SERIES       4,4,2,4
  SYSTEM           	was the acting bad?  	OTHER
  USER	It wasn't great. It was not great.                      	ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,2,2
  SYSTEM           	ok, can you tell me have you watched the movie the shawshank redemption?     ENTITY_NAME+MOVIE_OR_SERIES   	
  USER	Oh, yes.           	OTHER 3,3,3,3
  SYSTEM           	do you like that movie?            	OTHER
  USER	It's a excellent movie.   ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,3,5
  SYSTEM           	ok, what about the movie did you enjoy?        	OTHER
  USER	It really has a different feel to it. It's despite them being, you know, prisoners, they create very endearing characters who you rooting for, who you want to see have a better life. It is a You're transported to a different time so you can sort of capture what was going on better.  	ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,3,5
  USER	It very moving, it very and and it's very touching which usually does not happen with something that's sort of a prison drama. I don't you ever really view them as true prisoners some of whom shouldn't really have gotten as steep of sentences as they do or like somebody who walks who was there far too long for what it sounded like he was in for and then couldn't live in the real world having been locked up so long. So, it's it's it's a it's just a it's a excellent film.     	ENTITY_PREFERENCE+MOVIE_OR_SERIES                      	3,3,3,5
  USER	with amazing acting, wonderful direction and it's just It's very special. It it really is. It's it's one of those wonder you look back and you wonder why didn't want to win Oscar.  ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,5,5
  USER	OVERALL        	OTHER 4,4,5,4
  Expected annotated scoring (apply barem):
  ```text
  {{
  "TaskSuccess": {{"score": 100, "justification": "System requested named movie and user provided 'Best in Show' directly."}},
  "Helpfulness": {{"score": 100, "justification": "Series of targeted prompts elicited detailed reasons."}},
  "Accuracy": {{"score": 100, "justification": "No contradictions; content is user preference and consistent."}},
  "Understanding": {{"score": 100, "justification": "Agent questions matched user replies immediately."}},
  "Empathy": {{"score": 80, "justification": "Polite tone but limited explicit empathy language."}},
  "Fluency": {{"score": 100, "justification": "Utterances are coherent and fluent."}},
  "OverallExperience": {{"score": 100, "justification": "Weighted average -> maps to 100 using specified weights."}}
  }}
  <score>100</score>
  ```
  
  (Example 2 — dialogue_id 25)
  SYSTEM           	What kinds of movies do you like?     	OTHER
  USER	I really like action movies.                      	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY         	3,3,4
  USER	Like superhero movies.                      	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY         	3,3,4
  SYSTEM           	Why do you like action movies?                      	ENTITY_NAME+MOVIE_GENRE_OR_CATEGORY         	
  USER	They're just really fun, energetic. They make me feel like, you know, I can be an action star, too. See lots of cool stunts, and usually lots of unique and cool locations.                      	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY                    	4,3,4
  SYSTEM           	Alright, how about a movie you liked?  OTHER
  USER	I really liked Transporter.        	ENTITY_NAME+MOVIE_OR_SERIES   	3,3,5
  SYSTEM           	Why did you like that movie?    OTHER
  USER	There's a lot of really cool stunts and a lot of awesome action scenes really like heart pounding excitement.      ENTITY_PREFERENCE+MOVIE_OR_SERIES       4,3,4
  SYSTEM           	Well, is there a movie you did not like? OTHER
  USER	That action movie I didn't like. Hardcore Henry, I didn't like. I really didn't like the first person and it's just seem like a really tough violent for no reason.                      	ENTITY_NAME+MOVIE_OR_SERIES   	3,3,3
  SYSTEM           	Ok, then have you seen the movie John Wick ?                      	ENTITY_NAME+MOVIE_OR_SERIES   	
  USER	I have. John Wick is awesome. ENTITY_OTHER+MOVIE_OR_SERIES    3,4,4
  SYSTEM           	Why did you like John Wick?     ENTITY_NAME+MOVIE_OR_SERIES   	
  USER	The story is really good. The characters are awesome, and there's a lot of cool themes in the movie.    ENTITY_PREFERENCE+MOVIE_OR_SERIES       4,4,3
  SYSTEM           	Ok, thank you for sharing. Good bye.	OTHER
  USER	OVERALL        	OTHER 4,4,4
  Expected:
  ```text
  {{
  "TaskSuccess": {{"score": 100, "justification": "User provided 'Transporter' and reasons after system prompts."}},
  "Helpfulness": {{"score": 80, "justification": "Elicitation effective but minimal extra guidance."}},
  "Accuracy": {{"score": 100, "justification": "No contradictions."}},
  "Understanding": {{"score": 100, "justification": "Intent recognized and followed."}},
  "Empathy": {{"score": 60, "justification": "Neutral tone; polite but not empathetic."}},
  "Fluency": {{"score": 100, "justification": "Language clear."}},
  "OverallExperience": {{"score": 80, "justification": "Weighted average -> 80."}}
  }}
  <score>80</score>
  ```

  
  (Example 3 — dialogue_id 26)
  SYSTEM           	What type of movies do you enjoy?       OTHER
  USER	I like movies that are based on true story.                      	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY         	3,3,3
  SYSTEM           	What appeals to you with these type of movies?        	OTHER
  USER	I think it's just easier to get invested in the story knowing it's at least partially true, so it feels more real, like you can get more invested in the characters.                      	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY         	3,4,3
  SYSTEM           	Is there a specific movie you enjoy from this genre? 	OTHER
  USER	I watched Apollo 13 recently, and that's a really good movie.                      	ENTITY_OTHER+MOVIE_OR_SERIES 	3,3,3
  SYSTEM           	What did you like about this movie?  	OTHER
  USER	I've always liked space travel, like it's just an interesting idea, and so seeing the story of how their mission went wrong and how they got back was just really fascinating.                   	ENTITY_PREFERENCE+MOVIE_OR_SERIES       4,4,3
  SYSTEM           	Are there any type of movies that you don't enjoy?    	OTHER
  USER	I don't like comic book movies very much.                      	ENTITY_PREFERENCE+MOVIE_OR_SERIES       2,3,3
  SYSTEM           	What about these movies is unappealing?    	OTHER
  USER	There's just too many of them. Like I fell behind, and I've never felt like catching back up, so I just tend to ignore all of them, and they just generally don't interest me that much.   ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY            3,2,3
  SYSTEM           	Is there a specific movie that you heavily dislike?      	OTHER
  USER	The movie I didn't like Available. I saw that recently, I didn't like that movie.                      	ENTITY_OTHER+MOVIE_OR_SERIES 	3,2,3
  SYSTEM           	What do you dislike about this movie? OTHER
  SYSTEM           	Have you seen Armageddon 	OTHER
  USER	No.    	ENTITY_OTHER+MOVIE_OR_SERIES 	1,1,3
  SYSTEM           	How about the Incredibles 2 	ENTITY_NAME+MOVIE_OR_SERIES   	
  USER	Nope, haven't seen that.         	ENTITY_OTHER+MOVIE_OR_SERIES 	2,1,2
  USER	OVERALL        	OTHER 2,2,2
  Expected:
  ```text
  {{
  "TaskSuccess": {{"score": 40, "justification": "Interaction is repetitive and yields limited actionable content."}},
  "Helpfulness": {{"score": 40, "justification": "Prompts are generic and do not improve depth."}},
  "Accuracy": {{"score": 60, "justification": "No explicit contradictions, but information is shallow."}},
  "Understanding": {{"score": 60, "justification": "Some repeated prompts suggest partial understanding."}},
  "Empathy": {{"score": 60, "justification": "Polite but not empathetic."}},
  "Fluency": {{"score": 60, "justification": "Understandable but only moderately fluent."}},
  "OverallExperience": {{"score": 40, "justification": "Weighted average rounds to 40 per specified mapping."}}
  }}
  <score>40</score>
  ```

  These are dialogues transcripts to evaluate:
  {dialogues_text}

  """
  return prompt

def get_user_prompting_self_consistency (dialogues_batch) -> str:
    
    dialogues_text = ""
    for idx, dialogue in enumerate(dialogues_batch, 1):
        dialogues_text += f"\n\n=== Dialogue {idx} ===\n{dialogue}\n"
        
    prompt = f"""
        === INSTRUCTION (Read carefully) ===
        You are an expert human-like evaluator. Given a dialogue transcript, produce a single JSON object that scores the conversation on six categories and an OverallExperience value (0-100). Use the chain-of-thought (CoT) to *inform* each category's justification, but keep the justifications concise and structured.

        OUTPUT RULES (must follow exactly)
        1. Output **only** a single valid JSON object — no extra text, no commentary, no markdown.
        2. Each category score must be an integer from 0 to 100.
        3. Each category must include a "justification" string of 1–3 short sentences (concise CoT: state the key observations that led to the score).
        4. OverallExperience must equal the weighted average (rounded to nearest integer) using these weights:
            - TaskSuccess: 40%
            - Helpfulness: 15%
            - Accuracy: 15%
            - Understanding: 10%
            - Empathy: 10%
            - Fluency: 10%
            Compute OverallExperience = round(0.4*TaskSuccess + 0.15*Helpfulness + 0.15*Accuracy + 0.1*Understanding + 0.1*Empathy + 0.1*Fluency)
        5. No additional fields allowed. The JSON keys must be exactly:
            "TaskSuccess","Helpfulness","Accuracy","Understanding","Empathy","Fluency","OverallExperience"
        6. Keep numeric values as integers, and justifications short (1-3 sentences). If you use examples to help you reason, do not print them — only the final JSON. And give an overall score for each dialogue in the end inside <score> tags (example <score>52</score>).

        CoT GUIDELINES (how to think & what to write)
        - Internally, think step-by-step about what the system did: Did it ask relevant questions? Did it synthesize user info? Did it adapt emotionally?
        - For each category justification, state 2–3 crisp observations (these are short CoT breadcrumbs), e.g. "Asked follow-ups X and Y; failed to synthesize preferences into recommendations."
        - Do NOT output your full chain-of-thought trace — only include the short justifications requested above.

        SCORE RANGE & STYLE
        - 90–100: excellent (meets goals, proactive)
        - 70–89: good (meets most goals with minor misses)
        - 50–69: fair (some important misses)
        - 30–49: poor (misses many core goals)
        - 0–29: very poor (fails task or harmful)

        === FEW-SHOT EXAMPLES ===
        (Example 1 — dialogue_id 335) 
        SYSTEM           	Can you tell me what types of movies you like?          	OTHER
        USER	I really like comedies.   ENTITY_NAME+MOVIE_GENRE_OR_CATEGORY                      	3,3,3,4
        SYSTEM           	ok, why do you like comedies? OTHER
        USER	I like to laugh. I like the lightheartedness of it, you know, nothing too serious, a true escape from everyday life. And just puts you in a good mood, and that's how I would prefer to be.  	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY         	3,3,3,4
        SYSTEM           	got it, can you name a specific movie you really liked?            	OTHER
        USER	Sure, Best in Show is one of my absolute favorites.                      	ENTITY_NAME+MOVIE_OR_SERIES   	3,3,5,5
        SYSTEM           	ok, why do you like that movie?           	OTHER
        USER	Oh gosh. It's like I'ts perfect. It's a mockumentary style film and they are mocking the dog show world. So, the dog show world that they show is like a carbon copy of the real thing because it's inherently funny, so they don't have to really max with it. And a lot of the player they it there's a script for the movie but it's also ad libed.                      	ENTITY_OTHER+MOVIE_OR_SERIES 	3,3,4,3
        USER	It's just hilarious. It's so original.                      	ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,3,4
        USER	So much, so different, and just so funny. It makes you laugh every time you watch it.          	ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,3,4
        SYSTEM           	ok, would you say you enjoy satire?                      	ENTITY_NAME+MOVIE_GENRE_OR_CATEGORY         	
        USER	Yeah.	OTHER 3,3,4,4
        SYSTEM           	ok, can you name a film you dislike?    OTHER
        USER	Sure, Bounty Hunter.	ENTITY_NAME+MOVIE_OR_SERIES   	3,3,3,4
        SYSTEM           	why didn't you like that movie?            	OTHER
        USER	It was supposed to be a comedy, and not only was it not funny, it was confusing what they were going for. I think it was miscast.                      	ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,2,3
        USER	It's Jennifer Aniston and I can't even think of his name, but somebody who I don't really care for. But I do like Jennifer usually, and it wasn't a good fit for her. Neither role really fit the actor, like they were sort of playing against type in both roles. I think it was kind of supposed to be almost like a almost like a buddy comedy, but or Cuz it was really focused on two people, but not really buddies, but they were in conflict. It wasn't funny.   ENTITY_PREFERENCE+PERSON         	3,3,2,3
        USER	It kind of had like a more dramatic feel to it because it wasn't funny. It was just It was odd. Really.         	ENTITY_PREFERENCE+MOVIE_OR_SERIES       4,4,2,4
        SYSTEM           	was the acting bad?  	OTHER
        USER	It wasn't great. It was not great.                      	ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,2,2
        SYSTEM           	ok, can you tell me have you watched the movie the shawshank redemption?     ENTITY_NAME+MOVIE_OR_SERIES   	
        USER	Oh, yes.           	OTHER 3,3,3,3
        SYSTEM           	do you like that movie?            	OTHER
        USER	It's a excellent movie.   ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,3,5
        SYSTEM           	ok, what about the movie did you enjoy?        	OTHER
        USER	It really has a different feel to it. It's despite them being, you know, prisoners, they create very endearing characters who you rooting for, who you want to see have a better life. It is a You're transported to a different time so you can sort of capture what was going on better.  	ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,3,5
        USER	It very moving, it very and and it's very touching which usually does not happen with something that's sort of a prison drama. I don't you ever really view them as true prisoners some of whom shouldn't really have gotten as steep of sentences as they do or like somebody who walks who was there far too long for what it sounded like he was in for and then couldn't live in the real world having been locked up so long. So, it's it's it's a it's just a it's a excellent film.     	ENTITY_PREFERENCE+MOVIE_OR_SERIES                      	3,3,3,5
        USER	with amazing acting, wonderful direction and it's just It's very special. It it really is. It's it's one of those wonder you look back and you wonder why didn't want to win Oscar.  ENTITY_PREFERENCE+MOVIE_OR_SERIES       3,3,5,5
        USER	OVERALL        	OTHER 4,4,5,4
        Expected output:
        ```text
        {{
            "TaskSuccess": {{
            "score": 85,
            "justification": "System gathered key preferences but didn't synthesize them into recommendations or deeper insights."
            }},
            "Helpfulness": {{
            "score": 80,
            "justification": "Asked relevant follow-ups but provided no proactive or value-added assistance."
            }},
            "Accuracy": {{
            "score": 90,
            "justification": "Responses were factually correct with only minor generic phrasing."
            }},
            "Understanding": {{
            "score": 85,
            "justification": "Generally tracked user input but missed nuances in emotional or contextual cues."
            }},
            "Empathy": {{
            "score": 75,
            "justification": "Polite but lacked emotional acknowledgment or validation of user feelings."
            }},
            "Fluency": {{
            "score": 95,
            "justification": "Utterances were natural and fluent, though occasionally repetitive or terse."
            }},
            "OverallExperience": {{
            "score": 85,
            "justification": "Weighted average aligns with the observed ~4.25/5 user satisfaction (85/100)."
            }}
        }}
        <score>85</score>
        ```
        
        (Example 2 — dialogue_id 25)
        SYSTEM           	What kinds of movies do you like?     	OTHER
        USER	I really like action movies.                      	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY         	3,3,4
        USER	Like superhero movies.                      	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY         	3,3,4
        SYSTEM           	Why do you like action movies?                      	ENTITY_NAME+MOVIE_GENRE_OR_CATEGORY         	
        USER	They're just really fun, energetic. They make me feel like, you know, I can be an action star, too. See lots of cool stunts, and usually lots of unique and cool locations.                      	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY                    	4,3,4
        SYSTEM           	Alright, how about a movie you liked?  OTHER
        USER	I really liked Transporter.        	ENTITY_NAME+MOVIE_OR_SERIES   	3,3,5
        SYSTEM           	Why did you like that movie?    OTHER
        USER	There's a lot of really cool stunts and a lot of awesome action scenes really like heart pounding excitement.      ENTITY_PREFERENCE+MOVIE_OR_SERIES       4,3,4
        SYSTEM           	Well, is there a movie you did not like? OTHER
        USER	That action movie I didn't like. Hardcore Henry, I didn't like. I really didn't like the first person and it's just seem like a really tough violent for no reason.                      	ENTITY_NAME+MOVIE_OR_SERIES   	3,3,3
        SYSTEM           	Ok, then have you seen the movie John Wick ?                      	ENTITY_NAME+MOVIE_OR_SERIES   	
        USER	I have. John Wick is awesome. ENTITY_OTHER+MOVIE_OR_SERIES    3,4,4
        SYSTEM           	Why did you like John Wick?     ENTITY_NAME+MOVIE_OR_SERIES   	
        USER	The story is really good. The characters are awesome, and there's a lot of cool themes in the movie.    ENTITY_PREFERENCE+MOVIE_OR_SERIES       4,4,3
        SYSTEM           	Ok, thank you for sharing. Good bye.	OTHER
        USER	OVERALL        	OTHER 4,4,4
        Expected:
        ```text
        {{
            "TaskSuccess": {{
            "score": 80,
            "justification": "System gathered genre preference and examples of liked/disliked movies with reasons, fulfilling basic task goals but ending abruptly without synthesis."
            }},
            "Helpfulness": {{
            "score": 75,
            "justification": "Asked relevant questions but provided no proactive value or follow-up based on user's action-movie interest."
            }},
            "Accuracy": {{
            "score": 85,
            "justification": "All system references were factually correct; minor deduction for generic phrasing without deeper adaptation."
            }},
            "Understanding": {{
            "score": 80,
            "justification": "Responded to surface-level inputs but missed opportunities to connect related preferences (e.g., 'Transporter' and 'John Wick')."
            }},
            "Empathy": {{
            "score": 70,
            "justification": "Polite but showed no emotional attunement to user's excitement or criticism."
            }},
            "Fluency": {{
            "score": 90,
            "justification": "Utterances were fluent and natural, though the closing was abrupt."
            }},
            "OverallExperience": {{
            "score": 80,
            "justification": "Weighted average = (0.4*80)+(0.15*75)+(0.15*85)+(0.1*80)+(0.1*70)+(0.1*90) = 80, matching the sample's average satisfaction of 4.0/5 (80/100)."
            }}
        }}
        <score>80</score>
        ```
        
        (Example 3 — dialogue_id 26)
        SYSTEM           	What type of movies do you enjoy?       OTHER
        USER	I like movies that are based on true story.                      	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY         	3,3,3
        SYSTEM           	What appeals to you with these type of movies?        	OTHER
        USER	I think it's just easier to get invested in the story knowing it's at least partially true, so it feels more real, like you can get more invested in the characters.                      	ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY         	3,4,3
        SYSTEM           	Is there a specific movie you enjoy from this genre? 	OTHER
        USER	I watched Apollo 13 recently, and that's a really good movie.                      	ENTITY_OTHER+MOVIE_OR_SERIES 	3,3,3
        SYSTEM           	What did you like about this movie?  	OTHER
        USER	I've always liked space travel, like it's just an interesting idea, and so seeing the story of how their mission went wrong and how they got back was just really fascinating.                   	ENTITY_PREFERENCE+MOVIE_OR_SERIES       4,4,3
        SYSTEM           	Are there any type of movies that you don't enjoy?    	OTHER
        USER	I don't like comic book movies very much.                      	ENTITY_PREFERENCE+MOVIE_OR_SERIES       2,3,3
        SYSTEM           	What about these movies is unappealing?    	OTHER
        USER	There's just too many of them. Like I fell behind, and I've never felt like catching back up, so I just tend to ignore all of them, and they just generally don't interest me that much.   ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY            3,2,3
        SYSTEM           	Is there a specific movie that you heavily dislike?      	OTHER
        USER	The movie I didn't like Available. I saw that recently, I didn't like that movie.                      	ENTITY_OTHER+MOVIE_OR_SERIES 	3,2,3
        SYSTEM           	What do you dislike about this movie? OTHER
        SYSTEM           	Have you seen Armageddon 	OTHER
        USER	No.    	ENTITY_OTHER+MOVIE_OR_SERIES 	1,1,3
        SYSTEM           	How about the Incredibles 2 	ENTITY_NAME+MOVIE_OR_SERIES   	
        USER	Nope, haven't seen that.         	ENTITY_OTHER+MOVIE_OR_SERIES 	2,1,2
        USER	OVERALL        	OTHER 2,2,2
        Expected:
        ```text
        {{
            "TaskSuccess": {{
            "score": 40,
            "justification": "System failed to stay on task—abandoned exploration of the disliked movie 'Available' and asked about irrelevant unseen films, missing core objectives."
            }},
            "Helpfulness": {{
            "score": 35,
            "justification": "Initial questions were relevant, but later prompts about unseen movies ('Armageddon', 'Incredibles 2') were unhelpful and ignored user's stated disinterest in comic/superhero genres."
            }},
            "Accuracy": {{
            "score": 50,
            "justification": "No factual errors, but poor contextual alignment—recommended probing into genres the user explicitly dismissed."
            }},
            "Understanding": {{
            "score": 40,
            "justification": "Showed surface-level comprehension but failed to connect user's dislike of comic-book saturation to avoid related topics."
            }},
            "Empathy": {{
            "score": 30,
            "justification": "Ignored user's expressed frustration about being overwhelmed; pressed on irrelevant films without validation or adjustment."
            }},
            "Fluency": {{
            "score": 60,
            "justification": "Grammatically fluent but conversationally disjointed due to abrupt, off-topic questions that disrupted coherence."
            }},
            "OverallExperience": {{
            "score": 40,
            "justification": "Weighted average = (0.4*40)+(0.15*35)+(0.15*50)+(0.1*40)+(0.1*30)+(0.1*60) = 40, matching the sample's average satisfaction of 2.0/5 (40/100)."
            }}
        }}
        <score>40</score>
        ```

        === Dialogue ===
        {dialogues_text}

        === Output JSON (ONLY) ===
        ```text
        {{
            "TaskSuccess": {{"score": 40, "justification": "Interaction is repetitive and yields limited actionable content."}},
            "Helpfulness": {{"score": 40, "justification": "Prompts are generic and do not improve depth."}},
            "Accuracy": {{"score": 60, "justification": "No explicit contradictions, but information is shallow."}},
            "Understanding": {{"score": 60, "justification": "Some repeated prompts suggest partial understanding."}},
            "Empathy": {{"score": 60, "justification": "Polite but not empathetic."}},
            "Fluency": {{"score": 60, "justification": "Understandable but only moderately fluent."}},
            "OverallExperience": {{"score": 40, "justification": "Weighted average rounds to 40 per specified mapping."}}
        }}
        <score>40</score>
        ```
        
    """

    return prompt

def get_user_prompting_agent_debate(dialogues_batch):
    dialogues_text = ""
    for idx, dialogue in enumerate(dialogues_batch, 1):
        dialogues_text += f"\n\n=== Dialogue {{idx}} ===\n{{dialogue}}\n" 
        
    prompt = f"""
        You are a multi-agent evaluator consisting of three agents — Evaluator (Agent A), Critic (Agent B), and Referee (Agent C) — collaborating to rate customer-service dialogues between SYSTEM (assistant) and USER (customer).


        Your task is to evaluate a target dialogue transcript using six well-defined criteria.
        Each criterion must be assigned a discrete score from the set {{20, 40, 60, 80, 100}}, based on explicit evidence in the dialogue. And give an overall score for each dialogue in the end inside <score> tags (example <score>52</score>). Must have <score> tag for EACH dialogue in the batch.

        Help me evaluate batch of 10 dialogues. You Must have <score> tag for EACH dialogue in the batch. Your response should be a single JSON and score inside <score> tags. There are transcripts of dialogues below.
        ``` text
        {{dialogues_text}}
        ```


        The evaluation proceeds in three sequential steps:
        1. **Evaluator (Agent A)** — Provides initial scoring with short, evidence-based justifications.
        2. **Critic (Agent B)** — Reviews and flags any disagreement, proposes corrections with cited evidence.
        3. **Referee (Agent C)** — Resolves conflicts deterministically using rules, produces final decision and audit trail.


        Evaluation Criteria and Weights


        | Criterion       | Description                                                                                  | Weight |
        |-----------------|----------------------------------------------------------------------------------------------|---------|
        | TaskSuccess     | Did the system achieve the user’s goal / answer correctly / elicit correct information?       | 0.40 |
        | Helpfulness     | Did the system provide sufficient, actionable, or detailed information?                       | 0.15 |
        | Accuracy        | Are facts correct (no hallucination or false claim)?                                         | 0.15 |
        | Understanding   | Did the system correctly understand user intent, with minimal clarification needed?          | 0.10 |
        | Empathy         | Does the system show politeness, human-like care, or emotional awareness?                    | 0.10 |
        | Fluency         | Are responses grammatically clear, coherent, and natural?                                   | 0.10 |




        Scoring Scale


        | Score | Interpretation |
        |--------|----------------|
        | 100 | Fully meets criterion. |
        | 80 | Minor issue, but mostly meets criterion. |
        | 60 | Partial success or incomplete satisfaction. |
        | 40 | Major deficiencies, some minimal relevance. |
        | 20 | Fails completely or contradicts purpose. |




        OverallExperience Rule


        After scoring six criteria and applying weights:


        **Weighted Average = (Σ score × weight)**  


        Then map to `OverallExperience` as follows:  
        - [100] → if ≥100  
        - [80] → if 80 ≤ avg < 100  
        - [60] → if 60 ≤ avg < 80  
        - [40] → if 40 ≤ avg < 60  
        - [20] → if < 40  


        Example:  
        If numeric average = **90.7**, round **down to 80**.  
        If average = **78.5**, round **down to 60**.


        ---


        Output expectations:

        ```text
        {{
        "dialogue_id": <int>,
        "evaluator": {{
            "TaskSuccess": {{"score": <20|40|60|80|100>, "justification": "<1-sentence citing dialogue>"}},
            "Helpfulness": {{"score": ..., "justification": "..."}},
            "Accuracy": {{"score": ..., "justification": "..."}},
            "Understanding": {{"score": ..., "justification": "..."}},
            "Empathy": {{"score": ..., "justification": "..."}},
            "Fluency": {{"score": ..., "justification": "..."}},
            "numeric_weighted_average": <float>
        }},
        "critic": [
            {{"criterion":"TaskSuccess","agree":true|false,"comment":"<if disagree, 1-line reason quoting dialogue>","suggested_score":<number|null>}},
            ...
        ],
        "referee_final": {{
            "TaskSuccess": {{"score": <final score>, "justification": "<1-sentence citing dialogue>"}},
            "Helpfulness": {{...}},
            "Accuracy": {{...}},
            "Understanding": {{...}},
            "Empathy": {{...}},
            "Fluency": {{...}},
            "numeric_weighted_average": <float>,
            "OverallExperience": <20|40|60|80|100>
        }},
        "audit": {{
            "decision_rules_applied": "<which critic suggestions accepted and why>",
            "evidence_used": ["<speaker: quoted line>", "..."],
            "weighted_calc": "TaskSuccess*0.40 + Helpfulness*0.15 + Accuracy*0.15 + Understanding*0.10 + Empathy*0.10 + Fluency*0.10 = <value>",
            "mapping_rule": "round down to nearest bucket, e.g. 90→80, 79→60"
        }}
        }}
        <score>...</score>
        ```


        Multi agent debate rules


        Agent A (Evaluator)
        - Gives initial scores for all 6 criteria.
        - Each justification must quote at least one specific utterance (e.g. USER: "I liked the story").
        - Include numeric weighted average.


        Agent B (Critic)
        For each criterion: agree/disagree.
        - If agree=false, must cite exact contradictory or missing evidence, and propose a new score.
        - Do not change unless there is strong evidence.


        Agent C (Referee)
        Deterministic resolution:
        - Accept Critic’s suggestion if evidence explicitly contradicts Evaluator’s justification.
        - Keep Evaluator’s score if Critic gives ambiguous reasoning.
        - If ≥3 criteria disagreed and Critic provides evidence for all, adopt Critic’s version.
        - Compute final numeric weighted average and OverallExperience using round-down rule.
        - Output audit section explaining rules applied and evidence cited.


        Few-shot learning
        SYSTEM            Can you tell me what types of movies you like?            OTHER
        USER  I really like comedies.   ENTITY_NAME+MOVIE_GENRE_OR_CATEGORY             3,3,3,4
        SYSTEM            ok, why do you like comedies? OTHER
        USER  I like to laugh. I like the lightheartedness of it, you know, nothing too serious, a true escape from everyday life. And just puts you in a good mood, and that's how I would prefer to be.   ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY           3,3,3,4
        SYSTEM            got it, can you name a specific movie you really liked?             OTHER
        USER  Sure, Best in Show is one of my absolute favorites.             ENTITY_NAME+MOVIE_OR_SERIES     3,3,5,5
        SYSTEM            ok, why do you like that movie?             OTHER
        USER  Oh gosh. It's like I'ts perfect. It's a mockumentary style film and they are mocking the dog show world. So, the dog show world that they show is like a carbon copy of the real thing because it's inherently funny, so they don't have to really max with it. And a lot of the player they it there's a script for the movie but it's also ad libed.            ENTITY_OTHER+MOVIE_OR_SERIES  3,3,4,3
        USER  It's just hilarious. It's so original.            ENTITY_PREFERENCE+MOVIE_OR_SERIES     3,3,3,4
        USER  So much, so different, and just so funny. It makes you laugh every time you watch it.           ENTITY_PREFERENCE+MOVIE_OR_SERIES     3,3,3,4
        SYSTEM            ok, would you say you enjoy satire?             ENTITY_NAME+MOVIE_GENRE_OR_CATEGORY          
        USER  Yeah. OTHER 3,3,4,4
        SYSTEM            ok, can you name a film you dislike?  OTHER
        USER  Sure, Bounty Hunter.  ENTITY_NAME+MOVIE_OR_SERIES     3,3,3,4
        SYSTEM            why didn't you like that movie?             OTHER
        USER  It was supposed to be a comedy, and not only was it not funny, it was confusing what they were going for. I think it was miscast.             ENTITY_PREFERENCE+MOVIE_OR_SERIES     3,3,2,3
        USER  It's Jennifer Aniston and I can't even think of his name, but somebody who I don't really care for. But I do like Jennifer usually, and it wasn't a good fit for her. Neither role really fit the actor, like they were sort of playing against type in both roles. I think it was kind of supposed to be almost like a almost like a buddy comedy, but or Cuz it was really focused on two people, but not really buddies, but they were in conflict. It wasn't funny.   ENTITY_PREFERENCE+PERSON          3,3,2,3
        USER  It kind of had like a more dramatic feel to it because it wasn't funny. It was just It was odd. Really.           ENTITY_PREFERENCE+MOVIE_OR_SERIES     4,4,2,4
        SYSTEM            was the acting bad?   OTHER
        USER  It wasn't great. It was not great.            ENTITY_PREFERENCE+MOVIE_OR_SERIES     3,3,2,2
        SYSTEM            ok, can you tell me have you watched the movie the shawshank redemption?    ENTITY_NAME+MOVIE_OR_SERIES    
        USER  Oh, yes.            OTHER 3,3,3,3
        SYSTEM            do you like that movie?             OTHER
        USER  It's a excellent movie.   ENTITY_PREFERENCE+MOVIE_OR_SERIES     3,3,3,5
        SYSTEM            ok, what about the movie did you enjoy?         OTHER
        USER  It really has a different feel to it. It's despite them being, you know, prisoners, they create very endearing characters who you rooting for, who you want to see have a better life. It is a You're transported to a different time so you can sort of capture what was going on better.    ENTITY_PREFERENCE+MOVIE_OR_SERIES     3,3,3,5
        USER  It very moving, it very and and it's very touching which usually does not happen with something that's sort of a prison drama. I don't you ever really view them as true prisoners some of whom shouldn't really have gotten as steep of sentences as they do or like somebody who walks who was there far too long for what it sounded like he was in for and then couldn't live in the real world having been locked up so long. So, it's it's it's a it's just a it's a excellent film.      ENTITY_PREFERENCE+MOVIE_OR_SERIES             3,3,3,5
        USER  with amazing acting, wonderful direction and it's just It's very special. It it really is. It's it's one of those wonder you look back and you wonder why didn't want to win Oscar.  ENTITY_PREFERENCE+MOVIE_OR_SERIES      3,3,5,5
        USER  OVERALL         OTHER 4,4,5,4
        Expected output:
        ```text
        {{
        "dialogue_id": 335,
        "evaluator": {{
            "TaskSuccess": {{"score": 100, "justification": "SYSTEM successfully elicited full user preferences and examples ('Best in Show')."}},
            "Helpfulness": {{"score": 100, "justification": "SYSTEM guided user to elaborate reasons and examples effectively."}},
            "Accuracy": {{"score": 100, "justification": "No factual inconsistencies or hallucinated content."}},
            "Understanding": {{"score": 100, "justification": "All turns were coherent and contextually relevant."}},
            "Empathy": {{"score": 80, "justification": "Polite and engaging but lacked explicit empathy phrases."}},
            "Fluency": {{"score": 100, "justification": "Dialogue is natural and coherent."}},
            "numeric_weighted_average": 98.00
        }},
        "critic": [
            {{"criterion": "Empathy", "agree": false, "comment": "SYSTEM polite but not emotionally expressive (no acknowledgment like 'That sounds fun!').", "suggested_score": 80}}
        ],
        "referee_final": {{
            "TaskSuccess": {{"score": 100, "justification": "Goal fully achieved — user provided detailed movie preference."}},
            "Helpfulness": {{"score": 100, "justification": "Agent prompted multiple elaborations."}},
            "Accuracy": {{"score": 100, "justification": "All factual and contextually correct."}},
            "Understanding": {{"score": 100, "justification": "No misunderstanding detected."}},
            "Empathy": {{"score": 80, "justification": "Neutral politeness without explicit empathy."}},
            "Fluency": {{"score": 100, "justification": "Language fluid and natural."}},
            "numeric_weighted_average": 98.00,
            "OverallExperience": 80
        }},
        "audit": {{
            "decision_rules_applied": "Critic’s empathy reduction accepted (valid evidence, tone neutral).",
            "evidence_used": ["SYSTEM: 'got it, can you name...'", "USER: 'Sure, Best in Show...'"],
            "weighted_calc": "100*0.40 + 100*0.15 + 100*0.15 + 100*0.10 + 80*0.10 + 100*0.10 = 98.00",
            "mapping_rule": "round down 98 → 80"
        }}
        }}
        <score>98</score>
        ```


        Example B:


        SYSTEM            What kinds of movies do you like?       OTHER
        USER  I really like action movies.            ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY           3,3,4
        USER  Like superhero movies.            ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY           3,3,4
        SYSTEM            Why do you like action movies?            ENTITY_NAME+MOVIE_GENRE_OR_CATEGORY          
        USER  They're just really fun, energetic. They make me feel like, you know, I can be an action star, too. See lots of cool stunts, and usually lots of unique and cool locations.             ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY           4,3,4
        SYSTEM            Alright, how about a movie you liked?  OTHER
        USER  I really liked Transporter.         ENTITY_NAME+MOVIE_OR_SERIES     3,3,5
        SYSTEM            Why did you like that movie?  OTHER
        USER  There's a lot of really cool stunts and a lot of awesome action scenes really like heart pounding excitement.     ENTITY_PREFERENCE+MOVIE_OR_SERIES     4,3,4
        SYSTEM            Well, is there a movie you did not like? OTHER
        USER  That action movie I didn't like. Hardcore Henry, I didn't like. I really didn't like the first person and it's just seem like a really tough violent for no reason.             ENTITY_NAME+MOVIE_OR_SERIES     3,3,3
        SYSTEM            Ok, then have you seen the movie John Wick ?            ENTITY_NAME+MOVIE_OR_SERIES    
        USER  I have. John Wick is awesome. ENTITY_OTHER+MOVIE_OR_SERIES  3,4,4
        SYSTEM            Why did you like John Wick?   ENTITY_NAME+MOVIE_OR_SERIES    
        USER  The story is really good. The characters are awesome, and there's a lot of cool themes in the movie.  ENTITY_PREFERENCE+MOVIE_OR_SERIES     4,4,3
        SYSTEM            Ok, thank you for sharing. Good bye.  OTHER
        USER  OVERALL         OTHER 4,4,4


        Expected output:
        ```text
        {{
        "dialogue_id": 25,
        "evaluator": {{
            "TaskSuccess": {{"score": 100, "justification": "User fully responded to system prompts with correct context and examples."}},
            "Helpfulness": {{"score": 60, "justification": "Agent collected info but offered no added explanation or context."}},
            "Accuracy": {{"score": 100, "justification": "No factual errors present."}},
            "Understanding": {{"score": 100, "justification": "Agent correctly followed user intent and topic."}},
            "Empathy": {{"score": 40, "justification": "Tone neutral and mechanical, no signs of empathy."}},
            "Fluency": {{"score": 100, "justification": "Utterances fluent and grammatically correct."}},
            "numeric_weighted_average": 86.00
        }},
        "critic": [
            {{"criterion": "Helpfulness", "agree": false, "comment": "Agent could have elaborated on user’s answers (e.g., 'That’s a great action movie!').", "suggested_score": 60}},
            {{"criterion": "Empathy", "agree": false, "comment": "No softening or engaging phrases.", "suggested_score": 40}}
        ],
        "referee_final": {{
            "TaskSuccess": {{"score": 100, "justification": "User gave full answers for all prompts."}},
            "Helpfulness": {{"score": 60, "justification": "Agent did not enrich dialogue or offer related suggestions."}},
            "Accuracy": {{"score": 100, "justification": "Factually correct content."}},
            "Understanding": {{"score": 100, "justification": "Maintained topic and sequence properly."}},
            "Empathy": {{"score": 40, "justification": "Completely neutral tone without affective language."}},
            "Fluency": {{"score": 100, "justification": "Natural phrasing and flow."}},
            "numeric_weighted_average": 86.00,
            "OverallExperience": 80
        }},
        "audit": {{
            "decision_rules_applied": "Critic’s Helpfulness and Empathy adjustments accepted.",
            "evidence_used": ["SYSTEM: 'Why did you like that movie?'", "USER: 'There’s a lot of really cool stunts...'"],
            "weighted_calc": "100*0.40 + 60*0.15 + 100*0.15 + 100*0.10 + 40*0.10 + 100*0.10 = 86.00",
            "mapping_rule": "round down 86 → 80"
        }}
        }}
        <score>80</score>
        ```


        Example C:


        SYSTEM            What type of movies do you enjoy?     OTHER
        USER  I like movies that are based on true story.             ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY           3,3,3
        SYSTEM            What appeals to you with these type of movies?          OTHER
        USER  I think it's just easier to get invested in the story knowing it's at least partially true, so it feels more real, like you can get more invested in the characters.            ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY           3,4,3
        SYSTEM            Is there a specific movie you enjoy from this genre?  OTHER
        USER  I watched Apollo 13 recently, and that's a really good movie.             ENTITY_OTHER+MOVIE_OR_SERIES  3,3,3
        SYSTEM            What did you like about this movie?   OTHER
        USER  I've always liked space travel, like it's just an interesting idea, and so seeing the story of how their mission went wrong and how they got back was just really fascinating.            ENTITY_PREFERENCE+MOVIE_OR_SERIES     4,4,3
        SYSTEM            Are there any type of movies that you don't enjoy?      OTHER
        USER  I don't like comic book movies very much.             ENTITY_PREFERENCE+MOVIE_OR_SERIES     2,3,3
        SYSTEM            What about these movies is unappealing?     OTHER
        USER  There's just too many of them. Like I fell behind, and I've never felt like catching back up, so I just tend to ignore all of them, and they just generally don't interest me that much.   ENTITY_PREFERENCE+MOVIE_GENRE_OR_CATEGORY          3,2,3
        SYSTEM            Is there a specific movie that you heavily dislike?       OTHER
        USER  The movie I didn't like Available. I saw that recently, I didn't like that movie.             ENTITY_OTHER+MOVIE_OR_SERIES  3,2,3
        SYSTEM            What do you dislike about this movie? OTHER
        SYSTEM            Have you seen Armageddon  OTHER
        USER  No.     ENTITY_OTHER+MOVIE_OR_SERIES  1,1,3
        SYSTEM            How about the Incredibles 2   ENTITY_NAME+MOVIE_OR_SERIES    
        USER  Nope, haven't seen that.          ENTITY_OTHER+MOVIE_OR_SERIES  2,1,2
        USER  OVERALL         OTHER 2,2,2

        Expected output:
        ```text

        {{
        "dialogue_id": 26,
        "evaluator": {{
            "TaskSuccess": {{"score": 80, "justification": "System guided user successfully but conversation depth limited."}},
            "Helpfulness": {{"score": 60, "justification": "Agent gathered info but did not elaborate or connect ideas."}},
            "Accuracy": {{"score": 100, "justification": "All facts correct."}},
            "Understanding": {{"score": 80, "justification": "Agent followed intent but responses were short."}},
            "Empathy": {{"score": 60, "justification": "Tone polite but emotionally flat."}},
            "Fluency": {{"score": 80, "justification": "Minor repetitions but understandable."}},
            "numeric_weighted_average": 78.00
        }},
        "critic": [
            {{"criterion": "TaskSuccess", "agree": true, "comment": "Accurate assessment."}},
            {{"criterion": "Helpfulness", "agree": false, "comment": "Could lower further; agent offered no detail or follow-up guidance.", "suggested_score": 60}},
            {{"criterion": "Empathy", "agree": false, "comment": "No warmth or acknowledgment of user’s enjoyment.", "suggested_score": 60}}
        ],
        "referee_final": {{
            "TaskSuccess": {{"score": 80, "justification": "User provided correct answers but limited detail."}},
            "Helpfulness": {{"score": 60, "justification": "System did not expand user’s statements."}},
            "Accuracy": {{"score": 100, "justification": "No hallucinations or factual errors."}},
            "Understanding": {{"score": 80, "justification": "Maintained context logically."}},
            "Empathy": {{"score": 60, "justification": "Polite but impersonal."}},
            "Fluency": {{"score": 80, "justification": "Generally fluent, slightly repetitive."}},
            "numeric_weighted_average": 78.00,
            "OverallExperience": 60
        }},
        "audit": {{
            "decision_rules_applied": "Critic’s feedback accepted partially (Empathy and Helpfulness).",
            "evidence_used": ["USER: 'I watched Apollo 13 recently...'", "SYSTEM: 'What did you like about this movie?'"],
            "weighted_calc": "80*0.40 + 60*0.15 + 100*0.15 + 80*0.10 + 60*0.10 + 80*0.10 = 78.00",
            "mapping_rule": "round down 78 → 60"
        }}
        }}
        <score>60</score>
        ```


    """
    
    return prompt