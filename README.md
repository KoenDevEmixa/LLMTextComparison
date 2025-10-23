# LLM Text Comparison

## Rubric grader
To accurately grade a rubric a few steps are needed:
1. Acquire an accurate descriptive Rubric according to the Rubric_General_Format
2. Acquire Current_levels in the Rubric
3. Acquire an feedback.txt based on the rubric questions from speech-to-text
4. Anomonize names in Rubric and Feedback.txt by replacing names with regex lower case
5. Let an LLM answer a first_prompt according to the Rubric_Answer_Format and using the feedback.txt.
6. If possible expand feedback.txt and repeat steps 3-5.
7. Now make it possible to use an followup_specific_prompt for each subquestion with the previous prompt included. 
8. Decide wheter each subquestion is answered well enough. Save the answers in Rubric_Answer_Format

Rubric_General_Format:
```yaml
General_goal1:
  Specific_goal1:
    Description:
      "This goal measures ..."
    Levels:
      Description_level1:
        "To obtain the first level in this goal .."
      Description_level2:
        "To obtain the second level in this goal .."
      Description_level3:
        "To obtain the third level in this goal .."

  Specific_goal2:
    Description:
      "This goal measures ..."
    Levels:
      Description_level1:
        "To obtain the first level in this goal .."
      Description_level2:
        "To obtain the second level in this goal .."
      Description_level3:
        "To obtain the third level in this goal .."

General_goal2:
  Specific_goal1:
    Description:
      "This goal measures ..."
    Levels:
      Description_level1:
        "To obtain the first level in this goal .."
      Description_level2:
        "To obtain the second level in this goal .."
      Description_level3:
        "To obtain the third level in this goal .."
```
Current_Levels:
```json
{
    "General_goal1": {
    "Specific_goal1": "Level1",
    "Specific_goal2": "Level2",
    },
    "General_goal2": {
    "Specific_goal1": "Level1",
    "Specific_goal2": "Level2",
    },
}
```
Rubric_Answer_Format:
```json
"specific_goal": "specific_goal1",
"estimated_level": "Level1",
"direct_feedback": "Choose one of: New_level is reached/Current_level is maintained/Data is not sufficent to grade this"
"explanation": "..."
"reference": "Quote of the specific lines in the text where you based this answer on"
```

first_prompt:
```python
"""
Je bent een beoordelaar die op basis van feedback en een rubric het niveau van een medewerker bepaalt.

Je krijgt:
1. Een rubric met beschrijvingen van gedragingen per niveau per subskill.
2. Een tekst met feedback over de medewerker.

Analyseer de feedback en bepaal voor **elke subskill** uit de rubric welk niveau het best aansluit bij het gedrag dat wordt beschreven.

Geef per subskill:
- het ingeschatte niveau (één van: Beginner, Intermediate, Professional, Advanced, Expert)
- een korte toelichting (waarom dit niveau volgens de feedback past)

Geef het antwoord als geldige JSON-lijst met dit format:
    "category": "...",
    "subskill": "...",
    "estimated_level": "...",
    "explanation": "..."

Rubric:
{rubric}

Feedback:
\"\"\"{feedback}\"\"\"
"""
```

followup_specific_prompt:
```python
"""
"""
```

## Two text comparison
To compare the specifics of two texts the following is needed:

1.  Anomonize the two texts by replacing names
2.  Decide on global or local comparions
If local:
3.  Split the two texts into the bits that contain local criteria
4.  Build a local criteria and prompt a LLM to answer according to the Criterium_Answer_Format
If global:
3.  Build global criteria and prompt the LLM to answer according to the Criterium_Answer_Format


Criterium_Answer_Format:
```json
"criterium": "specific_criterium",
"direct_feedback": "Choose one of: Ambiguous/Unambiguous/Data is not sufficent to grade this"
"explanation": "..."
"reference": "Quote of the specific lines in the two texts where you based this answer on"
```